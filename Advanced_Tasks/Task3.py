from SeleniumHelperUtils import methods
import model_rating_scale
from controller_rating_scale import Controller_RatingScale

class RatingScaleValidation:
    def __init__(self, driver):
        self.methods = methods(driver)
        self.controller = Controller_RatingScale()
        self.names_status, self.sheet_data = self.controller.load_data("Rating Scale", "1-M4812qcUB5Lfyj2BRXqP0YqS-ywydvd0ZA3vhQNrCY")
        scrb_id = '_s.crb' + driver.current_url.split('_s.crb')[1]
        rating_scale_url = "https://hcm41preview.sapsf.com/acme?fbacme_o=admin&pess_old_admin=true&ap_param_action=form_rating_scale&" + scrb_id
        driver.get(rating_scale_url)

    def handling_ok_button(self):
        if self.methods.IsElementPresent("//button[text()='OK']", 'xpath'):
            self.methods.ClickElement("//button[text()='OK']", 'xpath')

    def get_rows_from_sap(self, name):
        names = self.methods.GetListofElementText("//span[@title='Name of the rating scale.']//a", 'xpath')
        if name in names:
            self.methods.ClickElement(f"//a[text()='{name}']", 'xpath')
            self.handling_ok_button()
            rows = []
            for i in range(1,self.methods.ReturnLengthOfElements("//span[contains(@title, 'The numerical value')]//input",'xpath') + 1):
                row = model_rating_scale.Model_RatingScale()
                row.name = self.methods.GetElementAttributeText('value', '//input[@data-testid="sfTextField"]', 'xpath')
                row.description = self.methods.GetElementAttributeText('value',"//span[@class='ratingScaleTextArea']//textarea",'xpath')
                row.score = self.methods.GetElementAttributeText('value',f"(//span[contains(@title, 'The numerical value')]//input)[{i}]",'xpath')
                row.label = self.methods.GetElementAttributeText('value',f"(//span[contains(@title,'The short title')]//input)[{i}]",'xpath')
                row.score_description = self.methods.GetElementText(f"(//span[contains(@title,'The description of the rating')]//textarea)[{i}]", 'xpath')
                rows.append(row)
            self.methods.ClickElement("//a[text()='Rating Scale Designer']", 'xpath')
            return rows
        else:
            print("Name not available at SAP")
            return False

    def compare(self, name, red_cells, green_cells):
        rows_on_sap = self.get_rows_from_sap(name)
        rows_on_sheet = [i for i in self.sheet_data if i.name==name]

        if rows_on_sap and len(rows_on_sap) <= len(rows_on_sheet):
            rows_on_sap = {(i.name, i.score):i for i in rows_on_sap}
            columns = [['name', 'B'], ['description', 'C'], ['score', 'D'], ['label', 'E'], ['score_description', 'F']]
            for r in rows_on_sheet:
                key = (r.name, str(r.score))
                if key in rows_on_sap:
                    for c in columns:
                        if getattr(r, c[0]) != getattr(rows_on_sap[key], c[0]):
                            red_cells.append(f"{c[1]}{int(r.itemid) + 1}")
                        else:
                            green_cells.append(f"{c[1]}{int(r.itemid) + 1}")
                    rows_on_sap.pop(key)
                else:
                    red_cells+=[f"{chr(64 + i)}{int(r.itemid) + 1}" for i in range(2, 7)]
            return red_cells, green_cells

    def main_fun_run(self):
        pending_names = [v.name for v in self.names_status if v.status=='Pending']
        if len(pending_names)>=1:
            red_cells = []
            green_cells = []
            for name in pending_names:
                red_cells,green_cells = self.compare(name, red_cells, green_cells)

            self.controller.formating('Rating Scale','1-M4812qcUB5Lfyj2BRXqP0YqS-ywydvd0ZA3vhQNrCY', red_cells, green_cells)
            self.controller.update_status_rating_scale('Rating Scale','1-M4812qcUB5Lfyj2BRXqP0YqS-ywydvd0ZA3vhQNrCY', self.names_status)