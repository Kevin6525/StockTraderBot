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
# Pick the 5 stocks to buy in today
# Allocate 200 dollars to each stock to trade with
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
#   decrement total, save current price and date/time of purchase add data to dict
#def executeSell():
#   add difference of buy and sell to a new value called todaysProfits and push the date/time/sale price and number of shares sold and the initial buy price into a dict
#   Remove the dict with the corresponding ticker key from the buy dict
#def printSummary():
#   Output the buy dict at end of day (should be empty)
#   Output the sell dict at the end of day (should not be empty)
#   Output total profits: todaysProfits
#   
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
# Run this every minute until market closes
# Print output summary
def mainRun(tickers):
    #iterate through all the tickers and get their current price
    for ticker in tickers:
        driver = webdriver.Chrome()
        driver.get('https://finance.yahoo.com/quote/' + ticker)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        currentPrice = soup.find(id="quote-market-notice").find_parent().find("span").text
        #if the current price fits our algorithm to buy && our total is > 0 then trigger buy for 200 dollars in fractional shares
        #if the current price fits out algorithm to sell && our buy dict has the ticker inside then sell the shares
tickers = getTickers()
getHistory(tickers)
