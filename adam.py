import sys
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import twstock
from mpl_finance import candlestick_ohlc

def weekday_candlestick(ohlc_data, ax, fmt='%b %d', freq=7, **kwargs):
    ohlc_data_arr = np.array(ohlc_data)
    ohlc_data_arr2 = np.hstack([np.arange(ohlc_data_arr[:,0].size)[:,np.newaxis], ohlc_data_arr[:,1:]])
    ndays = ohlc_data_arr2[:,0]

    # Convert matplotlib date numbers to strings based on `fmt`
    dates = mdates.num2date(ohlc_data_arr[:,0])
    date_strings = []
    for date in dates:
        date_strings.append(date.strftime(fmt))

    # Plot candlestick chart
    candlestick_ohlc(ax, ohlc_data_arr2, **kwargs)

    # Format x axis
    ax.set_xticks(ndays[::freq])
    ax.set_xticklabels(date_strings[::freq], rotation=45, ha='right')
    ax.set_xlim(ndays.min(), ndays.max())

    plt.autoscale(tight=True)
    plt.show()

def main():
    if len(sys.argv) != 2:
        print("Please run the script as:\n$python3 adam.py stock_num")
        exit(1)

    stock_num = sys.argv[1]
    stock = twstock.Stock(str(stock_num))

    # Convert to ohlc data
    quotes = []
    for i in range(len(stock.date)):
        quotes.append((mdates.date2num(stock.date[i]), stock.open[i], stock.high[i], stock.low[i], stock.price[i]))

    # Print candlestick
    fig, ax = plt.subplots()
    plt.title(str(stock_num))
    weekday_candlestick(quotes, ax, width=0.5, colorup='r', colordown='k')

if __name__ == "__main__":
    main()
