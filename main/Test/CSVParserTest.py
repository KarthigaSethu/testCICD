import unittest
from data_processor.configuration import Config
from data_transformer.csv_parser import CsvParser
from unittest import mock
from data_processor.entity import EntityCollection as EC
import csv

class CSVParserTest(unittest.TestCase):
    """
        Helps to test Abstract Parser Class
    """
    @classmethod
    def setUpClass(cls):
        """
        Helps to initialize the csv data and config for all method
        :return: None
        """
        test_csv = """name,english,science
        John Doe,90,85
        Jane Smith,95,92
        Bob Johnson,88,78
        Alice Williams,92,94"""
        lines = test_csv.strip().split('\n')
        cls.csv_data = [row for row in csv.DictReader(lines, delimiter=',')]

        cls.test_config = Config()
        cls.test_config.path = "testpath.csv"
        cls.test_config.data_type = "csv"
        cls.test_config.entity_collection = "student"
        cls.test_config.base_field = "name"
        cls.test_config.computable_fields = ['english']

    def setUp(self):
        """
        Helps to initialize parser object and entity object for each method
        :return: None
        """
        self.test_config.entity_collection = "student"
        self.test_config.computable_fields = ['english']
        self.test_csv_parser = CsvParser(self.test_config)

    def test_parse(self):
        """
        Helps to test:-
        1) Normal test scenario
        2) Wrong Config Parse Scenario
        3) Wrong file Scenario
        4) General data not found scenario
        :return:
        """
        with mock.patch("data_transformer.csv_parser.CsvParser.__load_data__") as mock_load:
            mock_load.return_value = self.csv_data
            self.test_csv_parser.entityCollection = EC()
            entityCollection = self.test_csv_parser.parse()
        self.assertTrue(len(entityCollection.items)> 0, "Test Failed")

        # EMC - with wrong entity collection
        self.test_config.entity_collection = "Employee"
        with mock.patch("data_transformer.csv_parser.CsvParser.__load_data__") as mock_load:
            with self.assertRaises(Exception):
                self.test_csv_parser.parse()

        # Value error - with wrong pdf
        self.path = "test.pdf"
        self.test_config.entity_collection = "students"
        with mock.patch("data_transformer.csv_parser.CsvParser.__load_data__") as mock_load:
            with self.assertRaises(Exception):
                self.test_csv_parser.parse()

        self.test_config.entity_collection = "Employee"
        with self.assertRaises(Exception):
            self.test_csv_parser.parse()

    def test_Load_data_and_expression(self):
        """
        Helps to test
        1) Path not found scenario
        2) expression scenario
        :return:
        """
        with self.assertRaises(FileNotFoundError):
            self.test_csv_parser.__load_data__()

        self.test_config.computable_fields.append('english+science As Total')
        with mock.patch("data_transformer.csv_parser.CsvParser.__load_data__") as mock_load:
            mock_load.return_value = self.csv_data
            entity_collection = self.test_csv_parser.parse()
            self.assertEqual(len(entity_collection.fields), 2, "Test Failed")
            self.assertEqual(entity_collection.fields[1], "Total", "Test Failed")
            self.assertTrue(len(entity_collection.items)>0, "Test Failed")

    def tearDown(self):
        """
        Helps to delete test_parser
        :return: None
        """
        del self.test_csv_parser

    @classmethod
    def tearDownClass(cls):
        """
        Helps to delete test config object and csv data
        :return:
        """
        del cls.test_config
        del cls.csv_data