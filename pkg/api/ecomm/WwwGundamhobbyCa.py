import string
from typing import List
from pkg.api.ecomm.Ecomm import EcommInterface
from pkg.api.webengine import WebEngine
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

class WwwGundamhobbyCa(EcommInterface):
    __skipCategories: list = ("Home", "Paint Supplies", "Tools")
    __categoryLinks: List[dict] = []

    def __init__(self):
        pass

    def execute(self, webEngine: WebEngine) -> List[dict]:
        webEngine.driver.get(WwwGundamhobbyCa.getUrl())

        # find all categories from the navbar
        try:
            WebDriverWait(webEngine.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#AccessibleNav"))
            )
        except:
            return [{"data": None, "error": "Cannot find nav bar"}]
        
        categories = self.__findCategories(webEngine, "#AccessibleNav>li:not(.buddha-disabled)")

        return [{"data": None}]
    
    @staticmethod
    def getUrl() -> string:
        return "http://www.gundamhobby.ca"

    def __findCategories(self, webEngine: WebEngine, rootSelector: string) -> list:
        elems = webEngine.driver.find_elements(By.CSS_SELECTOR, rootSelector)
        for e in elems:
            if e.text not in self.__skipCategories:
                anchor = e.find_element(By.CSS_SELECTOR, "a")
                if anchor != None:
                    self.__categoryLinks.append({e.text: anchor.get_property("href")})
                    
        for dict in self.__categoryLinks:
            for k, v in dict.items():
                print(k, v)
                
        webEngine.driver.quit()
