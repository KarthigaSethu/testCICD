import os

class EmptyData(Exception):
    """
    Helps to raise exception when parsed data is empty
    """
    def __init__(self, path):
        """
        Helps to initialize the data
        :param path: file path
        """
        self.path = path
    def __str__(self):
        """
        Helps to return output error in a custom format
        :return: Error
        """
        return "Parsed data is empty. Please check the data in path {}".format(self.path)

class EntityCollectionMismatch(Exception):
    """
    Helps to raise exception when data_collection config property doesn't match with data in the file
    """
    def __init__(self, parser_name, path):
        """
        Helps to initialize
        :param parser_name: name of the parser
        :param path: path
        """
        self.parser_name = parser_name
        self.path = path
    def __str__(self):
        """
            Helps to return output error in a custom format
            :return: Error
        """
        config_path = os.path.join(os.getcwd(), "config.json")
        return "{}:Please Check data at path {} and config at the path {}".format(self.parser_name, self.path, config_path)

class UnsupportedDataType(Exception):
    """
    Helps to raise exception when data_collection config property doesn't match with data in the file
    """
    def __init__(self,file_extension):
        """
        Helps to initialize
        :param parser_name: name of the parser
        :param path: path
        """
        self.file_extension = file_extension
    def __str__(self):
        """
            Helps to return output error in a custom format
            :return: Error
        """
        config_path = os.path.join(os.getcwd(), "config.json")
        return "Unsupported type : {} is found in config : {}".format(self.file_extension, config_path)