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
    elif "sym:" in msg:
        symbol = msg.split(":")
        symbol = str(symbol[1])
        response = endOfDay(symbol)
        reply.body(""+response)

    

 
 
    return str(resp)
 
if __name__ == "__main__":	
    app.run(debug=True)