import pandas as pd
# DataSource APIs
from full_fred.fred import Fred
import yfinance as yf
from futu import *

class DataInterface:
    def fetch_data(self):
        pass
    
    def refine_data(self):
        # Default preprocessing steps
        # checks if ‘date’ or ‘Date’ is a column in self.data
        if any('date' in col.lower() for col in self.data.columns) or 'Date' in self.data.columns:
            # converts this column to datetime format, renames it to ‘Date’, and sets it as the index
            date_column = next(col for col in self.data.columns if 'date' in col.lower())
            self.data[date_column] = pd.to_datetime(self.data[date_column])
            self.data.rename(columns={date_column: 'Date'}, inplace=True)
            self.data = self.data.set_index('Date')
        elif isinstance(self.data.index, pd.DatetimeIndex):
            # renames the index to ‘Date’
            self.data.index.name = 'Date'
        else:
            print("No date column or datetime index found.")
        
        return self.data

class ExcelDataInterface(DataInterface):
    def __init__(self, file_path, sheet_name=0):
        self.file_path = file_path
        self.sheet_name = sheet_name

    def fetch_data(self):
        self.data = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        return self.refine_data()
    
    

class CSVDataInterface(DataInterface):
    def __init__(self, file_path):
        self.file_path = file_path

    def fetch_data(self):
        self.data = pd.read_csv(self.file_path)
        return self.refine_data()
    
class APIDataInterface(DataInterface):
    def fetch_data(self):
        pass

class FredDataInterface(APIDataInterface):
    def __init__(self, key_file, series_id):
        self.key_file = key_file
        self.series_id = series_id

    def fetch_data(self):
        fred = Fred(self.key_file)
        self.data = fred.get_series_df(self.series_id)
        return self.refine_data()
    
    def refine_data(self):
        # Preprocessing steps specific to FRED data
        self.data['date'] = pd.to_datetime(self.data['date'], format='%Y-%m-%d')
        self.data = self.data.set_index('date')
        self.data = self.data[self.data['value'] != '.']
        self.data['value'] = self.data['value'].astype(float)
        return self.data

class YFinanceDataInterface(APIDataInterface):
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date

    def fetch_data(self):
        self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        return self.refine_data()

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
        return self.refine_data()