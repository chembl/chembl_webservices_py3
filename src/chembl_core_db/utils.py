__author__ = 'mnowotka'

import re
from django.views.generic import TemplateView

#-----------------------------------------------------------------------------------------------------------------------

def plural(string):
    patterns = [('[sxz]$','$','es'),
                ('[^aeioudgkprt]h$','$','es'),
                ('[^aeiou]y$','y$','ies'),
                ('$','$','s')]

    rules = [lambda word: re.pattern_search_replace[1](pattern_search_replace[0], word) and
                                                                re.sub(pattern_search_replace[1], pattern_search_replace[2], word) for pattern_search_replace in patterns]
    for rule in rules:
        result = rule(string)
        if result:
            return result

#-----------------------------------------------------------------------------------------------------------------------

class DirectTemplateView(TemplateView):
    extra_context = None
    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        if self.extra_context is not None:
            for key, value in list(self.extra_context.items()):
                if callable(value):
                    context[key] = value()
                else:
                    context[key] = value
        return context

#-----------------------------------------------------------------------------------------------------------------------
