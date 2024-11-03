from selenium import webdriver
from SeleniumHelperUtils import methods

class Task1:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        self.methods = methods(self.driver)

    def get_scrb_id(self):
        self.methods.SapLogin('configs.txt')
        scrb_id = '_s.crb' + self.driver.current_url.split('_s.crb')[1]
        print(scrb_id)

        rating_scale_link = "https://hcm41preview.sapsf.com/acme?fbacme_o=admin&pess_old_admin=true&ap_param_action=form_rating_scale&" + scrb_id
        self.driver.get(rating_scale_link)

task1 = Task1("https://hcm41preview.sapsf.com")
task1.get_scrb_id()
