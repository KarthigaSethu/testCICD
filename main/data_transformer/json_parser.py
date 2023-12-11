import os
import json
from data_transformer.abstract_parser import Parser
from data_processor.entity import EntityCollection as EC
from data_transformer.custom_exception import EntityCollectionMismatch as EMC


class JsonParser(Parser):
    """
    This is an important class variable that distinguishes it from other child parsers.
    It is used by Data Manager factory for the parser's it's type
    """
    type = "JSON"

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
        2. convert json to entity collection
        2.1. handles normal fields separately
        2.2. handles expression field separately

        :return(EntityCollection): Helps to return Entity Collection
        """
        data = self.__validate__()
        if self.config.entity_collection in data:
            entities = data[self.config.entity_collection]
            fields = self.get_computable_fields()
            parsed_expressions = self.get_parsed_expression()
            self.entityCollection.fields = list(fields) + [expression[3] for expression in self.get_parsed_expression()]
            for entity in entities:
                entity_object = self.entityCollection.add_entity(entity.get(self.config.base_field))
                self.__handle_normal_fields__(entity, fields, entity_object)
                self.__handle_expression_fields__(entity, parsed_expressions, entity_object)
        return self.entityCollection

    def __handle_normal_fields__(self, entity, fields, entity_object):
        """
        Loops through each field in json and add its field and value in entity

        :param entity (json block): this is one json block
        :param fields(List of String): Simple fields
        :param entity_object(Entity): Entity object
        :return: None
        """
        for field in fields:
            entity_object.add(field, entity.get(field))

    def __handle_expression_fields__(self, entity, parsed_expressions, entity_object):
        """
        This method helps to handle expression fields like "A/B as div"

        :param entity (json block): this is one json block
        :param parsed_expressions (List of string): parsed list of expression
        :param entity_object (Entity): Entity object
        :return: None
        """
        for expression in parsed_expressions:
            self.evaluate_expression(entity.get(expression[0]), entity.get(expression[1]),
                                     expression[3], expression[4], entity_object)

    def __validate__(self):
        """
        Helps to do simple validations that checks the file's presence, type and content
        :return: data
        """
        file_Name = os.path.basename(self.config.path)
        if ".json" not in file_Name:
            raise ValueError("JSON PARSER: Incorrect Parser")
        try:
            data = self.__load_data__()
            if self.config.entity_collection not in data:
                raise EMC("JSON PARSER", self.config.path)
            return data
        except Exception:
            raise Exception("JSON PARSER: Invalid Json")

    def __load_data__(self):
        """
        Helps to load the file
        :return: data
        """
        try:
            with open(self.config.path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError("JSON Parser: File not found in path {}".format(self.config.path))
        except Exception as e:
            raise Exception(e)




