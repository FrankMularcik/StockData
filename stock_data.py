from datetime import datetime
from datetime import timedelta
import gspread

import os

import yahoo_fin.stock_info as si
from oauth2client.service_account import ServiceAccountCredentials

os.chdir(r"C:\Users\mular\Python")

scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds =  ServiceAccountCredentials.from_json_keyfile_name('Sheets API key.json', scope)

client = gspread.authorize(creds)

sheet = client.open('Portfolio').sheet1

def datePlusOne(str):
	date = datetime.strptime(str, '%b %d, %Y')
	addOne = timedelta(days = 1)
	date = date + addOne
	strDate = date.strftime('%b %d, %Y')
	return strDate;

for j in range(2, 30):	
	if(sheet.cell(j, 1).value == ""):
		break;

for i in range(2, j):
	ticker = sheet.cell(i, 1).value
	data = si.get_stats(ticker)

	ex_date = data['Value'][25]
	sheet.update_cell(i, 20, datePlusOne(ex_date))

	pay_date = data['Value'][24]
	sheet.update_cell(i, 21, datePlusOne(pay_date))
	
	div = data['Value'][18]
	if isinstance(div, float) : sheet.update_cell(i, 9, "")
	else : sheet.update_cell(i, 9, div)
	
	beta = data['Value'][0]
	if isinstance(beta, float) : sheet.update_cell(i, 22, "")
	else : sheet.update_cell(i, 22, beta)
