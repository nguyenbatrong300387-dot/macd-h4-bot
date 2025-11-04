import telebot
import requests
import time

TOKEN = "8494567101:AAEBEfXhkf2_qNvctzavIM8M85VvK5j3fwc"
bot = telebot.TeleBot(TOKEN)

API_KEY = "2428bdb1c5744a8da1c1ca416c6a823e"
SYMBOL = "EUR/USD"
INTERVAL = "4h"

def get_macd():
    url = f"https://api.twelvedata.com/macd?symbol={SYMBOL}&interval={INTERVAL}&apikey={API_KEY}"
    data = requests.get(url).json()
    return float(data["macd"]["macd"]), float(data["macd"]["signal"])

chat_id = 2143619263

while True:
    macd, signal = get_macd()
    
    if macd > signal:
        msg = f"📈 MACD Bullish Cross H4\n{SYMBOL}"
        bot.send_message(chat_id, msg)

    if macd < signal:
        msg = f"📉 MACD Bearish Cross H4\n{SYMBOL}"
        bot.send_message(chat_id, msg)

    time.sleep(60)
