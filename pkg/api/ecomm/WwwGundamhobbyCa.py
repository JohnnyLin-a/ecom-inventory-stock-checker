from typing import List
from pkg.api.ecomm.Ecomm import EcommInterface
from pkg.api.webengine import WebEngine
from pkg.api.ecomm.Item import Item
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pkg.database.DBEngine import DBEngine

class WwwGundamhobbyCa(EcommInterface):
    __skipCategories: list = ("Home", "Paint Supplies", "Tools")
    __categoryLinks: List[dict] = []

    def __init__(self):
        pass

    def execute(self, webEngine: WebEngine) -> dict:
        webEngine.driver.get(WwwGundamhobbyCa.getUrl())

        # Wait for banner to finish rendering
        if not self.__bannerWait(webEngine):
            return {"error": "Failed to wait for banner on home page"}
        
        # find all categories from the navbar
        self.__findCategories(webEngine, webEngine.driver.find_elements(By.CSS_SELECTOR, "#AccessibleNav>li:not(.buddha-disabled)"))

        # find in-stock items
        inStockItems = {}
        for category in self.__categoryLinks:
            for categoryLabel, url in category.items():
                inStockItems[categoryLabel] = []
                page = 1
                while page != -1:
                    webEngine.driver.get(url + "?page=" + str(page))
                    # Wait for banner to finish rendering
                    if not self.__bannerWait(webEngine):
                        return {"error": "Failed to wait for banner on " + url}
                    
                    # Find items in current page:
                    itemsContainer = webEngine.driver.find_element(By.CSS_SELECTOR, ".grid-uniform.grid-link__container")

                    # Check if there are any items in this page
                    try:
                        itemsContainer.find_element(By.CSS_SELECTOR, "div.grid__item>p>em")
                        page = -1
                        continue
                    except:
                        # Do nothing when items are found in current page.
                        pass

                    # Iterate through all items in current page
                    items = itemsContainer.find_elements(By.XPATH, "./*")
                    for item in items:
                        # Check if sold out
                        soldOut = True
                        try:
                            item.find_element(By.CSS_SELECTOR, "a>span>span.badge--sold-out")
                        except:
                            soldOut = False
                        if not soldOut:
                            # get item name
                            itemTitle = item.find_element(By.CSS_SELECTOR, "a>p.grid-link__title")
                            inStockItems[categoryLabel].append(Item(1, itemTitle.text, categoryLabel))
                    page += 1

        return inStockItems
    
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
                    # Will crash if ul is not found
                    pass

    def __bannerWait(self, webEngine: WebEngine) -> bool:
        try:
            WebDriverWait(webEngine.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#cb-shipping-bar[style*='z-index: 9999']"))
            )
        except:
            return False
        return True

    def saveData(self, db: DBEngine, data: dict):
        pass