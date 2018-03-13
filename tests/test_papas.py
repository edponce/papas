#!/usr/bin/env python3

import unittest
import papas


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_appConfFile(self):
        with open('src/yaml_apps/hello.yaml') as fd:
            contents = fd.read()
        self.assertTrue(papas.validate_app_conf(contents))


'''
Main entry point
'''
if __name__ == '__main__':
    unittest.main()
