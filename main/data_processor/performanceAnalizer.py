from datetime import datetime
import matplotlib.pyplot as plt
import pandas.core.frame
from matplotlib.backends.backend_pdf import PdfPages
from array import array
from tabulate import tabulate
import pandas as pd
import numpy as np

class Performance_Analyzer:
    """
    Performance_Analyzer class helps to provide summary on statistics metrics and visualize the charts.
    
    It generates the following visualizations and call basic metrics to display in console and export in a PDF file the following:
    1. Bar plot
    2. Line chart
    3. Scatter  plot
    4. Box plot
    5. Metrics like mean, median, mode, count, max, min
    
    Parameters:
        config: Configuration
            An object from the Configuration class containing configuration settings.
    """
    def __init__(self, config):
        """
        Initializes the Performance_Analyzer.

        Parameters:
            config: Configuration
                An object from the Configuration class containing configuration settings.
        """
        self.config = config
        
    def __prepare_axis_components__(self, entity_collection, field):
        """
        Prepares data for plotting by extracting x and y axis components.

        Parameters:
            entity_collection: EntityCollection
                A collection of entities with data to be analyzed.
            field: str
                The field for which the data is being prepared.

        Returns:
            list, list
                Returns chart_x_axis and chart_y_axis.
        """
        chart_x_axis = []
        chart_y_axis = []
        for entity in entity_collection.items:
            chart_x_axis.append(entity.entity_id)
            if field in entity.field_value_pairs:
                chart_y_axis.append(entity.field_value_pairs[field])
            else:
                chart_y_axis.append(0)

        return chart_x_axis, chart_y_axis
      
    def __generate_barplot__(self, x, y, ylabel, axs):
        """
        Generates a bar plot.

        Parameters:
            x: list
                X-axis data.
            y: list
                Y-axis data.
            ylabel: list
                Label from Y-axis data.
            axs: AxesSubplot
                The subplot where the barplot will be plotted.
        """
        axs[1, 0].bar(x, y)
        axs[1, 0].set_title(f'{ylabel} Bar Chart'.upper())

    def __generate_line_chart__(self, x, y, ylabel, axs):
        """
        Generates a line chart.

        Parameters:
            x: list
                X-axis data.
            y: list
                Y-axis data.
            ylabel: list
                Label from Y-axis data.
            axs: AxesSubplot
                The subplot where the line chart will be plotted.
        """
        axs[2, 0].plot(x, y, marker='o')
        axs[2, 0].set_title(f'{ylabel} Line Chart'.upper())

    def __generate_boxplot__(self, y, ylabel,axs):
        """
        Generates a box plot.

        Parameters:
            y: list
                Y-axis data.
            ylabel: list
                Label from Y-axis data.
            axs: AxesSubplot
                The subplot where the boxplot will be plotted.
        """
        axs[2, 1].boxplot(y, vert=False)
        axs[2, 1].set_title(f'{ylabel} Boxplot'.upper())

    def __generate_scatter_plot__(self, x, y, ylabel, axs):
        """
        Generates a scatter plot.

        Parameters:
            x: list
                X-axis data.
            y: list
                Y-axis data.
            ylabel: list
                Label from Y-axis data.
            axs: AxesSubplot
                The subplot where the scatter plot will be plotted.
        """
        axs[1, 1].scatter(x, y)
        axs[1, 1].set_title(f'{ylabel} Scatter Plot'.upper())

    def __generate_statistical_table__(self, entity_collection, field, axs):
        """
        Generates a summary table filled with the statistical metrics for every field (column).

        Parameters:
            entity_collection: 
                Object of the class entity.
            field:
                The field that will be used to compute the statistical metrics.
            axs: AxesSubplot
                The subplot where the summary table will be plotted.
        """
        axs[0, 0].axis('off')  # Hide axes for the table
        metrics_labels = ['MEAN', 'MODE', 'MEDIAN', 'MIN', 'MAX', 'COUNT']
        summary_data = [entity_collection.compute_mean(field), entity_collection.compute_mode(field),
                        entity_collection.compute_median(field), entity_collection.compute_min(field),
                        entity_collection.compute_max(field), entity_collection.compute_count(field)]
        summary_data = np.array([summary_data])
        df = pd.DataFrame(summary_data, columns=metrics_labels)
        summary_table = axs[0, 0].table(cellText=df.values,
                                          colLabels=metrics_labels,
                                          cellLoc='center',
                                          loc='center',
                                          cellColours=[['#F0F0F0'] * len(metrics_labels)],
                                          colWidths=[0.2] * len(metrics_labels),
                                          bbox=[0, 0, 1, 1])

    def display(self, entity_collection):
        """
        Method that display the summary table and plots for the entity collection.

        Parameters:
            entity_collection: 
                Object of the class entity.
        """
        fields = entity_collection.fields
        for column in fields:
            X,Y = self.__prepare_axis_components__(entity_collection,column)
            fig, axs = plt.subplots(3, 2, figsize=(14, 12))
            fig.suptitle(f'{column} Analysis'.upper(), fontsize=16)
            self.__generate_statistical_table__(entity_collection,column,axs)
            axs[0, 1].axis('off')
            self.__generate_barplot__(X, Y, column, axs)
            self.__generate_scatter_plot__(X, Y, column, axs)
            self.__generate_line_chart__(X, Y, column, axs)
            self.__generate_boxplot__(Y, column, axs)
            plt.tight_layout()
            plt.show()
            plt.close()

    def export(self, entity_collection):
        """
        Method to export the summary table and plots for the entity collection in a PDF file.

        Parameters:
            entity_collection: 
                Object of the class entity.
        """
        fields = entity_collection.fields
        pdf_filename = "Summary.pdf"
        with PdfPages(pdf_filename) as pdf:
            for column in fields:
                X,Y = self.__prepare_axis_components__(entity_collection,column)
                fig, axs = plt.subplots(3, 2, figsize=(14, 12))
                fig.suptitle(f'{column} Analysis'.upper(), fontsize=16)
                self.__generate_statistical_table__(entity_collection,column,axs)
                axs[0, 1].axis('off')
                self.__generate_barplot__(X, Y, column, axs)
                self.__generate_scatter_plot__(X, Y, column, axs)
                self.__generate_line_chart__(X, Y, column, axs)
                self.__generate_boxplot__(Y, column, axs)
                pdf.savefig()
                plt.tight_layout()
                plt.close()
