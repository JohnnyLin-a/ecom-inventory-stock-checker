from typing import List
from pkg.api.ecomm.Ecomm import EcommInterface
from pkg.api.webengine import WebEngine
from pkg.api.ecomm.Item import Item
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pkg.database.DBEngine import DBEngine

class NiigsCa(EcommInterface):
    def __init__(self):
        pass

    def execute(self, webEngine: WebEngine) -> dict:
        print("")
        webEngine.driver.get(NiigsCa.getUrl() + "/collections/all-availible-items?sort_by=title-ascending&page=1")
        maxPage = 0

        # find max page
        try:
            WebDriverWait(webEngine.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".pagination-custom"))
            )
            pagesDOM = webEngine.driver.find_elements(By.CSS_SELECTOR, ".pagination-custom>li")
            maxPage = int(pagesDOM[len(pagesDOM)-2].text.strip()) + 1
        except:
            return {"error": "cannot wait for max page number"}
        
        if maxPage == 1:
            return {"error": "failed to get max page"}


        # find in-stock items
        inStockItems = {"*": []}
        for page in range(1, maxPage):
            print("Onto page " + str(page) + "/" + str(maxPage - 1))
            webEngine.driver.get(NiigsCa.getUrl() + "/collections/all-availible-items?sort_by=title-ascending&page=" + str(page))

            # wait for item containers
            try:
                WebDriverWait(webEngine.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".grid-uniform"))
                )
            except:
                return {"error": "cannot find items container"}
            # Find items in current page:
            items = webEngine.driver.find_elements(By.CSS_SELECTOR, ".grid-uniform>div.grid-item")

            for itemDOM in items:
                nameDOM = itemDOM.find_element(By.CSS_SELECTOR, "a>p")
                name = nameDOM.text
                inStockItems["*"].append(Item(1, name, "*"))
        return inStockItems
    
    @staticmethod
    def getUrl() -> str:
        return "https://niigs.ca"
        