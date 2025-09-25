import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Reader v1.0", layout="wide")


st.write("")
r1c1, r1c2, r1c3 = st.columns([1,2,1])

with r1c2:
    st.title("📈 Stock Reader")

st.write("")
st.write("")
st.write("")

r2c1, r2c2, r2c3, r2c4= st.columns([0.5,0.5,2,1])

r3c1, r3c2 = st.columns([2,3])

with r2c3:
    stockname = st.text_input("Enter a stock ticker symbol (e.g., AAPL, TSLA):", "").upper()

# Define period/interval options
period_options = {
    "1d": ("1d", "1h"),
    "5d": ("5d", "4h"),
    "1mo": ("1mo", "1d"),
    "6mo": ("6mo", "1wk"),
    "YTD": ("ytd", "1wk"),
    "1y": ("1y", "1mo"),
    "5y": ("5y", "3mo"),
    "Max": ("max", "3mo")
}

price_or_volume = {
    "Price": "price",
    "Volume": "volume",
    "Both": "both"
}

with r2c1:
    selected_pv = st.selectbox("Price/Volume:", list(price_or_volume.keys()), key="price_or_volume")
    pv_choice = price_or_volume[selected_pv]

with r2c2:
    selected = st.selectbox("Choose period:", list(period_options.keys()))
    period, interval = period_options[selected]

st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background-color: #4CAF50;  /* Green button */
        color: white;
        height: 70px;
        width: 360px;
        border-radius: 10px;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
with r2c4: 
    get_stock_data = st.button("Get Stock Data", key="get_stock_data")  

if get_stock_data:
    if stockname == "":
        st.warning("⚠️ Please enter a stock ticker symbol.")
    else:
        try:
            stock = yf.Ticker(stockname)
            current_price = stock.history(period=period)['Close'].iloc[-1]
        except Exception as e:
            st.error(f"Error retrieving data for {stockname}: Please enter a valid stock symbol")
            st.stop()
        # Download price data
        with r3c1:
            current_price = yf.download(stockname, period=period, interval=interval).round(2)
            if isinstance(current_price.index, pd.MultiIndex):
                current_price.index = current_price.index.droplevel(0)

            if isinstance(current_price.columns, pd.MultiIndex):
                current_price.columns = current_price.columns.droplevel(1)

            new_price = current_price['Close'].iloc[-1]
            old_price = current_price['Close'].iloc[0] 
            
            if new_price > old_price:
                percentage = ((new_price - old_price) / old_price) * 100
                st.markdown(
                    f"**Current Price of {stockname}: ${new_price:.2f}  "
                    f"<span style='color:green;'>↑(+{percentage:.2f}%)</span>**",
                    unsafe_allow_html=True
                )

            elif new_price < old_price:
                percentage = ((old_price - new_price) / old_price) * 100
                st.markdown(
                    f"**Current Price of {stockname}: ${new_price:.2f}  "
                    f"<span style='color:red;'>↓(-{percentage:.2f}%)</span>**",
                    unsafe_allow_html=True
                )
            else:
                st.write(f"**Current Price of {stockname}: ${new_price:.2f}**")   
 
            st.write(f"Price Data for {stockname}:\n")
            st.write(current_price)
            current_price_str = current_price.to_string(index=True, header=True, justify="right")
            lines = current_price_str.split('\n')
            max_len = max(len(line) for line in lines)
            aligned_data = '\n'.join(line.ljust(max_len) for line in lines) 

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


        with r3c2:
            if pv_choice == "both":
                fig = plt.figure(figsize=(10, 8), dpi=100)
                fig.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.27, hspace=0.5,)
                x = dates
                y = close_price

                volumeaxis = current_price['Volume'].to_numpy()
                
                if np.max(volumeaxis) > 1e9:
                    volumeaxis = volumeaxis / 1e9
                    volumelabel = "Volume (Billions)"
                elif np.max(volumeaxis) > 1e6:
                    volumeaxis = volumeaxis / 1e6
                    volumelabel = "Volume (Millions)"
                elif np.max(volumeaxis) > 1e3:
                    volumeaxis = volumeaxis / 1e3
                    volumelabel = "Volume (Thousands)"

                pplot = fig.add_subplot(211) #----------------> pplot = "price plot"

                pplot.plot(x,y)
                pplot.set_xlabel(xlabel)
                pplot.set_ylabel("Price ($)")
                pplot.set_title(f"{stockname} Stock Price")
                pplot.tick_params(axis='x', rotation=90)
                pplot.grid(True, linestyle='--', alpha=0.5)

                vplot = fig.add_subplot(212) #----------------> vplot = "volume plot"

                vplot.bar(x, volumeaxis, color='orange', width=0.5)
                vplot.set_ylabel(volumelabel)
                vplot.set_xlabel(xlabel)
                vplot.tick_params(axis='x', rotation=90)
                vplot.set_title(f"{stockname} Trading Volume")

                st.pyplot(fig)
            
            elif pv_choice == "price":
                fig = plt.figure(figsize=(10, 5), dpi=100)
                x = dates
                y = close_price

                plt.plot(x,y)
                plt.xlabel(xlabel)
                plt.ylabel("Price ($)")
                plt.title(f"{stockname} Stock Price")
                plt.xticks(rotation=90)
                plt.grid(True, linestyle='--', alpha=0.5)

                st.pyplot(fig)
            
            elif pv_choice == "volume":
                fig = plt.figure(figsize=(10, 5), dpi=100)
                x = dates
                volumeaxis = current_price['Volume'].to_numpy()
                
                if np.max(volumeaxis) > 1e9:
                    volumeaxis = volumeaxis / 1e9
                    volumelabel = "Volume (Billions)"
                elif np.max(volumeaxis) > 1e6:
                    volumeaxis = volumeaxis / 1e6
                    volumelabel = "Volume (Millions)"
                elif np.max(volumeaxis) > 1e3:
                    volumeaxis = volumeaxis / 1e3
                    volumelabel = "Volume (Thousands)"

                plt.bar(x, volumeaxis, color='orange', width=0.5)
                plt.ylabel(volumelabel)
                plt.xlabel(xlabel)
                plt.xticks(rotation=90)
                plt.title(f"{stockname} Trading Volume")

                st.pyplot(fig)







#btn1 = st.button("Button 1", key="btn1")
#btn2 = st.button("Button 2", key="btn2")

#st.markdown(
#    """
#    <style>
#    /* First button on the page */
#    div.stButton > button:first-child {
#        height: 60px;
#        background-color: green;
#   }

#    /* Second button on the page */
#    div.stButton > button:nth-child(2) {
#        height: 40px;
#       background-color: orange;
#    }
#    </style>
#    """,
#    unsafe_allow_html=True
