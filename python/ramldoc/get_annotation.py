
class AnnotatedClass(object):

    @classmethod
    def get_path_abstract(cls):
        return cls._path_auto_doc

    # Note, it's not really necessary for this to be
    # in a class (note self is not really referenced, just the method):
    @staticmethod
    def get_schema(method):
        try:
            return method._body_auto_doc['schema']

        # not available:
        except:
            return {}
