from selenium import webdriver
from SeleniumHelperUtils import methods
import model_succession_settings
from controller_succession_settings import Controller_SuccessionSettings

class SuccessionSettingsAutomation:
    def __init__(self, driver):
        self.methods = methods(driver)
        self.controller = Controller_SuccessionSettings()
        scrb_id = '_s.crb' + driver.current_url.split('_s.crb')[1]
        succession_setting_url = "https://hcm41preview.sapsf.com/acme?fbacme_o=admin&pess_old_admin=true&ap_param_action=succession_settings&itrModule=talent&" + scrb_id
        driver.get(succession_setting_url)

    def getting_data_from_sap(self):
        rows = []
        for i in range(1, self.methods.ReturnLengthOfElements("//td[contains(text(), 'Default Dates')]//tbody//tr", 'xpath') + 1):
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

    def automate(self, sheet_data, checkboxes_on_sheet):
        sap_data, checkboxes_on_sap = self.getting_data_from_sap()
        sap_data = {i.name:i for i in sap_data}
        if len(sap_data)<=len(sheet_data):
            counter = 1
            for r in sheet_data:
                if r.name in sap_data:
                    if sap_data[r.name].date1!=r.date1:
                        self.methods.EnterText(f"((//td[contains(text(), 'Default Dates')]//tbody//tr)[{counter}]//input)[1]", 'xpath',r.date1)

                    if sap_data[r.name].date2!=r.date2:
                        self.methods.EnterText(f"((//td[contains(text(), 'Default Dates')]//tbody//tr)[{counter}]//input)[2]",'xpath', r.date2)
                    sap_data.pop(r.name)
                    counter+=1
                else:
                    print(f"'{r.name}' is not live profile")

            checkboxes_on_sap = {i.checkbox_description:i for i in checkboxes_on_sap}
            counter = 1
            for r in checkboxes_on_sheet:
                if r.checkbox_description in checkboxes_on_sap:
                    if checkboxes_on_sap[r.checkbox_description].status!=r.status:
                        self.methods.ClickElement(f"(//input[@type='checkbox'])[{counter}]", 'xpath')
                    checkboxes_on_sap.pop(r.checkbox_description)
                    counter+=1
                else:
                    print(f"Checkbox description '{r.checkbox_description}' is not available")
        self.methods.ClickElement("//button[contains(text(),'Save')]", 'xpath')

    def main_fun_run(self):
        sheet_data, checkboxes_on_sheet = self.controller.getting_sheet_data('Succession Settings','1-M4812qcUB5Lfyj2BRXqP0YqS-ywydvd0ZA3vhQNrCY')
        self.automate(sheet_data, checkboxes_on_sheet)