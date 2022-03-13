import time
import yfinance as yf
from yahoo_fin import stock_info as si
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
from os import path
from selenium import webdriver
import json

#Keep track of our total investments and total profits
totalInvest = 0
totalProfit = 0
# If not sure what stocks to choose, call this function to pick the top 5 most active stocks (Positive change)
def getTickers():
    driver = webdriver.Chrome()
    driver.get('https://finance.yahoo.com/most-active')
    button = driver.find_element_by_xpath('//*[@id="scr-res-table"]/div[1]/table/thead/tr/th[4]')
    button.click()
    time.sleep(2)
    button.click()
    time.sleep(2)
    ticker1 = driver.find_element_by_xpath('//*[@id="scr-res-table"]/div[1]/table/tbody/tr[1]/td[1]/a').text
    ticker2 = driver.find_element_by_xpath('//*[@id="scr-res-table"]/div[1]/table/tbody/tr[2]/td[1]/a').text
    ticker3 = driver.find_element_by_xpath('//*[@id="scr-res-table"]/div[1]/table/tbody/tr[3]/td[1]/a').text
    ticker4 = driver.find_element_by_xpath('//*[@id="scr-res-table"]/div[1]/table/tbody/tr[4]/td[1]/a').text
    ticker5 = driver.find_element_by_xpath('//*[@id="scr-res-table"]/div[1]/table/tbody/tr[5]/td[1]/a').text
    driver.quit()
    return[ticker1,ticker2,ticker3,ticker4,ticker5]
# Execute a 'buy' update and store the data accordingly
def executeBuy(ticker, totalInvest, dict, currentPrice):
    totalInvest += 200
    dict[ticker]['buyPrice'] = currentPrice
    dict[ticker]['buyTime'] = datetime.now()
    dict[ticker]['totalShares'] = '{:.2f}'.format(float(200/currentPrice))
# Execute a 'sell' update and store the date accordingly
def executeSell(ticker, totalProfit, dict, currentPrice):
    totalProfit += (currentPrice - dict[ticker]['buyPrice']) * dict[ticker]['totalShares']
    dict[ticker]['sellPrice'] = currentPrice
    dict[ticker]['sellTime'] = datetime.now()
    dict[ticker]['totalShares'] = 0
# At the end of the stock market day output our summary
def printSummary(totalInvest, totalProfit):
    print("Invested a total of ", str(totalInvest), " dollars today")
    print("Made a total of ", str(totalProfit), " dollars today")
# Using our tickers, grab the buy/sell point by using bollinger bands and plotting the information
# To display the graphs, uncomment the plt.show()
def getHistory(tickers, dict):
    for i in range(len(tickers)):
        begin = date.today()-timedelta(days=100)
        finish = date.today()
        stockinfo = yf.download(tickers[i], start=begin, end=finish)
        simpleAvg20 = pd.DataFrame()
        simpleStd20 = pd.DataFrame()
        upperBand = pd.DataFrame()
        lowerBand = pd.DataFrame()
        simpleAvg20['20 Day MA'] = stockinfo['Adj Close'].rolling(window=20).mean()
        simpleStd20['20 Day STD'] = stockinfo['Adj Close'].rolling(window=20).std()
        upperBand['Upper Band'] = simpleAvg20['20 Day MA'] + (simpleStd20['20 Day STD'] * 1.5)
        lowerBand['Lower Band'] = simpleAvg20['20 Day MA'] - (simpleStd20['20 Day STD'] * 1.5)
        uBand = np.array(upperBand['Upper Band'])
        lBand = np.array(lowerBand['Lower Band'])
        dict[tickers[i]]['upperBand'] = '{:.2f}'.format(uBand[-1])
        dict[tickers[i]]['lowerBand'] = '{:.2f}'.format(lBand[-1])
        plt.figure(figsize=(12.5, 5))
        plt.plot(simpleAvg20['20 Day MA'], label='20 Day MA')
        plt.plot(upperBand['Upper Band'], label='Upper Band')
        plt.plot(lowerBand['Lower Band'], label='Lower Band')
        plt.title(tickers[i] + ': 20 Day Bollinger Band')
        plt.xlabel(str(begin) + " - " + str(finish))
        plt.ylabel('Price (in USD)')
        plt.legend(loc='upper left')
    # Uncomment to show the graphs (Program stops until graphs are closed)
    #plt.show()
# Use Bollinger Bands to determine when to buy/sell
# We only invest 200 at a time out of the 1000 and will look through 5 stocks every minute
# If we already bought a stock we will hold onto that stock until it is sold instead of
# Buying again (Subject to change as I have more time to add more complexity)
def mainRun(tickers, totalInvest, totalProfit, dict):
    for ticker in tickers:
        currentPrice = '{:.2f}'.format(float(si.get_live_price(ticker)))
        print("Current Price for ", ticker, " : ", currentPrice)
        dict[ticker]['currentPrice'] = currentPrice
        if currentPrice <= dict[ticker]['lowerBand'] and dict[ticker]['buyPrice'] == 0 and totalInvest < 1000:
            executeBuy(ticker, totalInvest, dict, currentPrice)
        elif currentPrice >= dict[ticker]['upperBand'] and dict[ticker]['totalShares'] > 0:
            executeSell(ticker, totalProfit, dict, currentPrice)
# Create our dictionary for each ticker
def createDict(tickers):
    dict = {}
    for ticker in tickers:
        dict[ticker] = {
            'name': ticker,
            'currentPrice': 0.0,
            'upperBand': 0.0,
            'lowerBand': 0.0,
            'buyPrice': 0.0,
            'sellPrice': 0.0,
            'totalShares': 0.0,
            'buyTime': '',
            'sellTime': ''
        }
    return dict

#Call the getTickers() function if we don't know what tickers to use
#tickers = getTickers()
tickers = ['TSLA', 'XLF', 'QQQ', 'SPY', 'VXX']
#In future calls we reference our past days stocks buys/sells
if not path.exists('stocksDictionary.txt'):
    stocksDict = createDict(tickers)
else :
    with open('stocksDictionary.txt') as file:
        data = file.read()
        stocksDict = json.loads(data)
stocksDict = createDict(tickers)
#Call getHistory at beginning of run to get stocks info and buy/sell points
getHistory(tickers, stocksDict)
#Run until the closing time of market (1PM PST)
while(datetime.now().hour < 13):
    mainRun(tickers, totalInvest, totalProfit, stocksDict)
    time.sleep(30)

printSummary(totalInvest, totalProfit)
# Store dictionary contents to file for future use
file = open('stocksDictionary.txt', 'x')
file.write(json.dumps(stocksDict))
file.close()
