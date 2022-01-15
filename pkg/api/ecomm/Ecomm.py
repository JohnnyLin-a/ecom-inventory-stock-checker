
import string
from typing import List
from pkg.api.webengine import WebEngine

class EcommInterface:
    def execute(self, webEngine: WebEngine) -> List[dict]:
        """Execute steps to get the data"""
        pass

    @staticmethod
    def getUrl() -> string:
        """Return the ecomm main website"""
        pass