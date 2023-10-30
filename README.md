# TechViz Documentation

TechViz is a financial tool designed to provide backtesting functions and interactive data visualization. It is implemented in Python and leverages libraries such as pandas, numpy, plotly, and dash.

## Overview

The main script of TechViz is `visulisation.py`, which serves as the backbone of the application. The script performs several key tasks:

1. **Data Import and Cleaning**: The script imports an Excel file named `trade_data.xlsx` and converts it into a pandas DataFrame. It then performs data cleaning and transformation tasks, such as removing null values, calculating returns, and reshaping the data.

2. **Color and Metric Definitions**: The script defines a set of colors and metrics that are used in the subsequent charting process.

3. **Dash Application Creation**: A Dash application named `app` is created with some external stylesheets set up.

4. **Layout Elements**: Various layout elements are added to the Dash application, including dropdown menus, sliders, and charts.

5. **Callback Functions**: Callback functions are added to the Dash application to connect the layout elements with an `update_graph` function. This function updates the charts based on user selections.

6. **Application Execution**: Finally, the Dash application is run and the results are displayed on a local server.

## Usage

To use TechViz, simply run the `visulisation.py` script. This will start the Dash application and open it in your default web browser. From there, you can interact with the various layout elements to explore your data and perform backtesting operations.

## Conclusion

TechViz is a powerful tool for financial analysis, providing users with an interactive platform for backtesting and data visualization. Its use of popular Python libraries ensures robust performance and easy customization.
