'''
File: Sheng.Junhui.Assignment-10.py
Name: Junhui Sheng
Date: 03/13/2020
Course: Python Programming ICT-4370
Desc:
Ehancement to the assignment week 8.
1）Read stock data from JSON file and then show the trend graph.
2) Show the candlestick graph for a specific stock on the same graph

'''
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.pylab import date2num
from dateutil.parser import parse
import json
from datetime import datetime
#import mpl_finance 
import mpl_finance as mpf

#Define the function to decide if the string is number.
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    
    return False


#Define the Stock class
class Stock():
    """Represent a stock profile"""
    def __init__(self, stockSymbol):
        """Initialize the dog"""
        self.stockSymbol = stockSymbol
        self.stockDateList = []
        self.stockClose = []
        self.stockOpen = []
        self.stockHigh = []
        self.stockLow = []
        self.stockVol = []

    def addTrading(self, close_price, date, open_price, high, low, vol):
        """Add new trading data for a date"""
        self.stockClose.append(close_price)
        self.stockDateList.append(date)

        #If the following string from the file is not number, just put a number 0
        if is_number(open_price) == True:
            self.stockOpen.append(open_price)
        else:
            self.stockOpen.append('0')

        if is_number(high) == True:
            self.stockHigh.append(high)
        else:
            self.stockHigh.append('0')
           
        if is_number(low) == True:
            self.stockLow.append(low)
        else:
            self.stockLow.append('0')

        
                
#Open stock data file to get data
filePath = "AllStocks.json"
with open(filePath) as f:
    dataSet = json.load(f)

#All stock data to be saved in this dict
stockDictionary = {}


for stock in dataSet:
        #if not exist, then add as a a new entry
	if stock['Symbol'] not in stockDictionary:
		newStock = Stock(stock['Symbol'])
		print (stock['Symbol'] + " added")
		stockDictionary[stock['Symbol']] = {'stock': newStock}

	#Add the trading data to this stock	
	stockDictionary[stock['Symbol']]['stock'].addTrading(stock['Close'],\
                                                             datetime.strptime(stock['Date'], '%d-%b-%y'),\
                                                             stock['Open'],\
                                                             stock['High'],\
                                                             stock['Low'],\
                                                             stock['Volume'])

#Start to draw the trend subgraph

#set up the figure size to hold two graphs
fig = plt.figure(figsize=(12,6))

#add the first subplot for the trend
ax1 = fig.add_subplot(121)

#Generate plot data for the trend graph
for stock in stockDictionary:
	CloseData = stockDictionary[stock]['stock'].stockClose
	dates = matplotlib.dates.date2num(stockDictionary[stock]['stock'].stockDateList)
	symbol = stockDictionary[stock]['stock'].stockSymbol
	ax1.plot_date(dates, CloseData, linestyle='solid', marker='None', label = symbol)

#Adjust display contents
plt.gcf().autofmt_xdate()
plt.title("Stock Trend Graph")
plt.xlabel("Trading Date")
plt.ylabel("Close Price")

#Show the stock graph
ax1.legend()

#add the second subplot for the candelstick graph
ax2 = fig.add_subplot(122)

#Generate plot data for the candlestick graph
candle_data_list = []

#Generate plot data for the candlestick graph
for stock in stockDictionary:
        CloseData = stockDictionary[stock]['stock'].stockClose
        dates = matplotlib.dates.date2num(stockDictionary[stock]['stock'].stockDateList)
        OpenData = stockDictionary[stock]['stock'].stockOpen
        HighData = stockDictionary[stock]['stock'].stockHigh
        LowData = stockDictionary[stock]['stock'].stockLow
		
        symbol = stockDictionary[stock]['stock'].stockSymbol

        #This time, only show the candlestick for MSFT
        if symbol == 'MSFT':
            
            for i in range(len(CloseData)):
                candle_data_list.append((dates[i],float(OpenData[i]), float(HighData[i]), \
                                         float(LowData[i]), CloseData[i]))
#setup the displays for the candlestick graph
ax2.xaxis_date()
plt.xticks(rotation=45)

plt.title("Stock candlestick Graph: MSFT")
plt.xlabel("Trading Date")
plt.ylabel("Stock Price")

#Call the mpl_finance library to show the candlestick                
mpf.candlestick_ohlc(ax2,candle_data_list,width=1.0,colorup='r',colordown='green', alpha=1)


plt.show()






