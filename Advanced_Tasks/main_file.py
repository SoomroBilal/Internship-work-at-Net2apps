from selenium import webdriver
from SeleniumHelperUtils import methods
class MainFile:
    def __init__(self, url):
        self.screen = input("Screen from (Rating Scale, Succession Settings, Emp Prof Standard): ")
        self.task = input("Select task from (Scrapping, Automation, Validation): ")
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        self.methods = methods(self.driver)
        self.methods.SapLogin('configs.txt')

    def navigation(self):
        if self.screen=="Rating Scale" and self.task == "Scrapping":
            from Task2 import RatingScaleScrapper
            obj = RatingScaleScrapper(self.driver)
            obj.main_fun_run()

        elif self.screen=="Rating Scale" and self.task == "Validation":
            from Task3 import RatingScaleValidation
            obj = RatingScaleValidation(self.driver)
            obj.main_fun_run()

        elif self.screen=="Rating Scale" and self.task == "Automation":
            from Task4 import RatingScaleAutomation
            obj = RatingScaleAutomation(self.driver)
            obj.main_fun_run()

        elif self.screen=="Succession Settings" and self.task =="Scrapping":
            from Task6 import SuccessionSettingsScrapper
            obj = SuccessionSettingsScrapper(self.driver)
            obj.main_fun_run()

        elif self.screen == "Succession Settings" and self.task == "Automation":
            from Task7 import SuccessionSettingsAutomation
            obj = SuccessionSettingsAutomation(self.driver)
            obj.main_fun_run()

        elif self.screen == "Succession Settings" and self.task == "Validation":
            from Task8 import SuccessionSettingsValidation
            obj = SuccessionSettingsValidation(self.driver)
            obj.main_fun_run()

        elif self.screen == "Emp Prof Standard" and self.task == "Scrapping":
            from Task10 import EmpProfStandardScrapper
            obj = EmpProfStandardScrapper(self.driver)
            obj.main_fun_run()

        elif self.screen == "Emp Prof Standard" and self.task == "Automation":
            from Task11 import EmpProfStandardAutomation
            obj = EmpProfStandardAutomation(self.driver)
            obj.main_fun_run()

        elif self.screen == "Emp Prof Standard" and self.task == "Validation":
            from Task12 import EmpProfStandardValidation
            obj = EmpProfStandardValidation(self.driver)
            obj.main_fun_run()

main_obj = MainFile("https://hcm41preview.sapsf.com")
main_obj.navigation()