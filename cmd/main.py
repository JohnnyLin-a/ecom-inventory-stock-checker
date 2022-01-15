from dotenv import load_dotenv
from pkg.api.webengine import WebEngine, WebEngineConfig
import os

def main():
    load_dotenv()

    # Start webdriver
    webEngineConfig = WebEngineConfig()
    webEngineConfig.headless = os.getenv("DEBUG").upper() != "TRUE"

    print(webEngineConfig.headless)

    webEngine = WebEngine(config=webEngineConfig)
    webEngine.start()

    # Create gundamhobby session and execute
    # Save gundamhobby results to database
    # Post notification on discord


if __name__ == '__main__':
    main()