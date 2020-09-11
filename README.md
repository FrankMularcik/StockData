# StockData
A short python script I created to import some stock data into a spreadsheet I use to track my investments.

In this script I'm using the gspread library which is a Google Sheets API for Python.  This allows me to access data in the spreadsheet and write data to the spreadsheet.

I'm also using the yahoo_fin library with the stock_info module.  This has a variety of functions that return various information about certain stocks.

Once I have access to the Google Sheets File, I read the ticker symbol of the stock from the file, get the desired data, and write that data to the Google Sheet in the appropriate spot.  
