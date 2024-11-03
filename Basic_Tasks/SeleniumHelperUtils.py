from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(element))
        if element:
            try:
                element.click()
            except:
                print(f"Element is not clickable at {locator}")

    def EnterText(self, locator, locatorType, text):
        element = self.GetElement(locator, locatorType)
        if element:
            try:
                element.clear()
                element.send_keys(text)
            except:
                print("There is not text field")

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
                print("Page is not scrollable")

    def GetElementAttributeText(self,attribute,locator,locatorType):
        element = self.GetElement(locator, locatorType)
        if element:
            text = element.get_attribute(attribute)
            if text:
                return text
            else:
                print(f"element has no such attribute as {attribute}")
                return ''

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
                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((locator, locatorType)))
                return True
            except:
                return False