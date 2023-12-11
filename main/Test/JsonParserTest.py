import unittest
from data_processor.configuration import Config
from data_transformer.json_parser import JsonParser
from unittest import mock
from data_processor.entity import EntityCollection as EC


class JsonParserTest(unittest.TestCase):
    """
        Helps to test Abstract Parser Class
    """
    @classmethod
    def setUpClass(cls):
        """
        Helps to initialize the json data and config for all method
        :return: None
        """
        cls.json_data = {"students": []}
        cls.json_data["students"].append({"name": "Kalpana", "english":90,"math":100 })
        cls.json_data["students"].append({"name": "Abu", "english":95, "math":80 })

        cls.test_config = Config()
        cls.test_config.path = "testpath.json"
        cls.test_config.data_type = "JSON"
        cls.test_config.entity_collection = "students"
        cls.test_config.base_field = "name"
        cls.test_config.computable_fields = ['english']

    def setUp(self):
        """
        Helps to initialize parser object and entity object for each method
        :return: None
        """
        self.test_config.entity_collection = "students"
        self.test_config.computable_fields = ['english']
        self.test_json_parser = JsonParser(self.test_config)
        print("")

    def test_parse(self):
        """
        Helsp to test:-
        1) Normal test scenario
        2) Wrong Config Parse Scenario
        3) Wrong file Scenario
        4) General data not found scenario
        :return:
        """
        with mock.patch("data_transformer.json_parser.JsonParser.__load_data__") as mock_load:
            mock_load.return_value = self.json_data
            self.test_json_parser.entityCollection = EC()
            entityCollection = self.test_json_parser.parse()
        self.assertTrue(len(entityCollection.items)> 0, "Test Failed")

        # EMC - with wrong entity collection
        self.test_config.entity_collection = "Employee"
        with mock.patch("data_transformer.json_parser.JsonParser.__load_data__") as mock_load:
            with self.assertRaises(Exception):
                self.test_json_parser.parse()

        # Value error - with wrong pdf
        self.path = "test.pdf"
        self.test_config.entity_collection = "students"
        with mock.patch("data_transformer.json_parser.JsonParser.__load_data__") as mock_load:
            with self.assertRaises(Exception):
                self.test_json_parser.parse()

        self.test_config.entity_collection = "Employee"
        with self.assertRaises(Exception):
            self.test_json_parser.parse()

    def test_Load_data_and_expression(self):
        """
        Helsp to test
        1) Path not found scenario
        2) expression scenario
        :return:
        """
        with self.assertRaises(FileNotFoundError):
            self.test_json_parser.__load_data__()

        self.test_config.computable_fields.append('english+math As Total')
        with mock.patch("data_transformer.json_parser.JsonParser.__load_data__") as mock_load:
            mock_load.return_value = self.json_data
            entity_collection = self.test_json_parser.parse()
            self.assertEqual(len(entity_collection.fields), 2, "Test Failed")
            self.assertEqual(entity_collection.fields[1], "Total", "Test Failed")
            self.assertTrue(len(entity_collection.items)>0, "Test Failed")

    def tearDown(self):
        """
        Helps to delete test_parser
        :return: None
        """
        del self.test_json_parser

    @classmethod
    def tearDownClass(cls):
        """
        Helps to delete test config object and json data
        :return:
        """
        del cls.test_config
        del cls.json_data
