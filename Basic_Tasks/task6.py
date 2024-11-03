import time
import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from SeleniumHelperUtils import methods

class FilesDownloader:
    def __init__(self, url):
        self.chrome_configurations()
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(url)
        self.methods = methods(self.driver)

    def chrome_configurations(self):
        self.download_folder = r'C:\Users\HP\PycharmProjects\InternshipTasks\Windows10catalogfiles'
        self.options = Options()
        chrome_prefs = {
            "download.default_directory": self.download_folder,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        self.options.add_experimental_option('prefs', chrome_prefs)

    def navigation(self):
        text_field = self.methods.GetElement("//input[@id='searchTextBox']",'xpath')
        text_field.send_keys('Windows 10')
        self.methods.ClickElement("//input[@id='searchButtonLink']", 'xpath')
        os.chdir(r"C:\Users\HP\PycharmProjects\InternshipTasks\Windows10catalogfiles")

    def take_screenshot(self):
        Screenshot = self.methods.GetElement("//table[@id='ctl00_catalogBody_updateMatches']//tbody", 'xpath')
        self.methods.ScrolltoView("//table[@id='ctl00_catalogBody_updateMatches']//tbody",'xpath')
        Screenshot.screenshot('Screenshot.png')

    def wait_for_download_completion(self, file, windows):
        for i in range(300):
            if os.path.isfile(file) and not file.endswith('.crdownload'):
                self.driver.close()
                self.driver.switch_to.window(windows[0])
                time.sleep(2)
                break
            else:
                time.sleep(1)

    def download_file(self, link):
        self.methods.ClickElement(link,'xpath')
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        time.sleep(1)
        filename = self.methods.GetElementAttributeText('title',"//a[@class='contentTextItemSpacerNoBreakLink']",'xpath')
        self.methods.ClickElement("//a[@class='contentTextItemSpacerNoBreakLink']", 'xpath')
        self.wait_for_download_completion(fr"C:\Users\HP\PycharmProjects\InternshipTasks\Windows10catalogfiles\{filename}", windows)

    def download_all_files(self):
        self.navigation()
        self.take_screenshot()
        for i in range(1,11):
            self.download_file(f"(//input[@value='Download'])[{i}]")

Downloader = FilesDownloader("https://www.catalog.update.microsoft.com/Home.aspx")
Downloader.download_all_files()