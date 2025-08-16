import tkinter as tk 
import tkinter.ttk as ttk 
from tkinter import messagebox
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)



main_window = tk.Tk()
main_window.attributes("-fullscreen", True)
main_window.title("Stock Reader v1.0")
main_window.resizable(False, False) 



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

    new_price = current_price['Close'].iloc[-1]
    old_price = current_price['Close'].iloc[0]

    if new_price > old_price:
        percentage = ((new_price - old_price) / old_price) * 100
        percentage.round(2)
        result_label.config(text=f"Current Price of {stockname}: ${new_price:.2f}  ↑(+{percentage:.2f}%)", style="Green.TLabel")
        
    elif new_price < old_price:
        percentage = ((old_price - new_price) / old_price) * 100
        percentage.round(2)
        result_label.config(text=f"Current Price of {stockname}: ${new_price:.2f}  ↓(-{percentage:.2f}%)", style="Red.TLabel")

    else:
        result_label.config(text=f"Current Price of {stockname}: ${new_price:.2f}", style="")

    if current_price.empty:
        result_label.config(text=f"No data available for {stockname}.")
        return
    
    if period =="1d" and interval == "1h":
        dates = current_price.index.strftime('%H:%M').to_numpy()
        xlabel = current_price.index[-1].strftime("%Y-%m-%d")
    elif period == "5d" and interval == "4h":
        dates = current_price.index.strftime('%d %H:%M').to_numpy()
        xlabel = current_price.index[-1].strftime("%Y %b")
    elif period == "1mo" and interval == "1d":
        dates = current_price.index.strftime('%d %b').to_numpy()
        xlabel = current_price.index[-1].strftime("%Y")
    elif period == "6mo" and interval == "1wk":
        dates = current_price.index.strftime('%b %d').to_numpy()
        xlabel = current_price.index[-1].strftime("%Y")
    elif period == "ytd" and interval == "1wk":
        dates = current_price.index.strftime('%b %d').to_numpy()
        xlabel = current_price.index[-1].strftime("%Y")
    elif period == "1y" and interval == "1mo":
        dates = current_price.index.strftime('%Y %b').to_numpy()
        xlabel = ""
    elif period == "5y" and interval == "3mo":
        dates = current_price.index.strftime('%Y-%b').to_numpy()
        xlabel = ""
    else:
         dates = current_price.index.strftime('%Y-%m-%d').to_numpy()

    close_price = current_price['Close'].to_numpy()

    #Canvas Structure
    fig = Figure(figsize=(7, 5), dpi=100)
    fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.3)
    x = dates
    y = close_price
    

    plot = fig.add_subplot(111)
    plot.plot(x,y)
    
    plot.set_xlabel(xlabel)
    plot.set_title(f"{stockname} Stock Price")
    plot.tick_params(axis='x', rotation=90)
    graph_canvas = FigureCanvasTkAgg(fig, master=graph_frame)

    graph_canvas.draw()
    
    #toolbar = NavigationToolbar2Tk(graph_canvas, graph_frame)
    #toolbar.update()

    graph_canvas.get_tk_widget().place(x=0,y=0)


#Widgets
table_frame = ttk.Frame(main_window)
table_frame.place(x=0, y=0, width=600, height=700)
title_label = ttk.Label(table_frame, text="Please enter a stock symbol:")
title_label.place(x=50,y=5)
stock_entry = ttk.Entry(table_frame, width=30)
stock_entry.place(x=50, y=30)

graph_frame = ttk.Frame(main_window)
graph_frame.place(x=550, y=30, width=1500, height=900)



# Buttons
buttons = [
    ("1d", "1d", "1h", 340, 30),
    ("5d", "5d", "4h", 390, 30),
    ("1mo", "1mo", "1d", 440, 30),
    ("6mo", "6mo", "1wk", 490, 30),
    ("YTD", "ytd", "1wk", 340, 60),
    ("1yr", "1y", "1mo", 390, 60),
    ("5y", "5y", "3mo", 440, 60),
    ("Max", "max", "3mo", 490, 60)
]

for text, period, interval, x, y in buttons:
    tk.Button(
        table_frame, text=text, 
        command=lambda period = period, interval = interval:get_stock_price(period, interval),
        width=2, font=("Courier", 12)
    ).place(x=x, y=y)





#Labels
style = ttk.Style()
style.configure("Red.TLabel", foreground="red",)
style.configure("Green.TLabel", foreground="green",)

result_label = ttk.Label(table_frame, text="",)
result_label.place(x=50, y=70)    
table_label = ttk.Label(table_frame, text="")
table_label.place(x=50, y=100)

#Valid Intervals: 
#1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 4h, 1d, 5d, 1wk, 1mo, 3mo

#Update:
#August 6th: Added a function to retrieve stock data based on user input.
#August 8th: Added a function to align the stock data for better readability, including a table that represented the stock data in a more structured format. Included data such as volume, open, and close 
#August 9th: Added buttons to retrieve stock data for different periods (1d, 5d, 1mo, 3mo, 6mo, YTD, 1y, MAX) with appropriate intervals.















main_window.mainloop()
