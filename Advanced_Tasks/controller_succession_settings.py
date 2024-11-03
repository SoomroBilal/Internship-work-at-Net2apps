from turtle import color
import gspread
from google.oauth2.service_account import Credentials
from gspread.utils import ValidationConditionType
from gspread_formatting import *

import model_succession_settings

class Controller_SuccessionSettings:
    def getting_sheet(self, sheet_name, id):
        scopes = ["https://spreadsheets.google.com/feeds",
                  'https://www.googleapis.com/auth/spreadsheets',
                  "https://www.googleapis.com/auth/drive.file",
                  "https://www.googleapis.com/auth/drive"
                  ]

        creds = Credentials.from_service_account_file('credentials.json', scopes=scopes)
        client = gspread.authorize(creds)
        sheets = client.open_by_key(id)
        sheet = sheets.worksheet(sheet_name)
        return sheet

    def fill_succession_settings(self, sheet_name, data, sheet_id):
        cells = []
        for i, obj in enumerate(data, 2):
            cells.append(gspread.Cell(i, 1, obj.itemid))
            cells.append(gspread.Cell(i, 2, obj.name))
            cells.append(gspread.Cell(i, 3, obj.date1))
            cells.append(gspread.Cell(i, 4, obj.date2))

        sheet = self.getting_sheet(sheet_name, sheet_id)
        sheet.update_cells(cells, value_input_option='USER_ENTERED')

    def fill_succession_settings_checkboxes(self,sheet_name, data, sheet_id):
        cells = []
        for i, obj in enumerate(data, 2):
            cells.append(gspread.Cell(i, 6, obj.checkbox_description))
            cells.append(gspread.Cell(i, 7, obj.status))

        sheet = self.getting_sheet(sheet_name, sheet_id)
        checkbox_validation = DataValidationRule(BooleanCondition('BOOLEAN', ('TRUE', 'FALSE')), showCustomUi=True)
        set_data_validation_for_cell_range(sheet, f'G2:G{len(data) + 1}', checkbox_validation)
        sheet.update_cells(cells, value_input_option='USER_ENTERED')


    def getting_sheet_data(self,sheet_name, sheet_id):
        sheet = self.getting_sheet(sheet_name, sheet_id)
        all_values = sheet.get_all_records()
        rows = []
        checkboxes = []
        for v in all_values:
            row = model_succession_settings.Model_SuccessionSettings()
            row.itemid = v['ItemId']
            row.name = v['Live Profiles']
            row.date1 = v['Date1']
            row.date2 = v['Date2']
            rows.append(row)

            if v['Checkbox description']!='':
                checkbox = model_succession_settings.checkboxes()
                checkbox.checkbox_description = v['Checkbox description']
                if checkbox.status == "TRUE":
                    checkbox.status = True
                else:
                    checkbox.status = False
                checkboxes.append(checkbox)
        return  rows, checkboxes

    def formating(self, sheet_name, sheet_id, red_cells, green_cells):
        sheet = self.getting_sheet(sheet_name, sheet_id)
        cells = []

        red = CellFormat(
            backgroundColor=color(1, 0, 0))

        green = CellFormat(
            backgroundColor=color(0, 1, 0))

        if len(red_cells) >= 1:
            for v in red_cells:
                cells.append((v, red))

        if len(green_cells) >= 1:
            for v in green_cells:
                cells.append((v, green))

        format_cell_ranges(sheet, cells)
