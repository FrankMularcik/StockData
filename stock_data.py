import gspread

import yahoo_fin.stock_info as si
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds =  ServiceAccountCredentials.from_json_keyfile_name('Sheets API key.json', scope)

client = gspread.authorize(creds)

sheet = client.open('Python Test').sheet1

for i in range(2, 23):	

	ticker = sheet.cell(i, 1).value
	data = si.get_stats(ticker)

	ex_date = data.loc[25, 'Value']
	sheet.update_cell(i, 6, ex_date)

	pay_date = data.loc[24, 'Value']
	sheet.update_cell(i, 7, pay_date)
	
	div = data.loc[18, 'Value']
	if isinstance(div, float) : sheet.update_cell(i, 4, "None")
	else : sheet.update_cell(i, 4, div)
	
	beta = data.loc[0, 'Value']
	if isinstance(beta, float) : sheet.update_cell(i, 8, "No Data")
	else : sheet.update_cell(i, 8, beta)
