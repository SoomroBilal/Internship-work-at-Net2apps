from selenium import webdriver
from SeleniumHelperUtils import methods
import save_data_methods

class DataScraper:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        self.method = methods(self.driver)

    def filtrate(self):
        self.method.HoverOverElement("ui-id-5",'id')
        self.method.HoverOverElement("ui-id-17",'id')
        self.method.ClickElement("ui-id-19", 'id')

        self.method.ClickElement("//div[text()='Size']", 'xpath')
        self.method.ClickElement("//a//div[text()='S']",'xpath')

        self.method.ClickElement("//div[text()='Color']", 'xpath')
        self.method.ClickElement("//a//div[@option-label='Red']",'xpath')

        self.method.ClickElement("//div[text()='Material']", 'xpath')
        self.method.ClickElement("//a[contains(text(), 'LumaTech')]", 'xpath')

    def collect_data(self):
        self.filtrate()
        size = self.method.GetElementText("//span[text()='S']",'xpath')
        color = self.method.GetElementText("//span[text()='Red']",'xpath')
        material = self.method.GetElementText("//span[contains(text(), 'LumaTech')]",'xpath')
        names = self.method.GetListofElementText("//a[@class='product-item-link']",'xpath')
        prices = self.method.GetListofElementText("//div[contains(@class, 'product-item-details')]//span[@class='price']",'xpath')
        prices = [float(p.replace('$',''))*280 for p in prices]
        size = [size]*len(names)
        color = [color]*len(names)
        material = [material]*len(names)

        data = {'Item': names, 'Price': prices, 'Size': size, 'Color': color, 'Material': material}
        save_data_methods.save_data_as_xlsx("Jackets_Data", data)

scraper = DataScraper("https://magento.softwaretestingboard.com")
scraper.collect_data()
