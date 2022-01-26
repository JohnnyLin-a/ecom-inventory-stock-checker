from pkg.api.ecomm.Ecomm import EcommInterface
from pkg.api.webengine import WebEngine
from pkg.api.ecomm.Item import Item
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests

class MetrohobbiesCa(EcommInterface):
    webhookFull: str = "DISCORD_WEBHOOK_METROHOBBIES_FULL"
    webhookDiff: str = "DISCORD_WEBHOOK_METROHOBBIES_DIFF"

    def __init__(self):
        pass

    def execute(self, webEngine: WebEngine) -> dict:
        # Use rest api directly
        inStockItems = {"*": []}
        page = 1
        totalPages = 1
        while page <= totalPages:
            print("Onto page " + str(page) + "/" + str(totalPages))
            req = requests.get("https://cdn5.editmysite.com/app/store/api/v17/editor/users/131444256/sites/426079854127040612/products?page=" + str(page) + "&per_page=180&sort_by=created_date&sort_order=desc&in_stock=1&excluded_fulfillment=dine_in")
            if not req.ok:
                return {"error": "failed to get data for page " + str(page)}
            try:
                data = req.json()
            except:
                return {"error": "failed to convert to json for page " + str(page)}
            
            # Set max page
            totalPages = data['meta']['pagination']['total_pages']

            # iterate over items
            for item in data['data']:
                inStockItems["*"].append(Item(1, item['name'], '*'))
            
            page += 1
        return inStockItems
    
    @staticmethod
    def getUrl() -> str:
        return "https://www.metrohobbies.ca"
