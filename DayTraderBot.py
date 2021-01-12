import time

import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import seaborn as sns
from bs4 import BeautifulSoup
from selenium import webdriver

totalInvest = 1000.00
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
#def executeBuy():
#    Bought : {
#        "close" :
#        "high" :

#
#
#    Need to pass in price, shares and time. Decrement total
#    return str(time) + " Bought " + str(shares) + " shares at " + str(price)
#def executeSell():
#    return str(time_ + " Sold " + str(shares) + "shares at " + str(price)
#def printSummary():
def getHistory(tickers):
    for i in range(len(tickers)):
        stockinfo = yf.download(tickers[i], start='2017-01-01', end='2020-12-31')
        print(stockinfo)
        plt.figure(figsize=(12.5, 5))
        plt.plot(stockinfo['Adj Close'], label=tickers[i])
        plt.title(tickers[i] + ' Adj. Close Price History')
        plt.xlabel('Jan 1, 2007 - Dec 31 2020')
        plt.ylabel('Adj. Close Price (in USD)')
        plt.legend(loc='upper left')

        simpleAvg30 = pd.DataFrame()
        simpleAvg30['Adj Close'] = stockinfo['Adj Close'].rolling(window=30).mean()
        print(simpleAvg30)
        simpleAvg100 = pd.DataFrame()
        simpleAvg100['Adj Close'] = stockinfo['Adj Close'].rolling(window=100).mean()

        plt.figure(figsize=(12.5, 5))
        plt.plot(stockinfo['Adj Close'], label=tickers[i])
        plt.plot(simpleAvg30['Adj Close'], label='Avg30')
        plt.plot(simpleAvg100['Adj Close'], label='Avg100')
        plt.title(tickers[i] + ' Adj. Close Price History')
        plt.xlabel('Jan 1, 2007 - Dec 31 2020')
        plt.ylabel('Adj. Close Price (in USD)')
        plt.legend(loc='upper left')
    plt.show()
# Use dual moving average crossover to determine when to buy/sell stock
def mainRun(tickers):
    for ticker in tickers:
        driver = webdriver.Chrome()
        driver.get('https://finance.yahoo.com/quote/' + ticker)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        currentPrice = soup.find(id="quote-market-notice").find_parent().find("span").text

tickers = getTickers()
getHistory(tickers)
