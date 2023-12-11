from data_transformer.json_parser import JsonParser
from data_transformer.xml_parser import XmlParser
from data_transformer.csv_parser import CsvParser
from data_transformer.custom_exception import EmptyData as ED

class DataManagerFactory:
    """ Helps to call respective  parser depending on data type of input content
    Process:  DataManagerFactory gets  data_type from config and check against the types of registered parsers.
    Then, calls matching parser to parse the data
    """
    def __init__(self, config):
        """ Helps to initialize.
        1. there is low chance that user will define their own parser.
        Even, if they do, they have to meet the criteria of having a class type.
        So to avoid this issue, but default user can't add parser externally.
        2. Config during initialization is allowed.
        3 Then __register__() method is called to register the valid parsers in current system.
        """
        self.parsers = []
        self.config = config
        self.__register__()

    def __register__(self):
        """ Helps to register the parsers"""
        self.parsers.append(JsonParser)
        self.parsers.append(XmlParser)
        self.parsers.append(CsvParser)

    def call_parser(self):
        """ Responsible for calling the respective parser by analysing the type of each registered parsers against config
        If the returned data is empty, throws error
        If not, then calls Performance Summarizer
        """
        try:
            for parser in self.parsers:
                if parser.type == self.config.data_type:
                    respective_parser = parser(self.config)
                    entityCollection = respective_parser.parse()
                    if self.__is_empty__(entityCollection):
                        raise ED(self.config.path)
                    return entityCollection
        except Exception as e:
            raise Exception(e)

    def __is_empty__(self, entityCollection):
        """
        This method helps to validate if the data is empty or not
        The data is considered empty if:-
            1. there is no entities
            2. there is no field-value pairs for all entities in collection

        parameter:
         - entityCollection(EntityCollection)

        return:
         - True or False
         """
        if entityCollection.items.count == 0:
            return True
        for entity in entityCollection.items:
            if len(entity.field_value_pairs) != 0:
                return False
        return True
