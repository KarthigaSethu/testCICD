import re

class Parser:
    """
    Parser class is a parent class which is inherited by all the other parsers classes.
    The main purpose of this parser class is to parse user expression.
    For Example:-
    If user gives "English + Math As Total" as an expression,
    1. this class helps to split and store parsed result
    2. add score of English & Math
    3. Store it as 'Total' in entity subject

    It's child classes are responsible of parsing different data into entity collection
    """
    def __init__(self,config):
        """
        Helps to initialize
        parameter:
        - config(Config): Config is stored as param in parser class
        """
        self.config = config
        self.__parsed_expression_collection__ =[]
    
    def parse(self):
        """
        This class doesn't have any definition for parsing.
        But it is used for inheritence purpose in child classes
        :return: None
        """
        pass
    
    def get_computable_fields(self):
        """
        Helps to read an expression and parse into simple individual components.
        Example:
        1. In case of expression fields, For Employee Domain if expression is 'Total_Task*Criticality As Score'
        then this method converts this expression into ['Total_Task', 'Criticality', 'As' , '*', 'Score']
        and stores it into __parsed_expression_collection__.

        2. The simple fields are just added into list and returned.
        return:
        - fields(List of String) : List of fields(without any expression)

        Limitations:
        - Accepts only 2 operands in expression
        """
        fields = set()
        for field in self.config.computable_fields:
            if "+" in field:
                self.__parse_expression__("+", field)
            elif "-" in field:
                self.__parse_expression__("-", field)
            elif "*" in field:
                self.__parse_expression__("*", field)
            elif "/" in field:
                self.__parse_expression__("/", field)
            else:
                fields.add(field)
        return fields
      
    def get_parsed_expression(self):
        """
        Helps to return this private field, which contains parsed expression

        :return: __parsed_expression_collection__
        """
        return self.__parsed_expression_collection__
    
    def evaluate_expression(self,first_term, second_term, alias, operator, entity_obj):
        """
         Converts first and second operand into numbers and stores the
         result of the expression in entity object

        :param first_term: (int) - first operand
        :param second_term: (int) - second operand
        :param alias: (string) - alias name for the result of expression
        :param operator: (string/char) - mathematical symbols
        :param entity_obj: (Entity) - Object of Entity
        :return: None
        """
        first_term, second_term = self.__validate_and_convert_operand__(first_term, second_term)
        if "+" == operator:
            entity_obj.add(alias, first_term+second_term)
        elif "-" == operator:
            entity_obj.add(alias, first_term - second_term)
        elif "*" == operator:
            entity_obj.add(alias, first_term * second_term)
        elif "/" == operator:
            entity_obj.add(alias, first_term / second_term)

    def __parse_expression__(self,dynamic_splitter, field):
        """
        Helps to parse result with an exporession

        :param dynamic_splitter(string/char): stores mathematical symbols like +,-,/,*
        :param field(string): expression Eg:- A+B AS C
        :return(list): parsed result in list Eg:- [A,B,AS,C]
        """
        pattern = r'\s*(?:[{}\s]|as)\s*'.format(dynamic_splitter)
        matches = re.split(pattern, field)
        self.__store_parsed_expression__(matches,dynamic_splitter)
        
    def __store_parsed_expression__(self, expression_collection, function):
        """
        This a simple helper class that stores the mathematical operands into existing expression list
        and store it in expression_collection.

        Adding operand into the list is useful when comes to calculating it.
        Also, this is made as a separate method for readability.
        As in previous methods adding + to match might confuse the readers.

        :param expression_collection(list of string): [A,B,As,C]
        :param function(string): +
        :return: None
        """
        expression_collection.append(function)
        self.__parsed_expression_collection__.append(expression_collection)  
        
    def __validate_and_convert_operand__(self, first_term, second_term):
        """
        Helps to validate and convert the operands into numbers
        :param first_term (string): first operand
        :param second_term (string): second operand
        :return (int, int): first operand, second operand both as number
        """
        try:
            first_term = int(first_term)
            second_term = int(second_term)
            return first_term, second_term
        except ValueError:
            raise ValueError("PARSER: The operands are not numeric")