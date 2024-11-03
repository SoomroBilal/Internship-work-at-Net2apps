from selenium import webdriver
from SeleniumHelperUtils import methods
import save_data_methods

class DataScraper:

    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.methods = methods(self.driver)

    def collect_data(self):
        countries = self.methods.GetListofElementText("//h3[@class='country-name']", 'xpath')
        capital = self.methods.GetListofElementText("//span[@class='country-capital']", 'xpath')
        population = self.methods.GetListofElementText("//span[@class='country-population']", 'xpath')
        area = self.methods.GetListofElementText("//span[@class='country-area']", 'xpath')

        data = {'Country':countries, 'Capital City':capital, 'Population':population, 'Area(km:Sq)': area}
        save_data_methods.save_data_as_csv("Country_Data", data)

scraper = DataScraper("https://www.scrapethissite.com/pages/simple")
scraper.collect_data()
