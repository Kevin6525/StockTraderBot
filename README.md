# StockTraderBot
This project is fully functional but may be updated in the future. The bot utilizes past stock data by using the yfinance API and uses that data to create Bollinger Bands that
determine the buy/sell points of a stock. If a user is unsure of which stocks they wish to look at, the getTickers function call will use webscraping to find the top 5 most active
(positive) stocks of the day and use those for trading. The information for each stock is stored in a dictionary which is outputted to a text file using json and will be accessed
in future calls (i.e. next day). 
