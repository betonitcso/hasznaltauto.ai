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

    def extractModelsDropdown(make:str):
        pass
    
    def extractCarMakes(self):
        dropdown = self.extractMakesDropdown()
        dropdown.click()

        carMakeList = []
        for i in range(300):
            try:
                makes = self.driver.find_elements(by=By.CLASS_NAME, value='MuiAutocomplete-option')
                for make in makes:
                    mk = make.get_attribute('innerText').split('(')[0].lower().strip()
                    if mk not in carMakeList:
                        carMakeList.append(mk)
                dropdown.send_keys(Keys.ARROW_DOWN)
            except Exception:
                pass

        return carMakeList 





if __name__ == '__main__':
    hd = HasznaltautoDriver()
    print(hd.extractCarMakes())