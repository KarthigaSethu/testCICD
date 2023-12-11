import unittest
from data_transformer.abstract_parser import Parser
from data_processor.configuration import Config
from data_processor.entity import Entity
from data_processor.entity import EntityCollection as EC

class AbstractParserTest(unittest.TestCase):
    """
    Helps to test Abstract Parser Class
    """
    @classmethod
    def setUpClass(cls):
        """
        Helps to initialize the config for all method
        :return: None
        """
        cls.test_config = Config()
        cls.test_config.path = "testpath.json"
        cls.test_config.data_type = "JSON"
        cls.test_config.entity_collection = "Students"
        cls.test_config.base_field = "Name"
        cls.test_config.computable_fields = ['Science','Science+Math','Science*Math','Science/Math','Science-Math']

    def setUp(self):
        """
        Helps to initialize parser object and entity object for each method
        :return: None
        """
        self.test_parser = Parser(self.test_config)
        self.test_entity = Entity("test")

    def test_expression_parsing_fields(self):
        """
        Helps to test: -
        1. get_computable_fields method
        2. get_parsed_expression method
        3. __validate_and_convert_operand__ method indirectly
        :return: None
        """
        fields = self.test_parser.get_computable_fields()
        self.assertEqual(len(fields), 1, "Test Failed")

        parsed_expression_list = self.test_parser.get_parsed_expression()
        self.assertEqual(len(parsed_expression_list), 4, "Test Failed")
        self.assertEqual(parsed_expression_list[0][2],"+","Test Failed")

        self.test_parser.parse()
        with self.assertRaises(ValueError):
            self.test_parser.evaluate_expression("five", "ten", "Div", "/", self.test_entity)

    def test_evaluating_fields(self):
        """
        Helps to test evaluate_expression methods with different expressions
        :return: None
        """
        self.test_parser.evaluate_expression("5", "10", "Total", "+", self.test_entity)
        self.test_parser.evaluate_expression("5", "10", "Product", "*", self.test_entity)
        self.test_parser.evaluate_expression("5", "10", "Diff", "-", self.test_entity)
        self.test_parser.evaluate_expression("5", "10", "Div", "/", self.test_entity)

        self.assertEqual(self.test_entity.field_value_pairs.get("Total"), 15,"Test Failed")
        self.assertEqual(self.test_entity.field_value_pairs.get("Product"), 50,"Test Failed")
        self.assertEqual(self.test_entity.field_value_pairs.get("Diff"), -5, "Test Failed")
        self.assertEqual(self.test_entity.field_value_pairs.get("Div"), 0.5, "Test Failed")

    def tearDown(self):
        """
        Helps to delete test_entity and test_parser
        :return: None
        """
        del self.test_entity
        del self.test_parser

    @classmethod
    def tearDownClass(cls):
        """
        Helps to delete test config object
        :return:
        """
        del cls.test_config