from selenium import webdriver
from SeleniumHelperUtils import methods
import model_succession_settings
from controller_succession_settings import Controller_SuccessionSettings

class SuccessionSettingsScrapper:
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

    def main_fun_run(self):
        data, checkboxes = self.getting_data_from_sap()
        self.controller.fill_succession_settings("Succession Settings", data,'1-M4812qcUB5Lfyj2BRXqP0YqS-ywydvd0ZA3vhQNrCY')
        self.controller.fill_succession_settings_checkboxes("Succession Settings", checkboxes,'1-M4812qcUB5Lfyj2BRXqP0YqS-ywydvd0ZA3vhQNrCY')
