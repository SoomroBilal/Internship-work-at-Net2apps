from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gspread
from google.oauth2.service_account import Credentials

class methods:
    def __init__(self, driver):
        self.driver = driver

    def locator_type(self, locatortype):
        locatortypes = {
            'id': By.ID,
            'xpath':By.XPATH,
            'class':By.CLASS_NAME,
            'css_selector':By.CSS_SELECTOR,
            'tagname': By.TAG_NAME
        }
        locatortype =  locatortypes.get(locatortype.lower())

        if locatortype:
            return locatortype
        else:
            print('incorrect locator type')

    def GetElement(self,locator,locatorType):
        locatorType = self.locator_type(locatorType)
        if locatorType:
            try:
                element = self.driver.find_element(locatorType, locator)
                return element
            except:
                print(f"Element not found at {locator}")
                return False

    def IsElementPresent(self, locator, locatorType):
        locatorType = self.locator_type(locatorType)
        if locatorType:
            try:
                self.driver.find_element(locatorType, locator)
                return True
            except:
                print(f"Unable to locate element at {locator}")
                return False

    def GetElementText(self, locator,locatorType):
        element = self.GetElement(locator, locatorType)
        if element:
            text = element.text
            if text:
                return text
            else:
                print('there is no text')
                return False

    def ClickElement(self, locator, locatorType):
        element = self.GetElement(locator, locatorType)
        if element:
            try:
                element.click()
            except Exception as e:
                print(e)

    def EnterText(self, locator, locatorType, text):
        element = self.GetElement(locator, locatorType)
        if element:
            try:
                element.clear()
                element.send_keys(text)
            except:
                print("There is not text field")

    def wait_for_element_and_click(self, locator, locatorType, time):
        element = self.GetElement(locator, locatorType)
        if element:
            WebDriverWait(self.driver, time).until(EC.element_to_be_clickable(element))
            try:
                element.click()
            except:
                print(f"Element not clickable at {locator}")

    def handle_stale_element_error_and_click(self, locator, locatorType):
        try:
            self.GetElement(locator, locatorType).click()
        except:
            ignored_exceptions = (NoSuchElementException,StaleElementReferenceException)
            element=WebDriverWait(self.driver, 10, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.XPATH, locator)))
            element.click()

    def ScrolltoView(self,locator,locatorType):
        element = self.GetElement(locator, locatorType)
        if element:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            except:
                print("Page is not scrollable")

    def ScrollToViewAndClick(self, locator,locatorType):
        element = self.GetElement(locator, locatorType)
        if element:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                self.waitforElementTobevisible(locator,locatorType)
                self.ClickElement(locator, locatorType)
            except:
                print(f"Page is not scrollable at {locator}")

    def GetElementAttributeText(self,attribute,locator,locatorType):
        element = self.GetElement(locator, locatorType)
        if element:
            text = element.get_attribute(attribute)
            if text:
                return text
            else:
                print(f"element has no such attribute as {attribute}")
                return False

    def HoverOverElement(self, locator, locatorType):
        element = self.GetElement(locator, locatorType)
        try:
            ActionChains(self.driver).move_to_element(element).perform()
        except:
            print(f"Cant hover over the element at {locator}")

    def GetElements(self, locator, locatorType):
        locatorType = self.locator_type(locatorType)
        if locatorType:
            try:
                elements = self.driver.find_elements(locatorType, locator)
                if elements:
                    return elements
            except:
                print(f"Elements not found at {locator}")
                return False

    def ReturnLengthOfElements(self, locator, locatorType):
        elements = self.GetElements(locator, locatorType)
        if elements:
            return len(elements)


    def GetListofElementText(self, locator, locatorType):
        elements = self.GetElements(locator, locatorType)
        if elements:
            textlist = [i.text for i in elements]
            if textlist:
                return textlist
            else:
                print("There is no list of text")
                return False


    def GetListofElementAttributeText(self, attribute,locator,locatorType):
        elements = self.GetElements(locator, locatorType)
        if elements:
            attributetextlist = [i.get_attribute(attribute) for i in elements if i.get_attribute is not None]
            if attributetextlist:
                return attributetextlist
            else:
                print("No such attribute")
                return False


    def waitforElementTobevisible(self, locator, locatorType):
        locatorType = self.locator_type(locatorType)
        if locatorType:
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((locatorType, locator)))
                return True
            except:
                return False

    def waitforElementTobeInvisible(self, locator, locatorType, time):
        locatorType = self.locator_type(locatorType)
        if locatorType:
            try:
                WebDriverWait(self.driver, time).until(EC.invisibility_of_element((locatorType, locator)))
            except:
                return False

    def gspread_config(self, credentials):
        scopes = ["https://spreadsheets.google.com/feeds",
                  'https://www.googleapis.com/auth/spreadsheets',
                  "https://www.googleapis.com/auth/drive.file",
                  "https://www.googleapis.com/auth/drive"
                  ]

        creds = Credentials.from_service_account_file(credentials, scopes=scopes)
        return gspread.authorize(creds)

    def SapLogin(self, config_file):
        file = open(config_file, 'r')
        lines = [line.replace('\n', '') for line in file.readlines()]
        self.EnterText('__input0-inner', 'id', lines[0])
        self.ClickElement('continueToLoginBtn', 'id')
        self.EnterText('j_username', 'id', lines[1])
        self.EnterText('j_password', 'id', lines[2])
        self.ClickElement('logOnFormSubmit', 'id')