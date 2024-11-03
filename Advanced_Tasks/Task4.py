from SeleniumHelperUtils import methods
import model_rating_scale
from controller_rating_scale import Controller_RatingScale

class RatingScaleAutomation:
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
        self.methods.ClickElement(f"//a[text()='{name}']", 'xpath')
        self.handling_ok_button()
        rows = []
        for i in range(1, self.methods.ReturnLengthOfElements("//span[contains(@title, 'The numerical value')]//input",'xpath')+1):
            row = model_rating_scale.Model_RatingScale()
            row.name = self.methods.GetElementAttributeText('value', '//input[@data-testid="sfTextField"]', 'xpath')
            row.description = self.methods.GetElementAttributeText('value', "//span[@class='ratingScaleTextArea']//textarea", 'xpath')
            row.score = self.methods.GetElementAttributeText('value',f"(//span[contains(@title, 'The numerical value')]//input)[{i}]",'xpath')
            row.label = self.methods.GetElementAttributeText('value',f"(//span[contains(@title,'The short title')]//input)[{i}]",'xpath')
            row.score_description = self.methods.GetElementText(f"(//span[contains(@title,'The description of the rating')]//textarea)[{i}]", 'xpath')
            rows.append(row)
        return rows

    def add_new_score(self, r):
        scores = self.methods.ReturnLengthOfElements("//span[contains(@title, 'The numerical value')]//input", 'xpath')
        if not scores:
            scores=0
        self.methods.ClickElement("//a[text()='Add New Score']", 'xpath')
        self.methods.EnterText(f"(//span[contains(@title, 'The numerical value')]//input)[{scores + 1}]",'xpath', r.score)
        self.methods.EnterText(f"(//span[contains(@title,'The short title')]//input)[{scores + 1}]", 'xpath',r.label)
        self.methods.EnterText(f"(//span[contains(@title,'The description of the rating')]//textarea)[{scores + 1}]", 'xpath',r.score_description)

    def updating_extra_rows(self, name):
        rows_on_sap = self.get_rows_from_sap(name)
        rows_on_sheet = [i for i in self.sheet_data if i.name==name]

        if rows_on_sap and len(rows_on_sap) <= len(rows_on_sheet):
            if rows_on_sap[0].description != rows_on_sheet[0].description:
                self.methods.EnterText("//span[@class='ratingScaleTextArea']//textarea", 'xpath',rows_on_sheet[0].description)

            rows_on_sap = {(i.name, i.score): i for i in rows_on_sap}
            for i, r in enumerate(rows_on_sheet,1):
                key = (r.name, str(r.score))
                if key in rows_on_sap:
                    if r.score != rows_on_sap[key].score:
                        self.methods.EnterText(f"(//span[contains(@title, 'The numerical value')]//input)[{i}]",'xpath', r.score)

                    if r.label != rows_on_sap[key].label:
                        self.methods.EnterText(f"(//span[contains(@title,'The short title')]//input)[{i}]", 'xpath',r.label)

                    if r.score_description != rows_on_sap[key].score_description:
                        self.methods.EnterText(f"(//span[contains(@title,'The description of the rating')]//textarea)[{i}]", 'xpath',r.score_description)
                else:
                    self.add_new_score(r)
            self.methods.ClickElement("//a//span[text()='Save']", 'xpath')
        self.methods.waitforElementTobeInvisible("overlayShim", 'class', 2)
        self.methods.ClickElement("//a[text()='Rating Scale Designer']", 'xpath')

    def add_new_rating_scale(self, name):
        rows = [i for i in self.sheet_data if i.name==name]
        self.methods.ClickElement("//span[text()='Create New Rating Scale']",'xpath')
        self.methods.EnterText("//input[@data-testid='sfTextField']", 'xpath', rows[0].name)
        self.methods.EnterText("//span[@class='ratingScaleTextArea']//textarea", 'xpath', rows[0].description)
        self.methods.ClickElement("//a//span[text()='Save']", 'xpath')

        for i in range(1, self.methods.ReturnLengthOfElements("//a[@rel='noopener noreferrer']", 'xpath')):
            self.methods.ClickElement(f"(//a[@rel='noopener noreferrer'])[1]", 'xpath')

        for r in rows:
            self.add_new_score(r)

        self.methods.ClickElement("//a//span[text()='Save']", 'xpath')
        self.methods.waitforElementTobeInvisible("overlayShim", 'class', 2)
        self.methods.ClickElement("//a[text()='Rating Scale Designer']", 'xpath')

    def main_fun_run(self):
        names_on_sheet = [n.name for n in self.names_status]
        print(f"Names on sheet: {names_on_sheet}")
        names_on_sap = self.methods.GetListofElementText("//span[@title='Name of the rating scale.']//a", 'xpath')
        names_on_sheet = ['New Rating Scale test']
        for name in names_on_sheet:
            if name in names_on_sap:
                self.updating_extra_rows(name)
            else:
                if name!='':
                    self.add_new_rating_scale(name)