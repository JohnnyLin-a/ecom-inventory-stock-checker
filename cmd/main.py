from dotenv import load_dotenv
from pkg.api.webengine import WebEngine, WebEngineConfig
import os

def main():
    load_dotenv()

    # Start webdriver
    webEngineConfig = WebEngineConfig()
    webEngineConfig.headless = os.getenv("DEBUG") != None and (os.getenv("DEBUG").upper() == "TRUE" or os.getenv("DEBUG") == "1")

    webEngine = WebEngine(config=webEngineConfig)
    webEngine.start()

    # Create gundamhobby session and execute
    # Save gundamhobby results to database
    # Post notification on discord


if __name__ == '__main__':
    main()