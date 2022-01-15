from typing import List
from pkg.api.ecomm.Ecomm import EcommInterface
from pkg.api.webengine import WebEngine

class WwwGundamhobbyCa(EcommInterface):
    url = "http://www.gundamhobby.ca"

    def execute(self, webEngine: WebEngine) -> List[dict]:
        webEngine.driver.get(self.url)
        return [{"data": None}]