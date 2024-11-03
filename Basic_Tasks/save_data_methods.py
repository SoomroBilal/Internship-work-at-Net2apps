import gspread
from google.oauth2.service_account import Credentials
import csv
import openpyxl

def save_data_as_csv(filename, data):
    if type(data) not in [dict, list, tuple]:
        print("Incorrect data type")
    else:
        if type(data) == dict:
            header = list(data.keys())
            data = [list(i) for i in zip(*data.values())]
            data.insert(0, header)

        if '.csv' not in filename:
            filename = filename + '.csv'
        with open(filename, 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            for i in data:
                writer.writerow(i)

def save_data_as_xlsx(filename, data):
    if type(data) not in [dict, list, tuple]:
        print("Incorrect data type")
    else:
        if type(data) == dict:
            header = list(data.keys())
            data = [list(i) for i in zip(*data.values())]
            data.insert(0, header)

        wb = openpyxl.Workbook()
        sheet = wb.active
        for i in data:
            sheet.append(i)
        if '.xlsx' not in filename:
            filename = filename + '.xlsx'
        wb.save(filename)

def gspread_config(credentials):
        scopes = ["https://spreadsheets.google.com/feeds",
                  'https://www.googleapis.com/auth/spreadsheets',
                  "https://www.googleapis.com/auth/drive.file",
                  "https://www.googleapis.com/auth/drive"
                  ]

        creds = Credentials.from_service_account_file(credentials, scopes=scopes)
        return gspread.authorize(creds)

def save_data_to_sheets(filename, data, credentials, sheet_id, starting_cell, create_new_sheet):
    if type(data) not in [dict, list, tuple]:
        print("Incorrect data type")
    else:
        if type(data) == dict:
            header = list(data.keys())
            data = [list(i) for i in zip(*data.values())]
            data.insert(0, header)

        client = gspread_config(credentials)
        sheet = client.open_by_key(sheet_id)
        if create_new_sheet:
            worksheet = sheet.add_worksheet(filename, len(data), len(data[0]))
        else:
            worksheet = sheet.worksheet(filename)
        worksheet.update(data, starting_cell)



