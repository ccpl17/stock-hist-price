from yahooquery import Ticker


def fetch_price(ticker, start_date, end_date, frequency, save_path):
    fetch_data = Ticker(ticker, asynchronous=True)
    dataframe = fetch_data.history(interval=frequency, start=start_date, end=end_date)
    if len(dataframe) == 0:
        return 1
    else:
        dataframe.to_excel(f"{save_path}/{ticker}_Historical_Prices.xlsx")
        dataframe.to_csv(f"{save_path}/{ticker}_Historical_Prices.csv")
        return 0
