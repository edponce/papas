#!/usr/bin/env python3

import os
import unittest
from papas import papas


class TestConfigurationFiles(unittest.TestCase):

    def test_appConfFile(self):
        with open(os.path.join('papas/yaml_apps/hello.yml'), 'r') as conf:
            self.assertTrue(papas.validate_app_conf(conf.read()))


if __name__ == '__main__':
    unittest.main()
