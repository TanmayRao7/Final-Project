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
    dataa.to_csv('stocks.csv')
    dataa = pd.read_csv('stocks.csv')
    return dataa


def endOfDay(symbol_ticker):
    dataa = get_data(symbol_ticker)
    string = dataa.iloc[-1]
    raw_text = u"\u20B9"
    response =  symbol_ticker.upper() +" EOD Data in "+raw_text+" :\n"
    response +=  string.to_string()
    return response

def trending_mf():
    mutual_funds = pd.read_html("https://finance.yahoo.com/mutualfunds")[0]
    df = mutual_funds
    df = df.iloc[0:4,:3]
    response =  df.to_string()
    return response

def get_graphical_data(symbol):
    url = "https://finance.yahoo.com/chart/"+symbol.upper()
    return url

def gainers():
    gainer = pd.read_html("https://finance.yahoo.com/gainers")[0]
    df = gainer
    df = df.iloc[0:4,:3]
    response =  df.to_string()
    return response

def losers():
    loser = pd.read_html("https://finance.yahoo.com/losers")[0]
    df = loser
    df = df.iloc[0:4,:3]
    response =  df.to_string()
    return response





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
    if "sym:" in msg :
        symbol = msg.split(":")
        symbol = str(symbol[1])
        response = endOfDay(symbol)
        reply.body(""+response)
    elif msg =="help":
        reply.body("To Get Stock Codes : \n"+'https://github.com/TanmayRao7/Final-PR/blob/1c4176ac1b24fd4292be93ca12cbc19d3a336f6a/stock_tickers.pdf')
    if msg == "mutual_funds" :
        response1 = trending_mf()
        reply.body(""+response1)
    if msg == "gainers" :
        response2 = gainers()
        reply.body(""+response2)
    if msg == "losers" :
        response3 = losers()
        reply.body(""+response3)
    elif "graph:" in msg:
        symbol = msg.split(":")
        symbol = str(symbol[1])
        url = get_graphical_data(symbol)
        reply.body(url)

    

 
 
    return str(resp)
 
if __name__ == "__main__":	
    app.run(debug=True)