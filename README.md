# TechViz Documentation

TechViz is a sophisticated financial software solution that offers backtesting capabilities and dynamic data visualization. It is engineered to support two programming pipelines, one in Python and the other in C++, catering to the diverse needs of financial professionals. This tool is designed to empower users with robust analytical tools, enhancing their ability to make data-driven decisions in the financial sector.

## Overview

TechViz stands as a formidable instrument in the realm of financial analysis, offering an immersive interface for backtesting and data visualization. It leverages the power and flexibility of widely-used Python libraries, ensuring robust performance and seamless customization. Furthermore, TechViz is built on the principles of Object-Oriented Programming (OOP) and modularity, enhancing its scalability and maintainability, thereby making it an indispensable asset for financial professionals.

## Data Interfaces
This project provides various data interfaces to fetch data from different sources, such as **FRED**, **Yahoo Finance**, **Excel** and **CSV** files. They are all subclasses of the abstract base class DataInterface, which defines some common methods such as `fetch_data`, `refine_data`, etc. Each data interface has its own parameters and attributes that are specific to the data source.

## Data Visualizer Class
The project also defines a class for visualizing the data in a web app. The class is called `DataVisualizer` and it takes a `DataInterface` object as an argument, along with some optional parameters such as the title, the x-axis title, and the colors. The class has a method called `visualize_data` that creates a Dash app with a dropdown menu and a graph. The dropdown menu allows the user to select a column from the data frame, and the graph shows the selected column as a line chart with hover labels and spikes. The graph is updated dynamically based on the user’s selection.

### How to Use
#### FRED Data Interface
The `FredDataInterface` class allows you to fetch data from the FRED API. You need to provide a valid API key and a series ID to create an instance of this class. You can also specify the start date and end date of the data, as well as the frequency and aggregation method. The `fetch_data` method will return a dataframe with the date as the index and the series value as the column.

Example: Fetching the data of `S&P 500`
```
#? Create an instance of FredDataInterface with the series ID of target data
fred_interface = FredDataInterface('SP500')

#? Create an instance of DataVisualizer with the FredDataInterface instance
data_visualizer = DataVisualizer(fred_interface, title='TechViz Visualizer', xaxis_title='Date')

#? Visualize the data from the FRED API
data_visualizer.visualize_data()
```

Output:
```
            SP500
Date	
2018-11-13	2722.18
2018-11-14	2701.58
2018-11-15	2730.20
2018-11-16	2736.27
2018-11-19	2690.73
...	...
2023-11-07	4378.38
2023-11-08	4382.78
2023-11-09	4347.35
2023-11-10	4415.24
2023-11-13	4411.55

[1258 rows × 1 columns]

![alt text](![alt text](https://github.com/lauchunhin/TradeViz/blob/dev/Demo/sp500_fred_demonstration.png))
```

#### Yahoo Finance Data Interface
The `YFinanceDataInterface` class allows you to fetch data from Yahoo Finance. You need to provide a ticker symbol, a start date, and an end date to create an instance of this class. You can also specify the interval of the data, such as daily, weekly, or monthly. The `fetch_data` method will return a dataframe with the date as the index and the open, high, low, close, adjusted close, and volume as the columns.

Example: Fetching the data of `S&P 500`
```
yfinance_interface = YFinanceDataInterface('^GSPC', '2023-01-01', '2023-08-01')
yfinance_data = yfinance_interface.fetch_data()
display(yfinance_data)
```

#### Excel Data Interface
The `ExcelDataInterface` class allows you to fetch data from an Excel file. You need to provide the file path of the Excel file to create an instance of this class. You can also specify the sheet name or index of the sheet that you want to read from the file. The `fetch_data` method will return a dataframe with the data from the sheet.

Example: Fetching the data of `CPIAUCSL.xls`
```
# create an instance of ExcelDataInterface with the file path
excel_interface = ExcelDataInterface('PATH_TO_CPIAUCSL.xls')
excel_data = excel_interface.fetch_data()
display(excel_data)
```

## Setting Up API Key Securely
This guide will walk you through the process of setting up your FRED API key securely using the `zsh` shell as an example.

#### Step 1: Open the Startup Script
Open your `zsh` shell’s startup script with a text editor. The startup script for `zsh` is typically `~/.zshrc`. You can open it with the following command:
```
nano ~/.zshrc
```
#### Step 2: Add the Export Command
Scroll to the bottom of the file and add the line that exports your FRED API key. It should look something like this:
```
export FRED_API_KEY="your_api_key"
```
Replace `"your_api_key"` with your actual FRED API key.

#### Step 3: Save and Exit
Save the file and exit the editor. If you’re using `nano`, you can do this by pressing `Ctrl+X`, then `Y` to confirm that you want to save the changes, and then Enter to confirm the file name.

#### Step 4: Source the Startup File
To make sure your changes take effect, you can source the startup file with the following command:
```
source ~/.zshrc
```
Now, the FRED API key you added should be available in all new shell sessions. You can check this by opening a new terminal window and typing `echo $FRED_API_KEY`, which should display your FRED API key.

## Support
- Excel files `.xls`
- CSV files `.csv`
- Yahoo! Finance API `yfinance`(https://github.com/ranaroussi/yfinance)
- Federal Reserve Economic Data API `full_fred`(https://fred.stlouisfed.org/)
- Futu API `futu-api`(https://openapi.futunn.com/futu-api-doc/en/)
