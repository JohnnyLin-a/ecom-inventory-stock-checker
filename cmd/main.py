from dotenv import load_dotenv
from pkg.api.webengine import WebEngine, WebEngineConfig
from pkg.api.ecomm.WwwGundamhobbyCa import WwwGundamhobbyCa
import os

def main():
    load_dotenv()

    # Start webdriver
    webEngineConfig = WebEngineConfig()
    webEngineConfig.headless = os.getenv("DEBUG").upper() != "TRUE"

    webEngine = WebEngine(config=webEngineConfig)
    webEngine.start()

    # Create gundamhobby session and execute
    gundamhobbyCaSession = WwwGundamhobbyCa()
    gundamhobbyData = gundamhobbyCaSession.execute(webEngine)

    # Save gundamhobby results to database
    # Post notification on discord


if __name__ == '__main__':
    main()