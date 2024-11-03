from SeleniumHelperUtils import methods
import model_rating_scale
from controller_rating_scale import Controller_RatingScale

class RatingScaleScrapper:
    def __init__(self, driver):
        scrb_id = '_s.crb' + driver.current_url.split('_s.crb')[1]
        rating_scale_url = "https://hcm41preview.sapsf.com/acme?fbacme_o=admin&pess_old_admin=true&ap_param_action=form_rating_scale&" + scrb_id
        driver.get(rating_scale_url)
        self.methods = methods(driver)
        self.contoller = Controller_RatingScale()

    def handling_ok_button(self):
        if self.methods.IsElementPresent("//button[text()='OK']", 'xpath'):
            self.methods.ClickElement("//button[text()='OK']", 'xpath')

    def collect_data(self,names):
        rows = []
        for name in names:
            self.methods.ClickElement(f"//a[text()='{name}']", 'xpath')
            self.handling_ok_button()
            for j in range(1, self.methods.ReturnLengthOfElements("//span[contains(@title, 'The numerical value')]//input", 'xpath') + 1):
                row = model_rating_scale.Model_RatingScale()
                row.itemid = "=row()-1"
                row.name = self.methods.GetElementAttributeText('value', '//input[@data-testid="sfTextField"]','xpath')
                row.description = self.methods.GetElementAttributeText('value',"//span[@class='ratingScaleTextArea']//textarea",'xpath')
                row.score = self.methods.GetElementAttributeText('value',f"(//span[contains(@title, 'The numerical value')]//input)[{j}]",'xpath')
                row.label = self.methods.GetElementAttributeText('value',f"(//span[contains(@title,'The short title')]//input)[{j}]",'xpath')
                row.score_description = self.methods.GetElementText(f"(//span[contains(@title,'The description of the rating')]//textarea)[{j}]", 'xpath')
                rows.append(row)
            self.methods.ClickElement("//a[text()='Rating Scale Designer']", 'xpath')
        return rows

    def main_fun_run(self):
        names = self.methods.GetListofElementText("//span[@title='Name of the rating scale.']//a",'xpath')
        rows = self.collect_data(names[:3])
        self.contoller.fill_rating_scale(rows,'test','1-M4812qcUB5Lfyj2BRXqP0YqS-ywydvd0ZA3vhQNrCY')
        self.contoller.fill_rating_names(rows, 'test', '1-M4812qcUB5Lfyj2BRXqP0YqS-ywydvd0ZA3vhQNrCY')