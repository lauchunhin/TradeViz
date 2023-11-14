import pandas as pd
import numpy as np
#* Import data source APIs
from full_fred.fred import Fred
import yfinance as yf
from futu import *
#* Import dotenv for loading API keys from .env file
from dotenv import load_dotenv
import os
import requests

#* Load environment variables from .env file
load_dotenv()

#* DataInterface as the base class for data interfaces
class DataInterface:
    #? Initialize the dta interface with an optional index column
    def __init__(self, index_column=None):
        self.index_column = index_column

    def fetch_data(self):
        pass
    
    #? Method to refine data
    def refine_data(self):
        try:
            if self.index_column:
                self.set_index()
            self.convert_non_numeric_columns_to_numeric()
            self.keep_only_numeric_columns()
        except Exception as e:
            raise RuntimeError(f"An error occurred during data refinement: {e}")

        return self.data

    def set_index(self):
            if self.index_column in self.data.columns:
                self.data[self.index_column] = pd.to_datetime(self.data[self.index_column])
                self.data.rename(columns={self.index_column: 'Date'}, inplace=True)
                self.data = self.data.set_index('Date')
            else:
                raise ValueError(f"No column named {self.index_column} found.")

    def convert_non_numeric_columns_to_numeric(self):
        for col in self.data.columns:
            if self.data[col].dtype == 'object':
                self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
        self.data.dropna(inplace=True)

    def keep_only_numeric_columns(self):
            self.data = self.data.select_dtypes(include=[np.number])

#? Define the class for Excel data interfaces
class ExcelDataInterface(DataInterface):
    def __init__(self, file_path, index_column=None):
        super().__init__(index_column)
        self.file_path = file_path

    def fetch_data(self):
        self.data = pd.read_excel(self.file_path)
        return self.refine_data()

#? Define the class for CSV data interfaces
class CSVDataInterface(DataInterface):
    def __init__(self, file_path, index_column=None):
        super().__init__(index_column)
        self.file_path = file_path

    def fetch_data(self):
        self.data = pd.read_csv(self.file_path)
        return self.refine_data()

#* APIDataInterface as the base class for API data interfaces
class APIDataInterface(DataInterface):
    def fetch_data(self):
        pass

#? Define the class for FRED data interfaces - Federal Reserve Economic Data
class FredDataInterface(APIDataInterface):
    def __init__(self, series_id):
        self.series_id = series_id # The series ID of the FRED data
        
    def fetch_data(self):
        try:
            fred = Fred()
            self.data = fred.get_series_df(self.series_id)
        except requests.exceptions.RequestException as e:
            print(f"Failed to send request to FRED API: {e}")
        else:
            return self.refine_data()
    
    def refine_data(self):
        # Preprocessing steps specific to FRED data
        try:
            # code that may raise ValueError or TypeError
            self.data['date'] = pd.to_datetime(self.data['date'], format='%Y-%m-%d')
            self.data = self.data.set_index('date')
            self.data = self.data[self.data['value'] != '.']
            self.convert_non_numeric_columns_to_numeric()
            self.keep_only_numeric_columns()

        except ValueError as e:
            # code to handle ValueError
            print(f"An error occurred while converting data types: {e}")
        except TypeError as e:
            # code to handle TypeError
            print(f"An error occurred while indexing or slicing data: {e}")
        
        return self.data


#? Define the class for YFinance data interfaces - Yahoo Finance
class YFinanceDataInterface(APIDataInterface):
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date

    def fetch_data(self):
        self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        return self.data

#? Define the class for Futu data interfaces - Futu
class FutuDataInterface(APIDataInterface):
    def __init__(self, stock_code, start_date, end_date, page_limit):
        self.stock_code = stock_code
        self.start_date = start_date
        self.end_date = end_date
        self.page_limit = page_limit

    def fetch_data(self):
        quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
        page_req_key = None
        all_data = []

        while True:
            ret, data, page_req_key = quote_ctx.request_history_kline(
                self.stock_code,
                start=self.start_date,
                end=self.end_date,
                max_count=self.page_limit,
                page_req_key=page_req_key
            )

            if ret == RET_OK:
                all_data.append(data)
            else:
                print(f"Error occurred while fetching data: {data}")
                break

            if page_req_key is None:
                break

        quote_ctx.close()
        self.data = pd.concat(all_data)
        return self.data()
