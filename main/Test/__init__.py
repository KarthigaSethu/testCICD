###############################################################################################
# Over view on test directory files:
# 1. AbstractParserTest/AbstractParserTest -  has setUpCls, setUp, test method(s),  tearDown, tearDownCls
# 2. JsonParserTest/JsonParserTest - has setUpCls, setUp, test method(s),  tearDown, tearDownCls
# 3. XMLParserTest/XMLParserTest - has setUpCls, setUp, test method(s),  tearDown, tearDownCls
# 4. CSVParserTest./CSVParserTest - has setUpCls, setUp, test method(s),  tearDown, tearDownCls
# 5. DataManagerFactoryTest/DataManagerFactoryTest - has setUpCls, setUp, test method(s),  tearDown, tearDownCls
# 6. test_entity/TestEntity
# 7. test_entity/TestEntityCollection
# 8. my_suite() - Suite that co-ordinates all the test
#############################################################################################

import sys
sys.path.append(r'.\main')
sys.path.append(r'.\main\data_transformer')
sys.path.append(r'.\main\data_processor')

import unittest
from Test.AbstractParserTest import AbstractParserTest
from Test.JsonParserTest import JsonParserTest
from Test.XmlParserTest import XMLParserTest
from Test.CSVParserTest import CSVParserTest
from Test.DataManagerfactoryTest import DataManagerFactoryTest

'''
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
'''

'''
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
'''

'''
class XMLParserTest(unittest.TestCase):
    """
        Helps to test Abstract Parser Class
    """
    @classmethod
    def setUpClass(cls):
        """
        Helps to initialize the xml data and config for all method
        :return: None
        """
        test_xml = """<students>
        <student><name>John Doe</name><english>90</english><science>85</science></student>
        <student><name>Jane Smith</name><english>95</english><science>92</science></student>
        </students>"""
        cls.xml_data = ElementTree.fromstring(test_xml)

        cls.test_config = Config()
        cls.test_config.path = "testpath.xml"
        cls.test_config.data_type = "XML"
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
        self.test_xml_parser = XmlParser(self.test_config)
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
        with mock.patch("data_transformer.xml_parser.XmlParser.__load_data__") as mock_load:
            mock_load.return_value = self.xml_data
            self.test_xml_parser.entityCollection = EC()
            entityCollection = self.test_xml_parser.parse()
        self.assertTrue(len(entityCollection.items)> 0, "Test Failed")

        # EMC - with wrong entity collection
        self.test_config.entity_collection = "Employee"
        with mock.patch("data_transformer.xml_parser.XmlParser.__load_data__") as mock_load:
            with self.assertRaises(Exception):
                self.test_xml_parser.parse()

        # Value error - with wrong pdf
        self.path = "test.pdf"
        self.test_config.entity_collection = "students"
        with mock.patch("data_transformer.xml_parser.XmlParser.__load_data__") as mock_load:
            with self.assertRaises(Exception):
                self.test_xml_parser.parse()

        self.test_config.entity_collection = "Employee"
        with self.assertRaises(Exception):
            self.test_xml_parser.parse()

    def test_Load_data_and_expression(self):
        """
        Helsp to test
        1) Path not found scenario
        2) expression scenario
        :return:
        """
        with self.assertRaises(FileNotFoundError):
            self.test_xml_parser.__load_data__()

        self.test_config.computable_fields.append('english+science As Total')
        with mock.patch("data_transformer.xml_parser.XmlParser.__load_data__") as mock_load:
            mock_load.return_value = self.xml_data
            entity_collection = self.test_xml_parser.parse()
            self.assertEqual(len(entity_collection.fields), 2, "Test Failed")
            self.assertEqual(entity_collection.fields[1], "Total", "Test Failed")
            self.assertTrue(len(entity_collection.items)>0, "Test Failed")

    def tearDown(self):
        """
        Helps to delete test_parser
        :return: None
        """
        del self.test_xml_parser

    @classmethod
    def tearDownClass(cls):
        """
        Helps to delete test config object and xml data
        :return:
        """
        del cls.test_config
        del cls.xml_data
'''

'''
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
'''
'''
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
            self.assertTrue(entityCollection.items[0].field_value_pairs["Total"] > 0, "Test Failed")

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
'''
def my_suite():
    """
    Test Suite
    """
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    suite.addTest(unittest.makeSuite(AbstractParserTest))
    suite.addTest(unittest.makeSuite(JsonParserTest))
    suite.addTest(unittest.makeSuite(XMLParserTest))
    suite.addTest(unittest.makeSuite(CSVParserTest))
    suite.addTest(unittest.makeSuite(DataManagerFactoryTest))
    print(runner.run(suite))

if __name__ == '__main__':
    my_suite()






