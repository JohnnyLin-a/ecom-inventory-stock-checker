from pkg.api.ecomm.Ecomm import EcommInterface
from pkg.api.webengine import WebEngine
from pkg.api.ecomm.Item import Item
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class ScifianimeCa(EcommInterface):
    webhookFull: str = "DISCORD_WEBHOOK_SCIFIANIME_FULL"
    webhookDiff: str = "DISCORD_WEBHOOK_SCIFIANIME_DIFF"

    def __init__(self):
        pass

    def execute(self, webEngine: WebEngine) -> dict:
        webEngine.driver.get(self.getUrl() + "/page/1/?post_type=product&s=&product_cat=")
        maxPage = 0

        # find max page
        try:
            WebDriverWait(webEngine.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul.page-numbers"))
            )
            pagesDOM = webEngine.driver.find_elements(By.CSS_SELECTOR, "ul.page-numbers>li")
            lastPageDOM = pagesDOM[len(pagesDOM)-2].find_element(By.CSS_SELECTOR, "a")
            maxPage = int(lastPageDOM.text)
        except:
            return {"error": "cannot wait for max page number"}
        
        if maxPage == 0:
            return {"error": "failed to get max page"}


        # find in-stock items
        inStockItems = {"*": []}
        for page in range(1, maxPage):
            print("Onto page " + str(page) + "/" + str(maxPage - 1))
            webEngine.driver.get(self.getUrl() + "/page/" + str(page) + "/?post_type=product&s=&product_cat=")

            # wait for item containers
            try:
                WebDriverWait(webEngine.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.products"))
                )
            except:
                return {"error": "cannot find items container"}
            # Find items in current page:
            items = webEngine.driver.find_elements(By.CSS_SELECTOR, "ul.products>li")

            for itemDOM in items:
                # Check if item addable to cart (in-stock check)
                try:
                    addToCart = itemDOM.find_element(By.CSS_SELECTOR, "a.button")
                    if addToCart.text == 'Read more':
                        continue
                except:
                    return {"error": "cannot find item add to cart button"}
                nameDOM = itemDOM.find_element(By.CSS_SELECTOR, "a>h2")
                name = nameDOM.text
                inStockItems["*"].append(Item(1, name, "*"))
        return inStockItems
    
    @staticmethod
    def getUrl() -> str:
        return "https://scifianime.ca"
        