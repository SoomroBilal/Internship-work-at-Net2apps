import time
from selenium.webdriver import Keys
from contoller_emp_prof_standard import ControllerEmpProfStandard
import model_emp_profile_standard
from selenium import webdriver
from SeleniumHelperUtils import methods

class EmpProfStandardScrapper:
    def __init__(self, driver):
        self.driver = driver
        self.methods = methods(driver)
        self.controller = ControllerEmpProfStandard()
        scrb_id = '_s.crb' + driver.current_url.split('_s.crb')[1]
        employee_profile_standard_url = "https://hcm41preview.sapsf.com/xi/ui/businessconfig/pages/adminConfiguration.xhtml?&" + scrb_id
        self.driver.get(employee_profile_standard_url)
        self.driver.implicitly_wait(10)
        self.methods.waitforElementTobeInvisible("overlayShim", 'class', 20)
        self.methods.wait_for_element_and_click("//a[text()='Employee Profile']", 'xpath', 30)
        self.methods.ClickElement("//a[text()='Standard']", 'xpath')

    def get_data_from_sap(self, dropdowns_data):
        identifier_rows = []
        permissions = []
        names = self.methods.GetListofElementText("(//a[text()='addressLine1']//ancestor::table[@class='leftNavItemsTableNarrow'])[2]//tr", 'xpath')
        for name in names:
            self.methods.ClickElement(f"//a[text()='{name}']", 'xpath')
            self.methods.waitforElementTobeInvisible("overlayShim", 'class', 2)
            self.methods.handle_stale_element_error_and_click("//span[text()='Take Action']", 'xpath')
            self.methods.ClickElement("//a[text()='Make Correction']", 'xpath')

            row = model_emp_profile_standard.ModelEmpProfStandard()
            row.itemId = "=row()-1"
            row.identifier = name
            row.label = self.methods.GetElementAttributeText('value', "//span[text()='Label']//ancestor::tr[@class='form_field ']//input", 'xpath') or ""
            row.default_label = self.methods.GetElementAttributeText('value', "//span[text()='Default Label']//ancestor::tr[@class='form_field ']//input", 'xpath')
            row.enabled =  self.methods.GetElementAttributeText('value', "//span[text()='Enabled']//ancestor::tr[@class='form_field ']//input", 'xpath')
            row.maximum_length = self.methods.GetElementAttributeText('value', "//span[text()='Maximum Length']//ancestor::tr[@class='form_field ']//input", 'xpath')
            row.picklist = self.methods.GetElementAttributeText('title', "//span[text()='Picklist']//ancestor::tr[@class='form_field ']//a", 'xpath')
            if not row.picklist:
                row.picklist = self.methods.GetElementText( "//span[text()='Picklist']//ancestor::tr[@class='form_field ']//a", 'xpath')

            row.parent_field_for_picklist = self.methods.GetElementAttributeText('title',"//span[text()='Parent Field for Picklist']//ancestor::tr[@class='form_field ']//input",'xpath')
            if not row.parent_field_for_picklist:
                row.parent_field_for_picklist = self.methods.GetElementAttributeText('value',"//span[text()='Parent Field for Picklist']//ancestor::tr[@class='form_field ']//input",'xpath')

            row.mandatory = self.methods.GetElementAttributeText('value', "//span[text()='Mandatory']//ancestor::tr[@class='form_field ']//input",'xpath')
            row.masked = self.methods.GetElementAttributeText('value', "//span[text()='Masked']//ancestor::tr[@class='form_field ']//input",'xpath')
            row.log_read_access = self.methods.GetElementAttributeText('value', "//span[text()='Log Read Access']//ancestor::tr[@class='form_field ']//input",'xpath')
            identifier_rows.append(row)

            length_of_permissions = self.methods.ReturnLengthOfElements("//input[@aria-label='Permission']", 'xpath')
            if length_of_permissions>1:
                for i in range(1, length_of_permissions):
                    permission_name  = self.methods.GetElementAttributeText('value',f"(//input[@aria-label='Permission'])[{i}]",'xpath')
                    if permission_name!='none':
                       permission = model_emp_profile_standard.ModelEmpProfStandardPermissions()
                       permission.itemId = "=row()-1"
                       permission.identifier = name
                       permission.permission = permission_name
                       permission.roll_type = self.methods.GetElementAttributeText('value',f"(//table[@aria-label='Element Permission']//tr//input[@type='text'])[{i}]",'xpath')
                       permissions.append(permission)
        return identifier_rows,permissions

    def add_drop_downs(self):
        data = model_emp_profile_standard.ModelEmpProfStandardDropDowns()
        data.names = self.methods.GetListofElementText("(//a[text()='addressLine1']//ancestor::table[@class='leftNavItemsTableNarrow'])[2]//tr", 'xpath')

        self.methods.ClickElement(f"//a[text()='{data.names[0]}']", 'xpath')

        self.methods.waitforElementTobeInvisible("overlayShim", 'class', 5)
        self.methods.handle_stale_element_error_and_click("//span[text()='Take Action']", 'xpath')
        self.methods.ClickElement("//a[text()='Make Correction']", 'xpath')

        self.methods.ClickElement("//span[text()='Enabled']//ancestor::tr[@class='form_field ']//span[contains(@class, 'toggle')]",'xpath')
        data.enabled = self.methods.GetListofElementText("//li//a", 'xpath')
        self.methods.ClickElement("//span[text()='Enabled']//ancestor::tr[@class='form_field ']//span[contains(@class, 'toggle')]",'xpath')

        self.methods.ClickElement("//span[text()='Picklist']//ancestor::tr[@class='form_field ']//a", 'xpath')
        time.sleep(1)
        current_value = self.methods.GetElementText("//span[text()='Picklist']//ancestor::tr[@class='form_field ']//a", 'xpath')
        data.picklist = self.methods.GetListofElementText("//li//a", 'xpath')[:500]
        self.methods.ClickElement(f"//li//a[text()='{current_value}']", 'xpath')

        self.methods.ClickElement("//span[text()='Parent Field for Picklist']//ancestor::tr[@class='form_field ']//span[contains(@class,'toggle' )]", 'xpath')
        p_picklist = self.methods.GetListofElementText("//li//a", 'xpath')
        for i in range(25):
            last_element = p_picklist[-1]
            self.methods.ScrolltoView(f"//li//a[@title='{last_element}']", 'xpath')
            time.sleep(5)
            p_picklist = self.methods.GetListofElementText("//li//a", 'xpath')
            if p_picklist[-1]==last_element:
                break
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        data.parent_field_for_picklist = ['No Selection'] + p_picklist

        current_value = self.methods.GetElementAttributeText('value',"//span[text()='Mandatory']//ancestor::tr[@class='form_field ']//input",'xpath')
        self.methods.ClickElement("//span[text()='Mandatory']//ancestor::tr[@class='form_field ']//span[contains(@class, 'toggle')]", 'xpath')
        data.mandatory = self.methods.GetListofElementText("//li//a", 'xpath')
        self.methods.ClickElement(f"//li//a[text()='{current_value}']", 'xpath')

        current_value = self.methods.GetElementAttributeText('value',"//span[text()='Masked']//ancestor::tr[@class='form_field ']//input",'xpath')
        self.methods.ClickElement("//span[text()='Masked']//ancestor::tr[@class='form_field ']//span[contains(@class, 'toggle')]", 'xpath')
        data.masked = self.methods.GetListofElementText("//li//a", 'xpath')
        self.methods.ClickElement(f"//li//a[text()='{current_value}']", 'xpath')

        current_value = self.methods.GetElementAttributeText('value',"//span[text()='Log Read Access']//ancestor::tr[@class='form_field ']//input",'xpath')
        self.methods.ClickElement("//span[text()='Log Read Access']//ancestor::tr[@class='form_field ']//span[contains(@class, 'toggle')]", 'xpath')
        log_read_access = self.methods.GetListofElementText("//li//a", 'xpath')
        data.log_read_access = [i.upper() if i in ['True', 'False'] else i for i in log_read_access]
        self.methods.ClickElement(f"//li//a[text()='{current_value}']", 'xpath')
        return data

    def main_fun_run(self):
        dropdowns = self.add_drop_downs()
        rows, permissions = self.get_data_from_sap(dropdowns)
        self.controller.fill_emp_prof_stand_Dropdowns(dropdowns, "testing", "1-M4812qcUB5Lfyj2BRXqP0YqS-ywydvd0ZA3vhQNrCY")
        self.controller.fill_emp_prof(rows, 'testing', "1-M4812qcUB5Lfyj2BRXqP0YqS-ywydvd0ZA3vhQNrCY")
        self.controller.fill_permissions(permissions, 'testing', "1-M4812qcUB5Lfyj2BRXqP0YqS-ywydvd0ZA3vhQNrCY")

