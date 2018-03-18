#!/usr/bin/env python3


import unittest
from papas import papas


class TestConfigurationFiles(unittest.TestCase):

    def test_loadYAMLTaskConf(self):
        t = load_yaml_file('papas/tasks_conf/YAML_conf/helloWorld.yml')
        self.assertTrue(len(t) > 0)

    def test_loadJSONTaskConf(self):
        t = load_json_file('papas/tasks_conf/JSON_conf/helloWorld.json')
        self.assertTrue(len(t) > 0)

    def test_validateTaskConf(self):
        with open('papas/tasks_conf/YAML_conf/helloWorld.yml', 'r') as conf:
            self.assertTrue(papas.validate_app_conf(conf.read()))


if __name__ == '__main__':
    unittest.main()
