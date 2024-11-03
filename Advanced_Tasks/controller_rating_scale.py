from turtle import color
import gspread
from gspread.utils import ValidationConditionType
from gspread_formatting import *
import model_rating_scale
from google.oauth2.service_account import Credentials
class Controller_RatingScale:

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

    def update_status_rating_scale(self, sheet_name, sheet_id, names_status):
        cells = []
        for i, v in enumerate(names_status, 2):
            if v.status == 'Pending':
                cells.append(gspread.Cell(i, 9, 'Processed'))
        sheet = self.getting_sheet(sheet_name, sheet_id)
        sheet.update_cells(cells)

    def fill_rating_scale(self, data,sheet_name, sheet_id):
        cells = []
        for i, obj in enumerate(data,2):
            cells.append(gspread.Cell(i, 1, obj.itemid))
            cells.append(gspread.Cell(i, 2, obj.name))
            cells.append(gspread.Cell(i, 3, obj.description))
            cells.append(gspread.Cell(i, 4,obj.score))
            cells.append(gspread.Cell(i, 5, obj.label))
            cells.append(gspread.Cell(i, 6, obj.score_description))

        worksheet = self.getting_sheet(sheet_name, sheet_id)
        worksheet.update_cells(cells, value_input_option='USER_ENTERED')

    def fill_rating_names(self, data, sheet_name, sheet_id):
        names = {i.name for i in data}
        cells = []
        for i, n in enumerate(names,2):
            cells.append(gspread.Cell(i, 8, n))
        sheet = self.getting_sheet(sheet_name, sheet_id)
        sheet.update_cells(cells)

        sheet.add_validation(
            f'I2:I{len(names)+1}',
            ValidationConditionType.one_of_list,
            ['Processed', 'Pending'],
            showCustomUi=True
        )
        sheet.update([['Pending']]*len(names), 'I2' )

    def load_data(self, sheet_name, sheet_id):
        working_sheet = self.getting_sheet(sheet_name, sheet_id)
        all_values = working_sheet.get_all_records()
        rows = []
        names_status = []

        for v in all_values:
            row = model_rating_scale.Model_RatingScale()
            row.itemid = v['ItemId']
            row.name = v['Name']
            row.description = v['Description']
            row.score = v['Score']
            row.label = v['Label']
            row.score_description = v['ScoreDescription']
            rows.append(row)

            if v['Rating Scale Name']!='':
                name_status = model_rating_scale.Names_Status()
                name_status.name = v['Rating Scale Name']
                name_status.status = v['Status']
                names_status.append(name_status)

        return names_status, rows

    def formating(self, sheet_name, sheet_id, red_cells, green_cells):
        sheet = self.getting_sheet(sheet_name,sheet_id)
        cells = []

        red = CellFormat(
            backgroundColor=color(1, 0, 0))

        green = CellFormat(
            backgroundColor=color(0, 1, 0))

        if len(red_cells)>=1:
            for v in red_cells:
                cells.append((v,red))

        if len(green_cells)>=1:
            for v in green_cells:
                cells.append((v,green))

        format_cell_ranges(sheet, cells)
