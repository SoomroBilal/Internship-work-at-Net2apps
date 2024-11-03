from selenium import webdriver
from SeleniumHelperUtils import methods
import model_succession_settings
from controller_succession_settings import Controller_SuccessionSettings

class SuccessionSettingsValidation:
    def __init__(self, driver):
        self.methods = methods(driver)
        self.controller = Controller_SuccessionSettings()
        scrb_id = '_s.crb' + driver.current_url.split('_s.crb')[1]
        succession_setting_url = "https://hcm41preview.sapsf.com/acme?fbacme_o=admin&pess_old_admin=true&ap_param_action=succession_settings&itrModule=talent&" + scrb_id
        driver.get(succession_setting_url)

    def getting_data_from_sap(self):
        rows = []
        for i in range(1, self.methods.ReturnLengthOfElements("//td[contains(text(), 'Default Dates')]//tbody//tr",'xpath') + 1):
            row = model_succession_settings.Model_SuccessionSettings()
            row.itemid = "=row()-1"
            row.name = self.methods.GetElementText(f"((//td[contains(text(),'Default Dates')]//tbody//tr)[{i}]//td)[1]",'xpath')
            row.date1 = self.methods.GetElementAttributeText('value',f"((//td[contains(text(), 'Default Dates')]//tbody//tr)[{i}]//input)[1]",'xpath')
            row.date2 = self.methods.GetElementAttributeText('value',f"((//td[contains(text(), 'Default Dates')]//tbody//tr)[{i}]//input)[2]",'xpath')
            rows.append(row)

        checkboxes = []
        for i in range(1, self.methods.ReturnLengthOfElements("//input[@type='checkbox']", 'xpath') + 1):
            checkbox = model_succession_settings.checkboxes()
            checkbox.checkbox_description = self.methods.GetElementText(f"(//input[@type='checkbox']/..)[{i}]", 'xpath')
            value = self.methods.GetElementAttributeText('checked', f"(//input[@type='checkbox'])[{i}]", 'xpath')
            if value:
                checkbox.status = True
            else:
                checkbox.status = False
            checkboxes.append(checkbox)

        return rows, checkboxes

    def compare(self, sheet_data, checkboxes_on_sheet):
        red_cells = []
        green_cells = []
        sap_data, checkboxes_on_sap = self.getting_data_from_sap()
        sap_data = {i.name:i for i in sap_data}
        columns = [['date1','C'], ['date2','D']]
        for r in sheet_data:
            if r.name in sap_data:
                for c in columns:
                    if getattr(r, c[0]) != getattr(sap_data[r.name], c[0]):
                        red_cells.append(f"{c[1]}{int(r.itemid) + 1}")
                    else:
                        green_cells.append(f"{c[1]}{int(r.itemid) + 1}")
                sap_data.pop(r.name)
            else:
                red_cells+=[f"{chr(64 + i)}{int(r.itemid) + 1}" for i in range(3,5)]

        checkboxes_on_sap = {i.checkbox_description:i for i in checkboxes_on_sap}
        for i, r in enumerate(checkboxes_on_sheet, 2):
            if r.checkbox_description in checkboxes_on_sap:
                if checkboxes_on_sap[r.checkbox_description].status!=r.status:
                    red_cells.append(f"G{i}")
                else:
                    green_cells.append(f"G{i}")
                checkboxes_on_sap.pop(r.checkbox_description)
            else:
                red_cells.append(f"G{i}")
        return red_cells, green_cells

    def main_fun_run(self):
        sheet_data, checkboxes = self.controller.getting_sheet_data('Succession Settings','1-M4812qcUB5Lfyj2BRXqP0YqS-ywydvd0ZA3vhQNrCY')
        red_cells, green_cells = self.compare(sheet_data, checkboxes)
        self.controller.formating('Succession Settings','1-M4812qcUB5Lfyj2BRXqP0YqS-ywydvd0ZA3vhQNrCY', red_cells, green_cells)