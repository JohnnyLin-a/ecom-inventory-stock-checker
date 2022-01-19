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
        return "https://www.gundamhobby.ca"

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

    def saveData(self, db: DBEngine, data: dict) -> dict:
        ecom_id = 0
        categories = {}
        items = {}

        # Find ecom_id for gundamhobby
        cursorResult = db.get().execute('SELECT id FROM ecoms WHERE website = %s LIMIT 1;', (self.getUrl()))
        if cursorResult.rowcount == 0:
            cursorResult = db.get().execute('INSERT INTO ecoms (website) VALUES (%s) RETURNING id;', (self.getUrl()))
        for r in cursorResult:
            ecom_id = r['id']
        if ecom_id == 0:
            return {"error": "Cannot find ecom_id for gundamhobby"}
        
        # Find items in db, set existing items and categories
        cursorResult = db.get().execute("""select items.name AS "items.name", items.id as "items.id", categories.name AS "categories.name", categories.id AS "categories.id" 
            from items
            left join item_categories on item_categories.item_id = items.id
            left join categories on categories.id = item_categories.category_id
            where items.ecom_id = %s;""", (ecom_id))
        for r in cursorResult:
            if r['categories.name'] not in categories:
                categories[r['categories.name']] = {'id': r['categories.id']}
            if r['items.name'] not in items:
                items[r['items.name']] = {'id': r['items.id'], 'categories': [r["categories.name"]]}
            else:
                items[r['items.name']]['categories'].append(r["categories.name"])

        # Save new execution
        execution_id = 0
        cursorResult = db.get().execute('INSERT INTO executions (ecom_id) VALUES (%s) RETURNING id;', (ecom_id))
        for r in cursorResult:
            execution_id = r['id']
        if execution_id == 0:
            return {"error": "Cannot insert new execution_id for gundamhobby"}
        
        # process data, insert new items/categories accordingly, insert execution data
        itemsAlreadyInserted = {}
        for categoryName, rawItems in data.items():
            category_id = 0
            if categoryName in categories:
                category_id = categories[categoryName]['id']
            if category_id == 0:
                cursorResult = db.get().execute('INSERT INTO categories (name) VALUES (%s) RETURNING id;', (categoryName))
                for r in cursorResult:
                    category_id = r['id']
                    categories[categoryName] = {'id': category_id}
            if category_id == 0:
                return {"error": "Cannot insert new category_id for gundamhobby"}
            
            for rawItem in rawItems:
                # match item
                item_id = 0
                if rawItem.name in items:
                    item_id = items[rawItem.name]['id']
                if item_id == 0:
                    cursorResult = db.get().execute('INSERT INTO items (ecom_id, name) VALUES (%s, %s) RETURNING id;', (ecom_id, rawItem.name))
                    for r in cursorResult:
                        item_id = r['id']
                        items[rawItem.name] = {'id': item_id, 'categories': [categoryName]}
                        db.get().execute('INSERT INTO item_categories (item_id, category_id) VALUES (%s, %s);', (item_id, category_id))
                if item_id == 0:
                    return {"error": "Cannot insert new item_id for gundamhobby"}
                # check if category is linked and add it if it isn't
                if categoryName not in items[rawItem.name]['categories']:
                    db.get().execute('INSERT INTO item_categories (item_id, category_id) VALUES (%s, %s);', (item_id, category_id))
                    items[rawItem.name]['categories'].append(categoryName)

                # Finally save execution
                if item_id not in itemsAlreadyInserted:
                    db.get().execute('INSERT INTO execution_item_stocks (execution_id, item_id) VALUES (%s, %s);', (execution_id, item_id))
                    itemsAlreadyInserted[item_id] = None
        return {"error": None, "execution_id": execution_id}

    def getDiffFromLast2SuccessfulRuns(self, db: DBEngine) -> dict:
        # Get ecom_id
        ecom_id = 0
        cursorResult = db.get().execute('SELECT id FROM ecoms WHERE website = %s LIMIT 1;', (self.getUrl()))
        if cursorResult.rowcount == 0:
            return {"error": "Cannot find ecom_id for gundamhobby"}
        for r in cursorResult:
            ecom_id = r['id']
        

        return {'error': None, 'data': {'+': [], '-': []}}