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

def get_stock_price():
    stockname = stock_entry.get().strip().upper()
    if stockname == "":
        result_label.config(text="Please enter a stock ticker symbol.")
        return
    else: 
        stock = yf.Ticker(stockname)
    try: 
        current_price = stock.history(period='1d')['Close'].iloc[-1]
        result_label.config(text=f"Current Price of {stockname}: ${current_price:.2f}")
    except Exception as e:
        result_label.config(text=f"Error retrieving data for {stockname}: Please enter a valid stock symbol")
    
    current_price = yf.download(stockname, period='1d', interval='1h').round(2)
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
title_label = ttk.Label(main_window, text="Please enter a stock symbol:")
title_label.place(x=50,y=5)
stock_entry = ttk.Entry(main_window, width=30)
stock_entry.place(x=50, y=30)
enter_button = ttk.Button(main_window, text="Enter", command=get_stock_price)
enter_button.place(x=350, y=30)
result_label = ttk.Label(main_window, text="")
result_label.place(x=50, y=70)    
table_label = ttk.Label(main_window, text="")
table_label.place(x=50, y=100)





















main_window.mainloop()
