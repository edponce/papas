#!/usr/bin/env python3

import os
import unittest
import papas


# Specify paths for package modules
pkgdir = 'src'


class TestConfigurationFiles(unittest.TestCase):

    def test_appConfFile(self):
        with open(os.path.join(pkgdir, 'yaml_apps/hello.yml'), 'r') as conf:
            self.assertTrue(papas.validate_app_conf(conf.read()))


if __name__ == '__main__':
    unittest.main()
