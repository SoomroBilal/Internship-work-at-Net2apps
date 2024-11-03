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
        self.methods.ScrollToViewAndClick("//button//span[text()='Show more']", 'xpath')

    def filtrate(self):
        if self.methods.IsElementPresent("//button[@aria-label='Close']", 'xpath'):
            self.methods.ClickElement("//button[@aria-label='Close']", 'xpath')

        self.methods.ScrollToViewAndClick("//span[text()='Shop']",'xpath')

        self.methods.ClickElement("//a[@title='Cell Phones and Accessories']",'xpath')

        self.methods.ClickElement("//a[@title='Unlocked Phones']",'xpath')

        self.methods.ClickElement("//a[@title='Unlocked Google Phones']", 'xpath')

        self.methods.ScrollToViewAndClick("//span[text()='Product Condition']", 'xpath')
        time.sleep(1)

        self.methods.ClickElement("//label[text()='Brand New']", 'xpath')
        time.sleep(2)

        results = int(self.methods.GetElementText("//div[@data-testid = 'PRODUCT_LIST_RESULT_COUNT_DATA_AUTOMATION']",'xpath').split()[0])
        items  = self.methods.ReturnLengthOfElements("//div[contains(@class,'style-module_col-xs-12__TFIB5')]", 'xpath')
        for i in range(results//items):
            self.load_more()
            time.sleep(2)
            items = self.methods.ReturnLengthOfElements("//div[contains(@class,'style-module_col-xs-12__TFIB5')]",'xpath')
            if items==results:
                break

    def collect_data(self):
        self.filtrate()
        names = self.methods.GetListofElementText("//ul[@class='list_3khgt']//div[@itemprop='name']", 'xpath')
        prices = []
        for i in range(1, self.methods.ReturnLengthOfElements("//ul[@class='list_3khgt']//span[@data-automation='product-price']//div//div", 'xpath')+1):
            p = self.methods.GetElementText(f"(//ul[@class='list_3khgt']//span[@data-automation='product-price']//div//div)[{i}]", 'xpath')
            p = p.replace('$','')
            if ',' in p:
                p = p.replace(',', '')
            prices.append(float(p))
        links = self.methods.GetListofElementAttributeText('href',"//ul[@class='list_3khgt']//a[@class='link_3hcyN']", 'xpath')
        data = {'Name': names, 'Price': prices, 'Link': links}
        save_data_methods.save_data_as_csv("Phones_Data", data)
scraper = DataScraper("https://www.bestbuy.ca/en-ca")
scraper.collect_data()
