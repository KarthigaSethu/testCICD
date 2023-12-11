import os
import csv
from data_transformer.abstract_parser import Parser
from data_processor.entity import EntityCollection as EC
from data_transformer.custom_exception import EntityCollectionMismatch as EMC

class CsvParser(Parser):
    """
        This is an important class variable that distinguishes it from other child parsers.
        It is used by Data Manager factory for the parser's it's type
    """
    type = "CSV"
    def __init__(self, config):
        """
        Helps to initialize
        :param config: Config class object
        """
        super().__init__(self)
        self.config = config
        self.entityCollection = EC()

    def parse(self):
        """
         This method helps to:-
         1. validate the file
         2. convert CSV to entity collection
         2.1. handles normal fields separately
         2.2. handles expression field separately

         :return(EntityCollection): Helps to return Entity Collection
         """
        data = self.__validate__()
        fields = self.get_computable_fields()
        parsed_expressions = self.get_parsed_expression()
        self.entityCollection.fields = list(fields) + [expression[3] for expression in self.get_parsed_expression()]
        for row in data:
            entity_object = self.entityCollection.add_entity(row[self.config.base_field])
            self.__handle_normal_fields__(row, fields, entity_object)
            self.__handle_expression_fields__(row, parsed_expressions, entity_object)
        return self.entityCollection

    def __handle_normal_fields__(self, row, fields, entity_object):
        """
        Loops through each row in csv and add its field and value in entity

        :param row (csv row): csv row
        :param fields(List of String): Simple fields
        :param entity_object(Entity): Entity object
        :return: None
        """
        for field in fields:
            entity_object.add(field, row[field])

    def __handle_expression_fields__(self, row, parsed_expressions, entity_object):
        """
        This method helps to handle expression fields like "A/B as div"

        :param row (csv row): this is one csv row
        :param parsed_expressions (List of string): parsed list of expression
        :param entity_object (Entity): Entity object
        :return: None
        """
        for expression in parsed_expressions:
            self.evaluate_expression(row[expression[0]], row[expression[1]],
                                     expression[3], expression[4], entity_object)

    def __validate__(self):
        """
        Helps to do simple validations that checks the file's presence, type and content
        :return: data
        """
        file_Name = os.path.basename(self.config.path)
        if ".csv" not in file_Name:
            raise ValueError("CSV PARSER: Incorrect Parser")
        try:
            data = self.__load_data__()
            if len(data) == 0:
                raise EMC("CSV PARSER", self.config.path)
            return data
        except Exception:
            raise Exception("CSV PARSER: Invalid CSV")

    def __load_data__(self):
        """
        Helps to load the file
        :return: data
        """
        try:
            with open(self.config.path, 'r') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader, None)
                return [dict(zip(header, row)) for row in csv_reader]
        except FileNotFoundError:
            raise FileNotFoundError("CSV Parser: File not found in path {}".format(self.config.path))
        except Exception as e:
            raise Exception(e)
