import tkinter as tk 
import tkinter.ttk as ttk 
from tkinter import messagebox
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


main_window = tk.Tk()
main_window.geometry("600x500")
main_window.title("Stock Reader v1.0")
main_window.resizable(False, False) 


current_price = None

def get_stock_price(period, interval):
    stockname = stock_entry.get().strip().upper()
    if stockname == "":
        result_label.config(text="Please enter a stock ticker symbol.")
        return
    else: 
        stock = yf.Ticker(stockname)
    try: 
        current_price = stock.history(period=period)['Close'].iloc[-1]
        result_label.config(text=f"Current Price of {stockname}: ${current_price:.2f}")
    except Exception as e:
        result_label.config(text=f"Error retrieving data for {stockname}: Please enter a valid stock symbol")
    
    current_price = yf.download(stockname, period=period, interval=interval).round(2)
    if isinstance(current_price.index, pd.MultiIndex):
        current_price.index = current_price.index.droplevel(0)

    if isinstance(current_price.columns, pd.MultiIndex):
        current_price.columns = current_price.columns.droplevel(1)
        
#Label Formatting (Panda DataFrame Alignment)
    current_price_str = current_price.to_string(index=True, header=True, justify="right")
    lines = current_price_str.split('\n')
    max_len = max(len(line) for line in lines)
    aligned_data = '\n'.join(line.ljust(max_len) for line in lines) 


    table_label.config(text=f"Price Data for {stockname}:\n{aligned_data}", font=("Courier", 12))
    print (current_price)

    if current_price.empty:
        result_label.config(text=f"No data available for {stockname}.")
        return



#Widgets
table_frame = ttk.Frame(main_window)
table_frame.place(x=0, y=0, width=600, height=700)
title_label = ttk.Label(table_frame, text="Please enter a stock symbol:")
title_label.place(x=50,y=5)
stock_entry = ttk.Entry(table_frame, width=30)
stock_entry.place(x=50, y=30)


#Buttons
oneday_button = tk.Button(table_frame, text="1d", command=lambda: get_stock_price("1d", "1h"), width=2, font=("Courier", 12))
oneday_button.place(x=340, y=30)
week_button = tk.Button(table_frame, text="5d", command=lambda: get_stock_price("5d", "4h"), width=2, font=("Courier", 12))
week_button.place(x=390, y=30)
onemonth_button = tk.Button(table_frame, text="1mo", command=lambda: get_stock_price("1mo", "1d"), width=2, font=("Courier", 12))
onemonth_button.place(x=440, y=30)
sixmonths_button = tk.Button(table_frame, text="6mo", command=lambda: get_stock_price("6mo", "1wk"), width=2, font=("Courier", 12))
sixmonths_button.place(x=490, y=30)
ytd_button = tk.Button(table_frame, text="YTD", command=lambda: get_stock_price("ytd", "1wk"), width=2, font=("Courier", 12))
ytd_button.place(x=340, y=60)
oneyear_button = tk.Button(table_frame, text="1yr", command=lambda: get_stock_price("1y", "1mo"), width=2, font=("Courier", 12))
oneyear_button.place(x=390, y=60)
fiveyear_button = tk.Button(table_frame, text="5y", command=lambda: get_stock_price("5y", "3mo"), width=2, font=("Courier", 12))
fiveyear_button.place(x=440, y=60)
max_button = tk.Button(table_frame, text="Max", command=lambda: get_stock_price("max", "3mo"), width=2, font=("Courier", 12))
max_button.place(x=490, y=60)



#Labels
result_label = ttk.Label(table_frame, text="")
result_label.place(x=50, y=70)    
table_label = ttk.Label(table_frame, text="")
table_label.place(x=50, y=100)

#Valid Intervals: 
#1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 4h, 1d, 5d, 1wk, 1mo, 3mo

#Update:
#August 6th: Added a function to retrieve stock data based on user input.
#August 8th: Added a function to align the stock data for better readability, including a table that represented the stock data in a more structured format. Included data such as volume, open, and close 
#August 9th: Added buttons to retrieve stock data for different periods (1d, 5d, 1mo, 3mo, 6mo, YTD, 1y, MAX) with appropriate intervals.

#NEED TO ADD SCROLLWHEEL FOR DATA THAT IS TOO LONG TO FIT IN THE WINDOW (ESPECIALLY FOR YTD AND MAX)
















main_window.mainloop()
