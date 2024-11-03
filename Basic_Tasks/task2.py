from selenium import webdriver
from SeleniumHelperUtils import methods
import save_data_methods

class DataScraper:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        self.methods = methods(self.driver)

    def collect_data(self):
        header = self.methods.GetListofElementText("//th",'xpath')
        data = {h:[] for h in header}
        pages = len(self.methods.GetElements("//ul[@class='pagination']//li", 'xpath'))
        for i in range(1, pages+1):
            if i==3:
                continue
            self.methods.ClickElement(f"(//ul[@class='pagination']//li//a)[{i}]", 'xpath')
            data[header[0]] += self.methods.GetListofElementText("//td[@class='name']",'xpath')
            data[header[1]] += self.methods.GetListofElementText("//td[@class='year']", 'xpath')
            data[header[2]] += self.methods.GetListofElementText("//td[@class='wins']", 'xpath')
            data[header[3]] += self.methods.GetListofElementText("//td[@class='losses']", 'xpath')
            data[header[4]] += self.methods.GetListofElementText("//td[@class='ot-losses']", 'xpath')
            data[header[5]] += self.methods.GetListofElementText("//td[contains(@class, 'pct')]", 'xpath')
            data[header[6]] += self.methods.GetListofElementText("//td[@class='gf']", 'xpath')
            data[header[7]] += self.methods.GetListofElementText("//td[@class='ga']", 'xpath')
            data[header[8]] += self.methods.GetListofElementText("//td[contains(@class, 'diff')]", 'xpath')
        save_data_methods.save_data_as_csv("Hockey_Data", data)

scraper = DataScraper("https://www.scrapethissite.com/pages/forms")
scraper.collect_data()