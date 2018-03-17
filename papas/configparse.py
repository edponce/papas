#!/usr/bin/env python3


from configparser import (
    ParsingError, InterpolationSyntaxError, InterpolationDepthError,
    InterpolationMissingOptionError, NoSectionError, NoOptionError
)
import configparser
import collections
import re


__all__ = ['MyParser']


class MyInterpolation(configparser.ExtendedInterpolation):

    MAX_INTERPOLATION_DEPTH = 10
    _KEYCRE = re.compile(r"\$\{([^}]+)\}")

    def before_get(self, parser, section, option, value, defaults):
        L = []
        LL = []
        self._interpolate_some(parser, option, L, value, section, defaults, 1)
        for v in L:
            if isinstance(v, list):
                for s in v:
                    LL.append(s + '\n')
            else:
                LL.append(v)
        return ''.join(LL)

    def before_set(self, parser, section, option, value):
        tmp_value = value.replace('$$', '') # escaped dollar signs
        tmp_value = self._KEYCRE.sub('', tmp_value) # valid syntax
        if '$' in tmp_value:
            raise ValueError("invalid interpolation syntax in %r at "
                             "position %d" % (value, tmp_value.find('$')))
        return value

    def _interpolate_some(self, parser, option, accum, rest, section, map,
                          depth):
        rawval = parser.get(section, option, raw=True, fallback=rest)
        if depth > self.MAX_INTERPOLATION_DEPTH:
            raise InterpolationDepthError(option, section, rawval)

        print('rawval {}'.format(rawval))
        print('rest {}'.format(rest))
        while rest:
            p = rest.find("$")
            if p < 0:
                accum.append(rest)
                return
            if p > 0:
                accum.append(rest[:p])
                rest = rest[p:]
            # p is no longer used
            c = rest[1:2]
            if c == "$":
                accum.append("$")
                rest = rest[2:]
            elif c == "{":
                m = self._KEYCRE.match(rest)
                if m is None:
                    raise InterpolationSyntaxError(option, section,
                        "bad interpolation variable reference %r" % rest)
                path = m.group(1).split(':')
                rest = rest[m.end():]
                sect = section
                opt = option
                try:
                    if len(path) == 1:
                        opt = parser.optionxform(path[0])
                        v = map[opt]
                    elif len(path) == 2:
                        sect = path[0]
                        opt = parser.optionxform(path[1])
                        v = parser.get(sect, opt, raw=True)
                    else:
                        raise InterpolationSyntaxError(
                            option, section,
                            "More than one ':' found: %r" % (rest,))
                except (KeyError, NoSectionError, NoOptionError):
                    raise InterpolationMissingOptionError(
                        option, section, rawval, ":".join(path)) from None
                if "$" in v:
                    self._interpolate_some(parser, opt, accum, v, sect,
                                           dict(parser.items(sect, raw=True)),
                                           depth + 1)
                else:
                    accum.append(v)
            else:
                raise InterpolationSyntaxError(
                    option, section,
                    "'$' must be followed by '$' or '{', "
                    "found: %r" % (rest,))


class MyParser(configparser.ConfigParser):

    papas_language = {
        'program': str,
        'cmd': str,
        'params': list,
        'before': list,
        'env': list
    }

    def __init__(self, defaults=None, dict_type=collections.OrderedDict,
                 allow_no_value=True, *, delimiters=(':'),
                 comment_prefixes=('#'), inline_comment_prefixes=None,
                 strict=True, empty_lines_in_values=False,
                 default_section='DEFAULT',
                 interpolation=MyInterpolation(),
                 converters=None):

        if not converters:
            converters = configparser.ConverterMapping(self)
        kwargs = {
            'delimiters': delimiters,
            'comment_prefixes': comment_prefixes,
            'inline_comment_prefixes': inline_comment_prefixes,
            'strict': strict,
            'empty_lines_in_values': empty_lines_in_values,
            'default_section': default_section,
            'interpolation': interpolation,
            'converters': converters
        }
        super().__init__(defaults, dict_type, allow_no_value, **kwargs)

    def get(self, section, option, **kwargs):
        v = super().get(section, option, **kwargs)
        v_list = list(filter(None, v.split('\n')))

        opt_type = self.papas_language[option]
        if isinstance(v_list, opt_type):
            return v_list

        if opt_type == str:
            if len(v_list) == 1:
                value = v_list[0]
            else:
                raise ParsingError(section)
        return value

    def load(self, fn):
        """Read and parse a filename or a list of filenames.

        Files that cannot be opened are silently ignored; this is
        designed so that you can specify a list of potential
        configuration file locations (e.g. current directory, user's
        home directory, systemwide directory), and all existing
        configuration files in the list will be read.  A single
        filename may also be given.

        Return list of successfully read files.
        """
        if isinstance(fn, list):
            for f in fn:
                self.read(f)
        else:
            self.read(fn)
        return self.to_dict()

    def to_dict(self):
        task_dicts = {}
        for task in self.sections():
           task_dicts.update({task: {**self[task]}})
        return task_dicts
