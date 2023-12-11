import unittest
from data_processor.configuration import Config
from data_transformer.json_parser import JsonParser
from unittest import mock
from data_processor.entity import EntityCollection as EC
from data_transformer.data_manager_factory import DataManagerFactory as DMF


class DataManagerFactoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Helps to initialize the json data and config for all method
        :return: None
        """
        cls.mockentitycollection = EC()
        cls.mockentitycollection.add("Kalpana", {"science":90,"english":85})

        cls.test_config = Config()
        cls.test_config.path = "testpath.csv"
        cls.test_config.data_type = "CSV"
        cls.test_config.entity_collection = "student"
        cls.test_config.base_field = "name"
        cls.test_config.computable_fields = ['english','english']

    def setUp(self):
        """
        Helps to initialize parser object and entity object for each method
        :return: None
        """
        self.test_config.entity_collection = "student"
        self.test_config.computable_fields = ['english']
        self.data_manager_factory = DMF(self.test_config)
        self.test_config.data_type = "CSV"
        self.mockentitycollection.add("Kalpana", {"science": 90, "english": 85})

    def test_call_parser(self):
        """
        Helps to test:-
        1) Non Empty Entity Collection scenario
        2) Non Empty Entity with empty field scenario
        :return:
        """
        with mock.patch("data_transformer.csv_parser.CsvParser.parse") as mock_parse:
            mock_parse.return_value = self.mockentitycollection
            entityCollection = self.data_manager_factory.call_parser()
            self.assertTrue(len(entityCollection.items) > 0, "Test Failed")
            self.assertTrue(len(entityCollection.items[0].field_value_pairs) > 0, "Test Failed")
            self.assertTrue(entityCollection.items[0].field_value_pairs["english"] > 0, "Test Failed")
            self.assertEqual(len(entityCollection.items[0].field_value_pairs), 2,  "Test Failed")

    """
        Helps to test:-
        1) Empty Entity Collection
        2) with unknown parser
        :return:
    """
    def test_register_and_is_empty(self):

        self.test_config.data_type = "pdf"
        entityCollection = self.data_manager_factory.call_parser()

        self.setUp()
        with self.assertRaises(Exception):
            self.mockentitycollection.items = []
            with mock.patch("data_transformer.csv_parser.CsvParser.parse") as mock_parse:
                mock_parse.return_value = self.mockentitycollection
                self.data_manager_factory.call_parser()
        self.setUp()
        with self.assertRaises(Exception):
            self.mockentitycollection.items = []
            self.mockentitycollection.add("Kalpana",{})
            with mock.patch("data_transformer.csv_parser.CsvParser.parse") as mock_parse:
                mock_parse.return_value = self.mockentitycollection
                self.data_manager_factory.call_parser()
        assert (self.data_manager_factory.parsers, 3, "test failed")
        assert (self.data_manager_factory.parsers, JsonParser, "test failed")
    def tearDown(self):
        """
        Helps to delete test_parser
        :return: None
        """
        del self.data_manager_factory

    @classmethod
    def tearDownClass(cls):
        """
        Helps to delete test config object and mock entitycollection data
        :return:
        """
        del cls.test_config
        del cls.mockentitycollection