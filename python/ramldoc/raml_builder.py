# POC for building RAML dynamically:
import inspect
import json
    
indent = "  "


# Simple class to handle output:
class _BufferedOutput:
    def __init__(self):
        self.output = ''

    def clear(self):
        self.output = ""

    def add_string(self, stringz):
        self.output += stringz + '\n'

    def get_string(self):
        return self.output
output = _BufferedOutput()


# dummy class, needed because you cant add stuff to object:
class Object:
    pass


# Note, dump to stdout for now
def build_documentation(modules, title, base_uri, version):
    output.clear()
    reflect = _parse_modules(modules)
    _build_header(title, base_uri, version)
    _build_uris(reflect.module_list)
    return output.get_string()


def _build_uris(module_list):

    # Sort the modules, determining the display path:
    sorted_modules = sorted(module_list, key=lambda val: val.path)
    last_module_path = "goofy_string_that_will_fail_startswith"
    module_depth = 0
    for module in sorted_modules:
        if module.path.startswith(last_module_path):
            module_depth += 1

            # doctor the display path:
            module.display_path = module.path[len(last_module_path):-1]

        else:
            module.display_path = module.path
            module_depth = 0

        module.depth = module_depth
        last_module_path = module.path

    # parse through all modules, dumping the raml file:
    for module in sorted_modules:
        output.add_string(indent * module.depth + "/" + str(module.display_path) + ":")

        for method in module.method_list:
            output.add_string(indent * (module.depth + 1) + method.name + ":")
            output.add_string(indent * (module.depth + 2) + "description: " + method.description)

            if len(method.parameters) > 0:
                output.add_string(indent * (module.depth + 2) + "queryParameters:")

            # dump query string parameters:
            for parameter in method.parameters:
                output.add_string(indent * (module.depth + 3) + parameter.name + ":")
                output.add_string(indent * (module.depth + 4) + "description: " + parameter.description)
                output.add_string(indent * (module.depth + 4) + "required: " + str(parameter.required).lower())
                output.add_string(indent * (module.depth + 4) + "type: " + parameter.type)
        
            # build a body if necessary:
            try:
                _build_body(module.depth + 2, method.body)
            except:
                pass

            output.add_string(indent * (module.depth + 2) + "responses:")

            sorted_responses = sorted(method.responses, key=lambda val: val.code)

            for response in sorted_responses:
                output.add_string(indent * (module.depth + 3) + str(response.code) + ":")
                output.add_string(indent * (module.depth + 4) + "description: " + response.description)

                # build a body object if necessary:
                try:
                    _build_body((module.depth + 4), response.body)
                except:
                    pass
            output.add_string("")


def _build_body(indent_level, body):
    if body is not None:
        output.add_string(indent * indent_level + "body:")
        output.add_string(indent * (indent_level+1) + "application/json:")
        output.add_string(indent * (indent_level+2) + "schema: |")
        output.add_string(indent * (indent_level+3) + json.dumps(body.schema))
        output.add_string(indent * (indent_level+2) + "example: |")
        output.add_string(indent * (indent_level+3) + json.dumps(body.example))


def _build_header(title, baseUri, version):
    output.add_string("#%RAML 0.8")
    output.add_string("---")
    output.add_string("title: " + title)
    output.add_string("baseUri: " + baseUri + '/{version}')
    output.add_string('version: ' + str(version))
    output.add_string("")


def _parse_modules(modules):
    retval = Object()
    retval.module_list = []
    for module in modules:
        doc_module = Object()

        # pull out the path.  Note it is presumed this is a member of the AnnotationBaseClass:
        doc_module.path = module.get_path_abstract()

        # pull out the methods:
        class_methods = inspect.getmembers(module, predicate=inspect.ismethod)
        doc_module.method_list = list()

        for name, method in class_methods:

            # Restful only method names plz:
            if name in ["get", 'post', 'put', 'delete']:
                # get the method from the class
                method_pointer = module.__dict__[name]

                method = Object()
                method.name = name
                method.description = method_pointer._description_auto_doc
                method.responses = list()
                method.parameters = list()
                
                if hasattr(method_pointer, '_parameter_auto_doc'):
                    for parameter in method_pointer._parameter_auto_doc:
                        doc_parameter = Object()
                        doc_parameter.name = parameter['name']
                        doc_parameter.description = parameter['description']
                        doc_parameter.required = parameter['required']
                        doc_parameter.type = parameter['type']
                        method.parameters.append(doc_parameter)

                if hasattr(method_pointer, '_body_auto_doc'):
                    body = Object()
                    body.schema = module.get_schema(method_pointer)

                    body.example = method_pointer._body_auto_doc.get('example')
                    method.body = body

                if hasattr(method_pointer, '_response_auto_doc'):
                    for response in method_pointer._response_auto_doc:
                        doc_response = Object()
                        doc_response.code = response["code"]
                        doc_response.description = response['description']
    
                        # does the body have a response?
                        if response.get('schema') is not None or response.get('example') is not None:
                            doc_response.body = Object()
    
                        if response.get('schema') is not None:
                            doc_response.body.schema = response['schema']
    
                        if response['example'] is not None:
                            doc_response.body.example = response['example']
    
                        method.responses.append(doc_response)
                doc_module.method_list.append(method)
        retval.module_list.append(doc_module)
    return retval