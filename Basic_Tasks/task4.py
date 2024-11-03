from selenium import webdriver
import time
from SeleniumHelperUtils import methods
import save_data_methods

class DataScraper:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        self.methods = methods(self.driver)

    def load_more(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    def filtrate(self):
        self.methods.HoverOverElement("(//a[text()='Community'])[1]", 'xpath')
        self.methods.ClickElement("//div[text()='Streaks']", 'xpath')

        for i in range(150):
            self.load_more()
            items = len(self.methods.GetElements("//div[@class='my-5 flex flex-row items-center justify-center gap-3 px-2']", 'xpath'))
            if items>=150:
                break

    def collect_data(self):
        self.filtrate()
        names = self.methods.GetListofElementText("//div[@class='text-16 font-semibold text-dark-gray']", 'xpath')[:150]
        streaks = self.methods.GetListofElementText("//div[@class='text-14 font-normal text-light-gray']", 'xpath')[:150]
        streaks = [int(s.split()[1]) for s in streaks]
        data = {'Name':names, 'Streak':streaks}
        save_data_methods.save_data_as_xlsx("Streaks_Data", data)

scraper = DataScraper("https://www.producthunt.com")
scraper.collect_data()