import time
from selenium.webdriver import Keys
from contoller_emp_prof_standard import ControllerEmpProfStandard
import model_emp_profile_standard
from selenium import webdriver
from SeleniumHelperUtils import methods

class EmpProfStandardAutomation:
    def __init__(self, driver):
        self.driver = driver
        self.methods = methods(self.driver)
        self.controller = ControllerEmpProfStandard()
        self.sheet_data, self.names_status, self.permissions = self.controller.load_data('Emp Prof Standard',"1-M4812qcUB5Lfyj2BRXqP0YqS-ywydvd0ZA3vhQNrCY")
        scrb_id = '_s.crb' + self.driver.current_url.split('_s.crb')[1]
        employee_profile_standard_url = "https://hcm41preview.sapsf.com/xi/ui/businessconfig/pages/adminConfiguration.xhtml?&" + scrb_id
        self.driver.get(employee_profile_standard_url)
        self.methods.waitforElementTobeInvisible("overlayShim", 'class', 20)
        self.methods.wait_for_element_and_click("//a[text()='Employee Profile']", 'xpath', 30)
        self.methods.ClickElement("//a[text()='Standard']", 'xpath')

    def get_data_from_sap(self, name):
        self.methods.ClickElement(f"//a[text()='{name}']", 'xpath')
        self.methods.waitforElementTobeInvisible("overlayShim", 'class', 2)
        self.methods.handle_stale_element_error_and_click("//span[text()='Take Action']", 'xpath')
        self.methods.ClickElement("//a[text()='Make Correction']", 'xpath')

        row = model_emp_profile_standard.ModelEmpProfStandard()
        row.itemId = "=row()-1"
        row.identifier = name
        row.label = self.methods.GetElementAttributeText('value',"//span[text()='Label']//ancestor::tr[@class='form_field ']//input",'xpath') or ""
        row.default_label = self.methods.GetElementAttributeText('value',"//span[text()='Default Label']//ancestor::tr[@class='form_field ']//input",'xpath')
        row.enabled = self.methods.GetElementAttributeText('value',"//span[text()='Enabled']//ancestor::tr[@class='form_field ']//input",'xpath')
        row.maximum_length = self.methods.GetElementAttributeText('value',"//span[text()='Maximum Length']//ancestor::tr[@class='form_field ']//input",'xpath')
        row.picklist = self.methods.GetElementAttributeText('title',"//span[text()='Picklist']//ancestor::tr[@class='form_field ']//a",'xpath')
        if not row.picklist:
            row.picklist = self.methods.GetElementText("//span[text()='Picklist']//ancestor::tr[@class='form_field ']//a", 'xpath')

        row.parent_field_for_picklist = self.methods.GetElementAttributeText('title',"//span[text()='Parent Field for Picklist']//ancestor::tr[@class='form_field ']//input",'xpath')
        if not row.parent_field_for_picklist:
            row.parent_field_for_picklist = self.methods.GetElementAttributeText('value',"//span[text()='Parent Field for Picklist']//ancestor::tr[@class='form_field ']//input",'xpath')

        row.mandatory = self.methods.GetElementAttributeText('value',"//span[text()='Mandatory']//ancestor::tr[@class='form_field ']//input",'xpath')
        row.masked = self.methods.GetElementAttributeText('value',"//span[text()='Masked']//ancestor::tr[@class='form_field ']//input",'xpath')
        row.read_log_access = self.methods.GetElementAttributeText('value',"//span[text()='Log Read Access']//ancestor::tr[@class='form_field ']//input",'xpath')

        permissions = []
        length_of_permissions = self.methods.ReturnLengthOfElements("//input[@aria-label='Permission']", 'xpath')
        if length_of_permissions > 1:
            for i in range(1, length_of_permissions):
                permission_name = self.methods.GetElementAttributeText('value', f"(//input[@aria-label='Permission'])[{i}]", 'xpath')
                if permission_name != 'none':
                    permission = model_emp_profile_standard.ModelEmpProfStandardPermissions()
                    permission.itemId = i
                    permission.identifier = name
                    permission.permission = permission_name
                    permission.roll_type = self.methods.GetElementAttributeText('value',f"(//table[@aria-label='Element Permission']//tr//input[@type='text'])[{i}]",'xpath')
                    permissions.append(permission)
        return row, permissions

    def automate_permissions(self, permissions_on_sap, name):
        permissions_on_sheet = [i for i in self.permissions if i.identifier == name]
        if len(permissions_on_sheet)>0:
            if len(permissions_on_sap)==0:
                for i,v in enumerate(permissions_on_sheet, 1):
                    self.methods.ClickElement(f"(//table[@aria-label='Element Permission']//tr//span[contains(@class, 'toggle')])[{i}]",'xpath')
                    self.methods.ClickElement(f"//li//a[text()='{v.permission}']", 'xpath')
                    self.methods.EnterText(f"(//table[@aria-label='Element Permission']//tr//input[@type='text'])[{i}]",'xpath', v.roll_type)
            else:
                permissions_on_sap = {(i.identifier, i.permission):i for i in permissions_on_sap}
                for i, v in enumerate(permissions_on_sheet, 2):
                    key = (v.identifier, v.permission)
                    if key in permissions_on_sap:
                        if v.roll_type!=permissions_on_sap[key].roll_type:
                            self.methods.EnterText(f"(//table[@aria-label='Element Permission']//tr//input[@type='text'])[{permissions_on_sap[key].itemId}]",'xpath', v.roll_type)
                    else:
                        length = self.methods.ReturnLengthOfElements("//table[@aria-label='Element Permission']//tr", 'xpath')
                        self.methods.ClickElement(f"(//table[@aria-label='Element Permission']//tr//span[contains(@class, 'toggle')])[{length}]",'xpath')
                        self.methods.ClickElement(f"//li//a[text()='{v.permission}']", 'xpath')
                        self.methods.EnterText(f"(//table[@aria-label='Element Permission']//tr//input[@type='text'])[{length}]",'xpath', v.roll_type)
            self.save_and_handle_ok_button()

    def save_and_handle_ok_button(self):
        if not self.methods.GetElementAttributeText('disabled', "//button[text()='Save']", 'xpath'):
            self.methods.ClickElement("//button[text()='Save']", "xpath")
            self.methods.waitforElementTobeInvisible("overlayShim", 'class', 5)
            if self.methods.IsElementPresent("//button[text()='OK']", 'xpath'):
                self.methods.ClickElement("//button[text()='OK']", 'xpath')
                self.methods.ClickElement("//button[text()='Cancel']", 'xpath')
                self.methods.waitforElementTobeInvisible("overlayShim", 'class', 5)
                self.methods.ClickElement("//button[text()='Don’t Save']", 'xpath')
                self.methods.handle_stale_element_error_and_click("//span[text()='Take Action']", 'xpath')
                self.methods.ClickElement("//a[text()='Make Correction']", 'xpath')
            else:
                self.methods.handle_stale_element_error_and_click("//span[text()='Take Action']", 'xpath')
                self.methods.ClickElement("//a[text()='Make Correction']", 'xpath')

    def automate_identifiers(self, sap_data, name):
        sheet_data = [i for i in self.sheet_data if i.identifier==name][0]

        if sap_data.label!=sheet_data.label:
            self.methods.EnterText("//span[text()='Label']//ancestor::tr[@class='form_field ']//input", 'xpath',sheet_data.label)

        if sap_data.default_label!=sheet_data.default_label:
            self.methods.EnterText("//span[text()='Default Label']//ancestor::tr[@class='form_field ']//input", 'xpath', sheet_data.default_label)

        if sap_data.maximum_length!=sheet_data.maximum_length:
            self.methods.EnterText("//span[text()='Maximum Length']//ancestor::tr[@class='form_field ']//input", 'xpath', sheet_data.maximum_length)

        if sap_data.enabled!=sheet_data.enabled:
            self.methods.ClickElement("//span[text()='Enabled']//ancestor::tr[@class='form_field ']//span[contains(@class, 'toggle')]", 'xpath')
            self.methods.ClickElement(f"//li//a[text()='{sheet_data.enabled}']", 'xpath')

        if sap_data.masked!=sheet_data.masked:
            self.methods.ClickElement("//span[text()='Masked']//ancestor::tr[@class='form_field ']//span[contains(@class, 'toggle')]", 'xpath')
            self.methods.ClickElement(f"//li//a[text()='{sheet_data.masked}']", 'xpath')

        if sap_data.picklist!=sheet_data.picklist:
            self.methods.ClickElement("//span[text()='Picklist']//ancestor::tr[@class='form_field ']//a", 'xpath')
            time.sleep(1)
            self.methods.ClickElement(f"//li//a[text()='{sheet_data.picklist}']", 'xpath')
        self.save_and_handle_ok_button()

        if sap_data.parent_field_for_picklist!=sheet_data.parent_field_for_picklist:
            self.methods.ClickElement("//span[text()='Parent Field for Picklist']//ancestor::tr[@class='form_field ']//span[contains(@class, 'toggle')]",'xpath')
            p_picklist = self.methods.GetListofElementText("//li//a", 'xpath')
            if sheet_data.parent_field_for_picklist in p_picklist:
                self.methods.ClickElement(f"//li//a[@title='{sheet_data.parent_field_for_picklist}']", 'xpath')
            else:
                for i in range(25):
                    last_element = p_picklist[-1]
                    self.methods.ScrolltoView(f"//li//a[@title='{last_element}']", 'xpath')
                    time.sleep(5)
                    p_picklist = self.methods.GetListofElementText("//li//a", 'xpath')

                    if sheet_data.parent_field_for_picklist in p_picklist:
                        self.methods.ClickElement(f"//li//a[@title='{sheet_data.parent_field_for_picklist}']", 'xpath')
                        break

                    if p_picklist[-1] == last_element:
                        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                        break
            self.save_and_handle_ok_button()

        if sap_data.mandatory!=sheet_data.mandatory:
            self.methods.ClickElement("//span[text()='Mandatory']//ancestor::tr[@class='form_field ']//span[contains(@class, 'toggle')]",'xpath')
            self.methods.ClickElement(f"//li//a[text()='{sheet_data.mandatory}']", 'xpath')
            self.save_and_handle_ok_button()

        if sap_data.log_read_access.lower()!=sheet_data.log_read_access.lower():
            self.methods.ClickElement("//span[text()='Log Read Access']//ancestor::tr[@class='form_field ']//span[contains(@class, 'toggle')]",'xpath')
            self.methods.ClickElement(f"//li//a[text()='{sheet_data.log_read_access.title()}']", 'xpath')
            self.save_and_handle_ok_button()

    def main_fun_run(self):
        names  = [i.identifier for i in self.names_status if i.status=='Pending']
        print(f"All Names: {names}")
        for name in names:
            print(f"name: {name}")
            sap_data, permissions_on_sap = self.get_data_from_sap(name)
            self.automate_identifiers(sap_data, name)
            self.automate_permissions(permissions_on_sap, name)