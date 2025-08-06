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



def get_stock_price():
    stockname = stock_entry.get().upper()
    stock = yf.Ticker(stockname)
    if not stockname:
        result_label.config(text="Please enter a stock ticker symbol.")
        return
    try: 
        current_price = stock.history(period='1d')['Close'].iloc[-1]
        result_label.config(text=f"Current Price of {stockname}: ${current_price:.2f}")
    except Exception as e:
        result_label.config(text=f"Error retrieving data for {stockname}: Please enter a valid stock symbol")


stock_entry = ttk.Entry(main_window, width=30)
stock_entry.place(x=50, y=30)
enter_button = ttk.Button(main_window, text="Enter", command=get_stock_price)
enter_button.place(x=350, y=30)
result_label = ttk.Label(main_window, text="")
result_label.place(x=50, y=70)    



















main_window.mainloop()
