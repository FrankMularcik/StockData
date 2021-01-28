from keep_alive import keep_alive
import gspread
from datetime import datetime
from datetime import timedelta
import time
from oauth2client.service_account import ServiceAccountCredentials
import yahoo_fin.stock_info as si
import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml


def datePlusOne(str):
	date = datetime.strptime(str, '%b %d, %Y')
	addOne = timedelta(days = 1)
	date = date + addOne
	strDate = date.strftime('%b %d, %Y')
	return strDate;

def is_float(s):
	try:
		float(s)
		return True
	except ValueError:
		return False


scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds =  ServiceAccountCredentials.from_json_keyfile_name('Sheets API key.env', scope)

client = gspread.authorize(creds)

sheet = client.open('Portfolio').sheet1

keep_alive()

while True:
  
  for j in range(2, 40):	
	  time.sleep(1.01)
	  if(sheet.cell(j, 1).value == ""):
		  break;
  
  for i in range(2, j):
    ticker = sheet.cell(i, 1).value
    data = si.get_stats(ticker)
    
    ex_date = data['Value'][25]
    sheet.update_cell(i, 22, datePlusOne(ex_date))

    pay_date = data['Value'][24]
    sheet.update_cell(i, 23, datePlusOne(pay_date))
    
    div = data['Value'][18]
    if isinstance(div, float) : sheet.update_cell(i, 9, "")
    else : sheet.update_cell(i, 10, div)
    
    beta = data['Value'][0]
    if isinstance(beta, float) : sheet.update_cell(i, 22, "")
    else : sheet.update_cell(i, 24, beta)
    
    time.sleep(3.01)

    URL = "https://www.reuters.com/companies/" + ticker + ".N/key-metrics"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    nums = soup.find_all('div', class_='KeyMetrics-table-container-3wVZN')
    num = nums[6]
    cagr = num.find_all('td')
    strCagr = cagr[5].get_text()
    if(is_float(strCagr)): numCagr = float(strCagr) / 100
    else: numCagr = strCagr
    sheet.update_cell(i, 26, numCagr)

    time.sleep(1)

  now = datetime.now()
  minus_five = timedelta(hours = 5)
  now_EST = now - minus_five
  sheet.update_cell(i + 6, 3, now_EST.strftime('%H:%M:%S %b %d, %Y'))
  
  time.sleep(259200)
