# TechViz Documentation

TechViz is a sophisticated financial software solution that offers backtesting capabilities and dynamic data visualization. It is engineered to support two programming pipelines, one in Python and the other in C++, catering to the diverse needs of financial professionals. This tool is designed to empower users with robust analytical tools, enhancing their ability to make data-driven decisions in the financial sector.

## Overview

TechViz stands as a formidable instrument in the realm of financial analysis, offering an immersive interface for backtesting and data visualization. It leverages the power and flexibility of widely-used Python libraries, ensuring robust performance and seamless customization. Furthermore, TechViz is built on the principles of Object-Oriented Programming (OOP) and modularity, enhancing its scalability and maintainability, thereby making it an indispensable asset for financial professionals.

## Data Interfaces
This project provides various data interfaces to fetch data from different sources, such as **FRED**, **Yahoo Finance**, **Excel** and **CSV** files. The data interfaces are subclasses of the DataInterface abstract class, which defines a common method called `fetch_data` that returns a pandas dataframe and a common method `refine_data` that preprocesses the data. Each data interface has its own parameters and attributes that are specific to the data source.

#### FRED Data Interface
The `FredDataInterface` class allows you to fetch data from the FRED API. You need to provide a valid API key and a series ID to create an instance of this class. You can also specify the start date and end date of the data, as well as the frequency and aggregation method. The `fetch_data` method will return a dataframe with the date as the index and the series value as the column.

Example: Fetching the data of `10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity`
```
# Create an instance of FredDataInterface with the API key file and the corresponding series ID for the Treasury Constant Maturity
fred_interface = FredDataInterface('T10Y2Y')
# Fetch the data from FRED
fred_data = fred_interface.fetch_data()
# Display the dataframe
display(fred_data)
```

Output:
```
            T10Y2Y
date              
2000-01-03    1.16
2000-01-04    1.12
2000-01-05    1.14
2000-01-06    1.15
2000-01-07    1.17
...            ...
2023-08-25    1.32
2023-08-28    1.31
2023-08-29    1.30
2023-08-30    1.29
2023-08-31    1.28

[5838 rows x 1 columns]
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
