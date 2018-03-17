#!/usr/bin/env python3


import configparser
import collections


__all__ = ['MyParser']


class MyInterpolation(configparser.ExtendedInterpolation):

    def before_get(self, parser, section, option, value, defaults):
        L = []
        self._interpolate_some(parser, option, L, value, section, defaults, 1)
        return ''.join(L)


class MyParser(configparser.ConfigParser):

    def __init__(self, defaults=None, dict_type=collections.OrderedDict,
                 allow_no_value=True, *, delimiters=(':'),
                 comment_prefixes=('#'), inline_comment_prefixes=None,
                 strict=True, empty_lines_in_values=False,
                 default_section='DEFAULT',
                 # interpolation=configparser.ExtendedInterpolation(),
                 interpolation=MyInterpolation(),
                 converters=None):

        if not converters:
            converters = configparser.ConverterMapping(self)
        kwargs = {'delimiters': delimiters,
                  'comment_prefixes': comment_prefixes,
                  'inline_comment_prefixes': inline_comment_prefixes,
                  'strict': strict,
                  'empty_lines_in_values': empty_lines_in_values,
                  'default_section': default_section,
                  'interpolation': interpolation,
                  'converters': converters}
        super().__init__(defaults, dict_type, allow_no_value, **kwargs)

    def get(self, section, option, **kwargs):
        s = super().get(section, option, **kwargs)
        if isinstance(s, str):
            s = list(filter(None, s.split('\n')))
            if len(s) == 1:
                s = s[0]
        else:
            print('Value is not a string')
            print(type(s))
        return s

    def load(self, fn=''):
        self.read(fn)
        return self.to_dict()

    def to_dict(self):
        task_dicts = []
        for task in self.sections():
            task_dict = {'task': task}
            task_dicts.append({**task_dict, **self[task]})
        if len(task_dicts) == 1:
            return task_dicts[0]
        return task_dicts
