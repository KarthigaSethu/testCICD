# Python Package Performance Analysis System

The Performance Analysis System is a flexible project developed for the Data 533 subject in the Mater of Data Science Program at UBC-O, to extract data from various sources such as CSV, JSON, and XML files to provide meaningful statistical metrics and plots to help customers from different fields understanding human performance.

# Contents

- `package-main` The main package facilitates the entire setup process, such as retrieving the configuration and prompting the user to choose the information to compute and/or visualize.
- `subpackage1-\main\data_processor` The main subpackage provides a structured and modular approach to handling datasets. It ensures that the necessary configuration is in place before performing data operations.
- `subpackage1-module1 \main\data_processor\configuration.py` This module provides a structured and modular approach to handling datasets. It ensures that the necessary configuration is in place before performing data operations.
- `subpackage1-module2 \main\data_processor\entity.py` This module processes entities and collections (e.g. student-students, employee-employees, etc.).
- `subpackage1-module3 \main\data_processor\performanceanalyzer.py` This module generates a summary of basic statistical metrics for the data from the entity collection. It also facilitates the creation of appropriate plots using the matplotlib and seaborn libraries.
- `subpackage2-\main\data_trasformer` It helps to invoke the respective parser depending on the data type of the input content.
- `subpackage2-module1 \main\data_trasformer\data_manager_factory.py` It helps to invoke the respective parser depending on the data type of the input content.
- `subpackage2-module2 \main\data_trasformer\abstract_parser.py` This class serves as a parent class which is inherited by all the other parsers classes.
- `subpackage2-module3 \main\data_trasformer\csv_parser.py` These classes are responsible for parsing data from various sources such as CSV files.
- `subpackage2-module4 \main\data_trasformer\xml_parser.py` These classes are responsible for parsing data from various sources such as XML files.
- `subpackage2-module4 \main\data_trasformer\json_parser.py` These classes are responsible for parsing data from various sources such as JSON files.
