from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# importing python modules
import pandas as pd
import csv
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import os
import matplotlib.pyplot as plt
import os

def get_data(symbol_ticker):
    company= symbol_ticker
    dataa = yf.download(company , period="1d" , interval="1m")
    return dataa

def endOfDay(symbol_ticker):
    dataa = get_data(symbol_ticker)
    string = dataa.iloc[-1]
    raw_text = u"\u20B9"
    response = "Current Prices for "+ symbol_ticker.upper() +" in "+raw_text+" :\n"
    response += string.to_string()
    return response

def get_Consolidated_data(symbol_ticker):
    df = get_data(symbol_ticker)
    df = yf.download(symbol_ticker , period="1d" , interval="1m")
    trace1 = go.Scatter(x = df['Datetime'], y = df['Open'], name='Opening Prices (in Rupees)')
    trace2 = go.Scatter(x = df['Datetime'], y = df['High'], name='High Prices (in Rupees)')
    trace3 = go.Scatter(x = df['Datetime'], y = df['Low'], name='Low Prices (in Rupees)')
    trace4 = go.Scatter(x = df['Datetime'], y = df['Close'], name='Closing Prices (in Rupees)')
    trace5 = go.Scatter(x = df['Datetime'], y = df['Adj Close'], name='Adjusted Closing Prices (in Rupees)')
    fig = go.Figure(data=[trace1, trace2, trace3, trace4,trace5] )
    fig.update_layout(title='Current Stock Prices against Time',
                   plot_bgcolor='rgb(230, 230,230)',
                   showlegend=True)
    if not os.path.exists("images"):
        os.mkdir("images")
    return fig

app = Flask(__name__)
 
@app.route("/")
def wa_hello():
    return "Hello, World!"
 
@app.route("/wasms", methods=['POST'])
def wa_sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    
    msg = request.form.get('Body','').lower() # Reading the message from the whatsapp
 
    print("msg-->",msg)
    resp = MessagingResponse()
    reply=resp.message()
    # Create reply
    if msg == "hi":
       reply.body("Hello, welcome to the Stock Market Bot \n Type sym:<stock_symbol> to know the price of the stock. ")
    elif "sym:" in msg and "g:sym" not in msg:
        symbol = msg.split(":")
        symbol = str(symbol[1])
        response = endOfDay(symbol)
        reply.body(""+response)
    elif "g:sym:" in msg :
        symbol = msg.split(":")
        symbol = str(symbol[2])
        img = get_Consolidated_data(symbol)
        reply.media(img)

    elif "help" in msg:
        reply.body("To Get Stock Codes : \n"+'https://github.com/TanmayRao7/Final-PR/blob/1c4176ac1b24fd4292be93ca12cbc19d3a336f6a/stock_tickers.pdf')
    else:
        reply.body("Please type hi to get started.")

    

 
 
    return str(resp)
 
if __name__ == "__main__":	
    app.run(debug=True)