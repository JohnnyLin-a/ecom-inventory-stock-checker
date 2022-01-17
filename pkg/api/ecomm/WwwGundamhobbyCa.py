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

        # Wait for banner to finish rendering
        try:
            WebDriverWait(webEngine.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#cb-shipping-bar[style*='z-index: 9999']"))
            )
        except:
            return [{"data": None, "error": "Cannot find nav bar"}]
        
        # find all categories from the navbar
        self.__findCategories(webEngine, webEngine.driver.find_elements(By.CSS_SELECTOR, "#AccessibleNav>li:not(.buddha-disabled)"))

        for category in self.__categoryLinks:
            for k, v in category.items():
                print(k, v)
        webEngine.driver.quit()

        return [{"data": None}]
    
    @staticmethod
    def getUrl() -> str:
        return "http://www.gundamhobby.ca"

    def __findCategories(self, webEngine: WebEngine, listItems: List[WebElement]) -> None:
        for e in listItems:
            anchor = e.find_element(By.CSS_SELECTOR, "a")
            label = anchor.get_attribute("aria-label")
            if label not in self.__skipCategories:
                if anchor != None and anchor.get_attribute("href") != "javascript:void(0);":
                    self.__categoryLinks.append({label: anchor.get_attribute("href")})
                try:
                    ul = e.find_element(By.CSS_SELECTOR, "ul")
                    self.__findCategories(webEngine, ul.find_elements(By.XPATH, "./*"))
                except:
                    pass
