from pkg.api.ecomm.Ecomm import EcommInterface
from pkg.api.webengine import WebEngine
from pkg.api.ecomm.Item import Item
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class MetrohobbiesCa(EcommInterface):
    webhookFull: str = "DISCORD_WEBHOOK_METROHOBBIES_FULL"
    webhookDiff: str = "DISCORD_WEBHOOK_METROHOBBIES_DIFF"

    def __init__(self):
        pass

    def execute(self, webEngine: WebEngine) -> dict:
        # Dismiss free shipping message by adding cookie
        webEngine.driver.get(self.getUrl() + "/s/shop?page=1&limit=180&sort_by=created_date&sort_order=desc&item_status=in_stock")
        webEngine.driver.add_cookie({"name": "leadform_d76274a5-8666-46d9-be27-d447af3baed5_closed", "value": "1", "path": "/", "domain": "www.metrohobbies.ca", "secure": False, "sameSite": "Lax", "expiry": 2147483647})

        webEngine.driver.get(self.getUrl() + "/s/shop?page=1&limit=180&sort_by=created_date&sort_order=desc&item_status=in_stock")
        maxPage = 0


        # find max page
        try:
            WebDriverWait(webEngine.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".pagination-page-numbers"))
            )
            pagesDOM = webEngine.driver.find_elements(By.CSS_SELECTOR, ".pagination-page-numbers>a")
            maxPage = int(pagesDOM[len(pagesDOM)-1].text.strip()) + 1
        except:
            return {"error": "cannot wait for max page number"}
        
        if maxPage == 1:
            return {"error": "failed to get max page"}


        # find in-stock items
        inStockItems = {"*": []}
        for page in range(1, maxPage):
            print("Onto page " + str(page) + "/" + str(maxPage - 1))
            webEngine.driver.get(self.getUrl() + "/s/shop?page=" + str(page) + "&limit=180&sort_by=created_date&sort_order=desc&item_status=in_stock")

            # wait for item containers
            try:
                WebDriverWait(webEngine.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".category__wrapper>.category__products>.w-container>div:nth-child(2)>div>div"))
                )
            except:
                return {"error": "cannot find items container"}
            # Find items in current page:
            items = webEngine.driver.find_elements(By.CSS_SELECTOR, ".category__wrapper>.category__products>.w-container>div:nth-child(2)>div>div")

            for itemDOM in items:
                nameDOM = itemDOM.find_element(By.CSS_SELECTOR, "div>a>div>div>div>p.w-product-title")
                name = nameDOM.text
                inStockItems["*"].append(Item(1, name, "*"))
        return inStockItems
    
    @staticmethod
    def getUrl() -> str:
        return "https://www.metrohobbies.ca"
