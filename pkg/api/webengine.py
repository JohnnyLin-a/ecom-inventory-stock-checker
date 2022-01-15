from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options

@dataclass
class WebEngineConfig:
    headless: bool = False

class WebEngine:
    def __init__(self, config: WebEngineConfig):
        self.config = config

    def start(self) -> bool:
        options = Options()
        options.headless = self.config.headless
        self.driver = webdriver.Firefox(options=options)
