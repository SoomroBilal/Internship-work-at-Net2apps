from contoller_emp_prof_standard import ControllerEmpProfStandard
import model_emp_profile_standard
from SeleniumHelperUtils import methods

class EmpProfStandardValidation:
    def __init__(self, driver):
        self.driver = driver
        self.methods = methods(self.driver)
        self.controller = ControllerEmpProfStandard()
        scrb_id = '_s.crb' + self.driver.current_url.split('_s.crb')[1]
        employee_profile_standard_url = "https://hcm41preview.sapsf.com/xi/ui/businessconfig/pages/adminConfiguration.xhtml?&" + scrb_id
        self.driver.get(employee_profile_standard_url)
        self.driver.implicitly_wait(10)
        self.methods.waitforElementTobeInvisible("overlayShim", 'class', 20)
        self.methods.wait_for_element_and_click("//a[text()='Employee Profile']", 'xpath', 30)
        self.methods.ClickElement("//a[text()='Standard']", 'xpath')

        self.methods = methods(self.driver)
        self.controller = ControllerEmpProfStandard()
        self.sheet_data, self.names_status, self.permissions = self.controller.load_data('Emp Prof Standard',"1-M4812qcUB5Lfyj2BRXqP0YqS-ywydvd0ZA3vhQNrCY")

    def get_data_from_sap(self, name):
        self.methods.ClickElement(f"//a[text()='{name}']", 'xpath')
        self.methods.waitforElementTobeInvisible("overlayShim", 'class', 2)
        self.methods.handle_stale_element_error_and_click("//span[text()='Take Action']", 'xpath')
        self.methods.ClickElement("//a[text()='Make Correction']", 'xpath')

        row = model_emp_profile_standard.ModelEmpProfStandard()
        row.itemId = "=row()-1"
        row.identifier = self.methods.GetListofElementText("//span[text()='Identifier']//ancestor::tr[@class='form_field ']//span[@class=' ectTextAreaWrapperOldValueContainer']", 'xpath')
        print(f"Name on sap: {row.identifier}")
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
        row.log_read_access = self.methods.GetElementAttributeText('value',"//span[text()='Log Read Access']//ancestor::tr[@class='form_field ']//input",'xpath')

        permissions = []
        length_of_permissions = self.methods.ReturnLengthOfElements("//input[@aria-label='Permission']", 'xpath')
        if length_of_permissions > 1:
            for i in range(1, length_of_permissions):
                permission_name = self.methods.GetElementAttributeText('value',f"(//input[@aria-label='Permission'])[{i}]",'xpath')
                if permission_name != 'none':
                    permission = model_emp_profile_standard.ModelEmpProfStandardPermissions()
                    permission.itemId = i
                    permission.identifier = name
                    permission.permission = permission_name
                    permission.roll_type = self.methods.GetElementAttributeText('value',f"(//table[@aria-label='Element Permission']//tr//input[@type='text'])[{i}]",'xpath')
                    permissions.append(permission)
        return row, permissions

    def compare_identifiers_data(self, name, sap_data, red_cells, green_cells):
        sheet_data = [i for i in self.sheet_data if i.identifier==name][0]
        print(f"Sheet_data: {sheet_data.identifier}")
        columns = [['identifier', 'B'], ['label', 'C'], ['default_label', 'D'], ['enabled', 'E'],  ['maximum_length', 'F'], ['picklist', 'G'], ['parent_field_for_picklist', 'H'], ['mandatory', 'I'],  ['masked', 'J'], ['log_read_access', 'K']]
        for c in columns:
            if getattr(sheet_data, c[0]) != getattr(sap_data, c[0]):
                red_cells.append(f"{c[1]}{int(sheet_data.itemId) + 1}")
            else:
                green_cells.append(f"{c[1]}{int(sheet_data.itemId) + 1}")
        return red_cells, green_cells

    def compare_permissions(self, name, sap_permissions, red_cells, green_cells):
        permissions_on_sheet = [i for i in self.permissions if i.identifier == name]
        if len(permissions_on_sheet) > 0:
            columns = [['identifier', 'M'], ['permission', 'N'], ['roll_type', 'O']]
            if len(sap_permissions) == 0:
                for i in permissions_on_sheet:
                    red_cells+=[f"{c[1]}{int(i.itemId) + 1}" for c in columns]
            else:
                permissions_on_sap = {(i.identifier, i.permission): i for i in sap_permissions}
                for v in permissions_on_sheet:
                    key = (v.identifier, v.permission)
                    if key in permissions_on_sap:
                        for c in columns:
                            if getattr(v, c[0]) != getattr(permissions_on_sap[key], c[0]):
                                red_cells+=[f"{c[1]}{int(v.itemId) + 1}" for c in columns]
                            else:
                                green_cells+=[f"{c[1]}{int(v.itemId) + 1}" for c in columns]
                    else:
                        red_cells+=[f"{c[1]}{int(v.itemId) + 1}" for c in columns]

        return red_cells, green_cells

    def main_fun_run(self):
        red_cells, green_cells = [], []
        names  = [i.identifier for i in self.names_status if i.status=='Pending']
        for name in names:
            sap_data, sap_permissions = self.get_data_from_sap(name)
            red_cells, green_cells = self.compare_identifiers_data(name, sap_data, red_cells, green_cells)
            red_cells, green_cells = self.compare_permissions(name, sap_permissions, red_cells, green_cells)
            self.controller.formating('Emp Prof Standard', "1-M4812qcUB5Lfyj2BRXqP0YqS-ywydvd0ZA3vhQNrCY", red_cells, green_cells)
            self.controller.update_status_rating_scale('Emp Prof Standard', "1-M4812qcUB5Lfyj2BRXqP0YqS-ywydvd0ZA3vhQNrCY", self.names_status)