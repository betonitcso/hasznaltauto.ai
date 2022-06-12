import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class HasznaltautoDriver:

    baseURL = 'http://hasznaltauto.hu'

    def __init__(self, wd = webdriver.Chrome()):
        self.driver = wd
        self.driver.get(HasznaltautoDriver.baseURL)

    def extractMakesDropdown(self):
        dropdown = self.driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[1]/div[6]/div[3]/div/div[2]/div[2]/div[1]/div/form/div[1]/div/div[1]/div/div/input')
        return dropdown

    def extractDropdownValues(self, dropdown):
        li = []
        dropdown.click()
        for i in range(300):
            try:
                elements = self.driver.find_elements(by=By.CLASS_NAME, value='MuiAutocomplete-option')
                for element in elements:
                    el = element.get_attribute('innerText')
                    if el not in li:
                        li.append(el)
                dropdown.send_keys(Keys.ARROW_DOWN)
            except Exception:
                pass
        return li

    
    def extractCarMakes(self):
        dropdown = self.extractMakesDropdown()
        makes = self.extractDropdownValues(dropdown)

        def splitMakes(make:str):
            
            return re.split('\([0-9]',make)[0].strip()

        return list(map(splitMakes, makes))

    def extractModelsDropdown(self):
        dropdown = self.driver.find_elemnt(by=By.XPATH, value="/html/body/div[3]/div[1]/div[6]/div[3]/div/div[2]/div[2]/div[1]/div/form/div[1]/div/div[2]/div/div")
        return dropdown

    def extractCarModels(self, make:str):
        makeInput = self.driver.find_element(by=By.XPATH, value= '//*[@id="mui-2"]')
        makeInput.send_keys(make)
        makeInput.send_keys(Keys.ENTER)
        dropdown = self.extractModelsDropdown()





if __name__ == '__main__':
    hd = HasznaltautoDriver()
    print(hd.extractCarMakes())