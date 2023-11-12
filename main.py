# Import the necessary classes from data.py and visualization.py
from data import ExcelDataInterface, CSVDataInterface, FredDataInterface, YFinanceDataInterface, FutuDataInterface
from visualization import DataVisualizer

def main():
    #* Handling csv files
    #? Create an instance of CSVDataInterface with the file path and the index column
    csv_interface = CSVDataInterface('csv_file_path', index_column='DATE')

    #? Create an instance of DataVisualizer with the CSVDataInterface instance
    data_visualizer = DataVisualizer(csv_interface, title='Title', xaxis_title='Date')

    #? Visualize the data from the CSV file
    data_visualizer.visualize_data()

    #* Handling excel files
    excel_interface = ExcelDataInterface('/Users/ICSA.xls', index_column='date')
    data_visualizer = DataVisualizer(excel_interface, title='Title', xaxis_title='Date')
    data_visualizer.visualize_data()

    #* Handling FRED data
    #? Create an instance of FredDataInterface with the series ID for the Initial Claims data
    fred_interface = FredDataInterface('ICSA')

    #? Create an instance of DataVisualizer with the FredDataInterface instance
    data_visualizer = DataVisualizer(fred_interface, title='Title', xaxis_title='Date')

    #? Visualize the data from the FRED API
    data_visualizer.visualize_data()

    #* Handling Yfinance data
    yfinance_interface = YFinanceDataInterface('AAPL', '2020-01-01', '2020-12-31')
    data_visualizer = DataVisualizer(yfinance_interface, title='Title', xaxis_title='Date')
    data_visualizer.visualize_data()

if __name__ == "__main__":
    main()
