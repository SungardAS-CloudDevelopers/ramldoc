# OK, I think I have this figured out.  Decorators in python 2 are pure evil.
# Worse than:
#   Paper cuts
#   Tax Returns
#   Empty Beer Pints
#
# They are even more evil because the code below looks elegant.
#
# If you must use annotations, a good reference is here on a good way to build them:
# http://www.artima.com/weblogs/viewpost.jsp?thread=240845
#
# Building them in other ways make them behave in seemingly erratic ways
#
# Now, if you want to annotate classes and methods, you can do it like this:
# http://stackoverflow.com/questions/2366713/can-a-python-decorator-of-an-instance-method-access-the-class
#
# Also note that there exists a way to collapse these methods into one 'generic annotator of classes'


class path:

    def __init__(self, path):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """

        # Remember where you came from:
        self.path = path

    def __call__(self, cls):

        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        # Annotate the class with the path.
        cls._path_auto_doc = self.path

        return cls


class description:
    def __init__(self, des_string):
        self.des_string = des_string

    def __call__(self, fun):

        # annotate the function:
        fun._description_auto_doc = self.des_string

        # dont mess with the method!
        return fun


# allowed:  Multiple annotations for responses
class response:
    def __init__(self, code, description, schema=None, example=None):
        self.code = code
        self.description = description
        self.schema = schema
        self.example = example

    def __call__(self, fun):
        # build a response array if necessary:
        if not hasattr(fun, '_response_auto_doc'):
            fun._response_auto_doc = []

        # add this response:
        fun._response_auto_doc.append({"code": self.code,
                                       "description": self.description,
                                       "schema": self.schema,
                                       "example": self.example
                                       })

        # dont otherwise mess with the method!
        return fun


# a list of responses.  Note that responses must be an iterable.
class responses:

    def __init__(self, responses):
        self.responses = responses

    def __call__(self, fun):
        # build a response array if necessary:
        if not hasattr(fun, '_response_auto_doc'):
            fun._response_auto_doc = []

        for response in self.responses:
            # add this response:
            fun._response_auto_doc.append({"code": response.code,
                                           "description": response.description,
                                           "schema": response.schema,
                                           "example": response.example
                                           })

        # dont otherwise mess with the method!
        return fun


# allowed:  Multiple annotations for responses
class body:
    def __init__(self, schema=None, example=None):
        self.schema = schema
        self.example = example

    def __call__(self, fun):

        # add this response:
        fun._body_auto_doc = {"schema": self.schema, "example": self.example}

        # dont otherwise mess with the method!
        return fun


class queryparameter:
    def __init__(self, name, description, required=False, type="string"):
        self.name = name
        self.description = description
        self.required = required
        self.type = type

    def __call__(self, fun):
        # build a response array if necessary:
        if not hasattr(fun, '_parameter_auto_doc'):
            fun._parameter_auto_doc = []

        # add this parameter:
        fun._parameter_auto_doc.append({"name": self.name,
                                       "description": self.description,
                                       "required": self.required,
                                       "type": self.type
                                       })

        # dont otherwise mess with the method!
        return fun

# a list of responses.  Note that responses must be an iterable.
class queryparameters:

    def __init__(self, queryparameters):
        self.queryparameters = queryparameters

    def __call__(self, fun):
        # build a response array if necessary:
        if not hasattr(fun, '_parameter_auto_doc'):
            fun._parameter_auto_doc = []

        for response in self.queryparameters:
            # add this response:
            fun._parameter_auto_doc.append({"name": self.name,
                                           "description": self.description,
                                           "required": self.required,
                                           "type": self.type
                                           })

        # dont otherwise mess with the method!
        return fun