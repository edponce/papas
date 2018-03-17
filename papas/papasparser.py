#!/usr/bin/env python3


'''PaPaSParser

This section provides the specification for PaPaSParser, used in both
configuration files and task parameter descriptions.

* A PaPaSParser implementation consists of tasks (or sections), identified
  by a "[task]" (or "[section]") header, and followed by up to two levels
  of "name/value" entries. That is, the first set of values can themselves
  be a pair of "name/value" entries.

* "[task]" (or "[section]") should not contain any whitespace to its left,
  that is, it should start at the first column of a line.

* The delimiter for "name/value" entries is the colon character (":").

* The first level of "names" should not contain any whitespace to its left,
  that is, it should start at the first column of a line.

* Indentation, tabs or whitespace, is used to make a "value" pertain to a
  particular "name".

* A "name" can be specified using any alphanumeric character, [0-9a-zA-Z].

* Predefined "names" are:
    * "command" - provide the command line string to run the task
    * "after" - specifies dependencies between tasks

* The only mandatory "name/value" pair is: "command".

* Inter-task interpolation using "${...}" syntax is allowed using "values"
  from both levels of entries, "${name}" and "${name:value}".

* Intra-task interpolation using "${...}" syntax is allowed using "values"
  from both levels of entries, "${task:name}" and "${task:name:value}".

* A single-line comment is a line that starts with a hash sign, "#".
'''

'''Example (simple)

# This example describes a task called "hello" to execute the program
# "hello_world.py" twice, once for each value given in "xparam" name.

[hello]
program: hello_world.py
cmdargs:
    xparam: 10
            20
command: ${program} --xparam ${cmdargs:xparam}
'''


'''
Intrinsic defaults can be specified by passing them into the
PaPaSParser constructor as a dictionary.

class:

ConfigParser -- responsible for parsing a list of
                    configuration files, and managing the parsed database.

    methods:

    __init__(defaults=None, dict_type=_default_dict, allow_no_value=False,
             delimiters=('=', ':'), comment_prefixes=('#', ';'),
             inline_comment_prefixes=None, strict=True,
             empty_lines_in_values=True, default_section='DEFAULT',
             interpolation=<unset>, converters=<unset>):
        Create the parser. When `defaults' is given, it is initialized into the
        dictionary or intrinsic defaults. The keys must be strings, the values
        must be appropriate for %()s string interpolation.

        When `dict_type' is given, it will be used to create the dictionary
        objects for the list of sections, for the options within a section, and
        for the default values.

        When `delimiters' is given, it will be used as the set of substrings
        that divide keys from values.

        When `comment_prefixes' is given, it will be used as the set of
        substrings that prefix comments in empty lines. Comments can be
        indented.

        When `inline_comment_prefixes' is given, it will be used as the set of
        substrings that prefix comments in non-empty lines.

        When `strict` is True, the parser won't allow for any section or option
        duplicates while reading from a single source (file, string or
        dictionary). Default is True.

        When `empty_lines_in_values' is False (default: True), each empty line
        marks the end of an option. Otherwise, internal empty lines of
        a multiline option are kept as part of the value.

        When `allow_no_value' is True (default: False), options without
        values are accepted; the value presented for these is None.

        When `default_section' is given, the name of the special section is
        named accordingly. By default it is called ``"DEFAULT"`` but this can
        be customized to point to any other valid section name. Its current
        value can be retrieved using the ``parser_instance.default_section``
        attribute and may be modified at runtime.

        When `interpolation` is given, it should be an Interpolation subclass
        instance. It will be used as the handler for option value
        pre-processing when using getters. RawConfigParser object s don't do
        any sort of interpolation, whereas ConfigParser uses an instance of
        BasicInterpolation. The library also provides a ``zc.buildbot``
        inspired ExtendedInterpolation implementation.

        When `converters` is given, it should be a dictionary where each key
        represents the name of a type converter and each value is a callable
        implementing the conversion from string to the desired datatype. Every
        converter gets its corresponding get*() method on the parser object and
        section proxies.

    sections()
        Return all the configuration section names, sans DEFAULT.

    has_section(section)
        Return whether the given section exists.

    has_option(section, option)
        Return whether the given option exists in the given section.

    options(section)
        Return list of configuration options for the named section.

    read(filenames, encoding=None)
        Read and parse the list of named configuration files, given by
        name.  A single filename is also allowed.  Non-existing files
        are ignored.  Return list of successfully read files.

    read_file(f, filename=None)
        Read and parse one configuration file, given as a file object.
        The filename defaults to f.name; it is only used in error
        messages (if f has no `name' attribute, the string `<???>' is used).

    read_string(string)
        Read configuration from a given string.

    read_dict(dictionary)
        Read configuration from a dictionary. Keys are section names,
        values are dictionaries with keys and values that should be present
        in the section. If the used dictionary type preserves order, sections
        and their keys will be added in order. Values are automatically
        converted to strings.

    get(section, option, raw=False, vars=None, fallback=_UNSET)
        Return a string value for the named option.  All % interpolations are
        expanded in the return values, based on the defaults passed into the
        constructor and the DEFAULT section.  Additional substitutions may be
        provided using the `vars' argument, which must be a dictionary whose
        contents override any pre-existing defaults. If `option' is a key in
        `vars', the value from `vars' is used.

    getint(section, options, raw=False, vars=None, fallback=_UNSET)
        Like get(), but convert value to an integer.

    getfloat(section, options, raw=False, vars=None, fallback=_UNSET)
        Like get(), but convert value to a float.

    getboolean(section, options, raw=False, vars=None, fallback=_UNSET)
        Like get(), but convert value to a boolean (currently case
        insensitively defined as 0, false, no, off for False, and 1, true,
        yes, on for True).  Returns False or True.

    items(section=_UNSET, raw=False, vars=None)
        If section is given, return a list of tuples with (name, value) for
        each option in the section. Otherwise, return a list of tuples with
        (section_name, section_proxy) for each section, including DEFAULTSECT.

    remove_section(section)
        Remove the given file section and all its options.

    remove_option(section, option)
        Remove the given option from the given section.

    set(section, option, value)
        Set the given option.

    write(fp, space_around_delimiters=True)
        Write the configuration state in .ini format. If
        `space_around_delimiters' is True (the default), delimiters
        between keys and values are surrounded by spaces.
"""

from collections.abc import MutableMapping
from collections import OrderedDict as _default_dict, ChainMap as _ChainMap
import functools
import io
import itertools
import os
import re
import sys
import warnings


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
