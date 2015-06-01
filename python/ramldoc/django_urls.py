import re as regex
from django.conf.urls import patterns, url


def build_patterns(modules, version):
    pattern_list = []

    for module in modules:
        url_string = r'^'
        url_string += str(version) + r'/'

        # NOTE, the assumption here is that get_path() is an instance of the AnnotationBaseClass:
        url_string += module.get_path_abstract() + r'$'
        url_string = regex.sub(r'{', r'(?P<', url_string)
        url_string = regex.sub(r'}', r'>[\w.@]+)', url_string)
        url_string = regex.sub('[\?]?[/]?\$$', '/?$', url_string)
        pattern_list.append(url(url_string, module()))
    return patterns('', *pattern_list)
