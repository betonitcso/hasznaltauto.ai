from selenium import webdriver

class HasznaltautoDriver:

    def __init__(self):
        self.driver = webdriver.Chrome()

    def getSite(self):
        while True:
            self.driver.get("https://hasznaltauto.hu")
        


if __name__ == "__main__":
    hasznaltauto = HasznaltautoDriver()
    hasznaltauto.getSite()