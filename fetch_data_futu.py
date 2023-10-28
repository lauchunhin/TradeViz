from futu import *

def fetch_kline_data(stock_code, start_date, end_date, page_limit):
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    page_req_key = None
    all_data = []

    while True:
        ret, data, page_req_key = quote_ctx.request_history_kline(
            stock_code, 
            start=start_date, 
            end=end_date, 
            max_count=page_limit,
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
    return pd.concat(all_data)

if __name__ == "__main__":
    data = fetch_kline_data('HK.00700', '2019-09-11', '2019-09-18', 5)
    print("Data loading has been successfully completed.")
    print(f"Loaded {len(data)} rows of data for {data['code'][0]}")
