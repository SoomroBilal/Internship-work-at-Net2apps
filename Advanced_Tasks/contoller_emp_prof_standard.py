from turtle import color
import gspread
from gspread.utils import ValidationConditionType
from gspread_formatting import *
import model_emp_profile_standard
from google.oauth2.service_account import Credentials

class ControllerEmpProfStandard:

    def getting_sheet(self, sheet_name, sheet_id):
        scopes = ["https://spreadsheets.google.com/feeds",
                  'https://www.googleapis.com/auth/spreadsheets',
                  "https://www.googleapis.com/auth/drive.file",
                  "https://www.googleapis.com/auth/drive"
                  ]

        creds = Credentials.from_service_account_file('credentials.json', scopes=scopes)
        client = gspread.authorize(creds)
        sheets = client.open_by_key(sheet_id)
        sheet = sheets.worksheet(sheet_name)
        return sheet

    def fill_emp_prof_stand_Dropdowns(self, data, sheet_name, sheet_id):
        sheet = self.getting_sheet(sheet_name, sheet_id)
        cells = []
        for i, n in enumerate(data.names, 2):
            cells.append(gspread.Cell(i, 2, n))
            cells.append(gspread.Cell(i, 17, n))
            cells.append(gspread.Cell(i, 18, 'Pending'))


        data_validations = [
            (f"E2:E{len(data.names) + 1}", DataValidationRule(BooleanCondition('ONE_OF_LIST', data.enabled),showCustomUi=True)),
            (f"G2:G{len(data.names) + 1}", DataValidationRule(BooleanCondition('ONE_OF_LIST', data.picklist),showCustomUi=True)),
            (f"H2:H{len(data.names) + 1}", DataValidationRule(BooleanCondition('ONE_OF_LIST', data.parent_field_for_picklist),showCustomUi=True)),
            (f"I2:I{len(data.names) + 1}", DataValidationRule(BooleanCondition('ONE_OF_LIST', data.mandatory),showCustomUi=True)),
            (f"J2:J{len(data.names) + 1}", DataValidationRule(BooleanCondition('ONE_OF_LIST', data.masked),showCustomUi=True)),
            (f"K2:K{len(data.names) + 1}", DataValidationRule(BooleanCondition('ONE_OF_LIST', data.log_read_access),showCustomUi=True)),
            (f"R2:R{len(data.names) + 1}", DataValidationRule(BooleanCondition('ONE_OF_LIST', ['Pending', 'Processed']),showCustomUi=True))
        ]

        set_data_validation_for_cell_ranges(sheet, data_validations)
        sheet.update_cells(cells)

    def fill_emp_prof(self, data, sheet_name, sheet_id):
        cells = []
        for i, obj in enumerate(data, 2):
            cells.append(gspread.Cell(i, 1, obj.itemId))
            cells.append(gspread.Cell(i, 3, obj.label))
            cells.append(gspread.Cell(i, 4, obj.default_label))
            cells.append((gspread.Cell(i, 5, obj.enabled)))
            cells.append(gspread.Cell(i, 6, obj.maximum_length))
            cells.append(gspread.Cell(i, 7, obj.picklist))
            cells.append(gspread.Cell(i, 8, obj.parent_field_for_picklist))
            cells.append(gspread.Cell(i, 9, obj.mandatory))
            cells.append(gspread.Cell(i, 10, obj.masked))
            cells.append(gspread.Cell(i, 11, obj.read_log_access))
        worksheet = self.getting_sheet(sheet_name, sheet_id)
        worksheet.update_cells(cells, value_input_option='USER_ENTERED')

    def fill_permissions(self, data, sheet_name, sheet_id):
        cells = []
        for i, obj in enumerate(data, 2):
            cells.append(gspread.Cell(i, 1, obj.itemId))
            cells.append(gspread.Cell(i, 13, obj.identifier))
            cells.append(gspread.Cell(i, 14, obj.permission))
            cells.append(gspread.Cell(i, 15, obj.roll_type))
        worksheet = self.getting_sheet(sheet_name, sheet_id)
        worksheet.update_cells(cells, value_input_option='USER_ENTERED')

    def load_data(self, sheet_name, sheet_id):
        working_sheet = self.getting_sheet(sheet_name, sheet_id)
        all_values = working_sheet.get_all_records()
        rows = []
        names_status = []
        permissions = []
        for v in all_values:
            if v['Identifier'] != '':
                row = model_emp_profile_standard.ModelEmpProfStandard()
                row.itemId = v['ItemId']
                row.identifier = v['Identifier']
                row.label = v['Label']
                row.default_label = v['Default Label']
                row.maximum_length = str(v['Maximum Length'])
                row.enabled = v['Enabled']
                row.picklist = v['Picklist']
                row.parent_field_for_picklist = v['Parent Field for Picklist']
                row.mandatory = v['Mandatory']
                row.masked = v['Masked']
                row.log_read_access = v['Log Read Access']
                rows.append(row)

                name_status = model_emp_profile_standard.ModelEmpProfStandardProcessing()
                name_status.identifier = v['Identifier-Processing-Section']
                name_status.status = v['Status']
                names_status.append(name_status)

            if v['Identifier-Permission']!='':
                permission = model_emp_profile_standard.ModelEmpProfStandardPermissions()
                permission.itemId = v['ItemId']
                permission.identifier = v['Identifier-Permission']
                permission.permission = v['Permission']
                permission.roll_type = v['Role Type']
                permissions.append(permission)

        return rows, names_status, permissions

    def update_status_rating_scale(self, sheet_name, sheet_id, names_status):
        cells = []
        for i, v in enumerate(names_status, 2):
            if v.status == 'Pending':
                cells.append(gspread.Cell(i, 18, 'Processed'))
        sheet = self.getting_sheet(sheet_name, sheet_id)
        sheet.update_cells(cells)

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
