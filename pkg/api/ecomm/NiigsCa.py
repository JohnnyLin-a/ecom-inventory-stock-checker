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
            print("Onto page " + str(page) + "/" + str(maxPage))
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

    def saveData(self, db: DBEngine, data: dict) -> dict:
        ecom_id = 0
        categories = {}
        items = {}

        # Find ecom_id for niigs
        cursorResult = db.get().execute('SELECT id FROM ecoms WHERE website = %s LIMIT 1;', (self.getUrl()))
        if cursorResult.rowcount == 0:
            cursorResult = db.get().execute('INSERT INTO ecoms (website) VALUES (%s) RETURNING id;', (self.getUrl()))
        for r in cursorResult:
            ecom_id = r['id']
        if ecom_id == 0:
            return {"error": "Cannot find ecom_id for niigs"}
        
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
            return {"error": "Cannot insert new execution_id for niigs"}
        
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
                return {"error": "Cannot insert new category_id for niigs"}
            
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
                    return {"error": "Cannot insert new item_id for niigs"}
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
        cursorResult = db.get().execute("""SELECT second_last_run_items.item_id as "second_last_run_items.item_id", second_last_run_items.name as "second_last_run_items.name", last_run_items.item_id as "last_run_items.item_id", last_run_items.name as "last_run_items.name"
            FROM (
            SELECT execution_item_stocks.item_id, items.name
            FROM execution_item_stocks
            INNER JOIN executions on execution_item_stocks.execution_id = executions.id
            inner join items on items.id = execution_item_stocks.item_id
            WHERE executions.id IN (
                SELECT executions.id FROM executions
                inner join ecoms on ecoms.id = executions.ecom_id
                WHERE executions.successful = true AND ecoms.website = %s
                ORDER BY executions.id DESC
                LIMIT 1
                OFFSET 1 ROWS
            )) AS second_last_run_items
            FULL OUTER JOIN (SELECT execution_item_stocks.item_id, items.name
            FROM execution_item_stocks
            INNER JOIN executions on execution_item_stocks.execution_id = executions.id
            inner join items on items.id = execution_item_stocks.item_id
            WHERE executions.id IN (
                SELECT executions.id FROM executions
                inner join ecoms on ecoms.id = executions.ecom_id
                WHERE executions.successful = true AND ecoms.website = %s
                ORDER BY executions.id DESC
                LIMIT 1
            )) AS last_run_items ON last_run_items.item_id = second_last_run_items.item_id
            WHERE second_last_run_items.item_id IS NULL OR last_run_items.item_id IS NULL;""", (self.getUrl(), self.getUrl()))
        data = {'+': [], '-': []}
        for r in cursorResult:
            if r['second_last_run_items.item_id'] != None:
                data['-'].append(r['second_last_run_items.name'])
            else:
                data['+'].append(r['last_run_items.name'])
        return {'error': None, 'data': data}

    def getFullInventory(self, db: DBEngine):
        cursorResult = db.get().execute("""SELECT items.name
            FROM execution_item_stocks
            INNER JOIN executions on execution_item_stocks.execution_id = executions.id
            inner join items on items.id = execution_item_stocks.item_id
            WHERE executions.id IN (
                SELECT executions.id FROM executions
                inner join ecoms on ecoms.id = executions.ecom_id
                WHERE executions.successful = true AND ecoms.website = %s
                ORDER BY executions.id DESC
                LIMIT 1
            )
            ORDER BY items.name""", (self.getUrl()))
        return cursorResult
        