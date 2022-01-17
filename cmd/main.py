from dotenv import load_dotenv
from pkg.api.webengine import WebEngine, WebEngineConfig
from pkg.api.ecomm.WwwGundamhobbyCa import WwwGundamhobbyCa
import os

from pkg.database.DBEngine import DBEngine

def main():
    load_dotenv()
    load_dotenv("postgres.env")

    # Start webdriver
    webEngineConfig = WebEngineConfig()
    webEngineConfig.headless = os.getenv("DEBUG").upper() != "TRUE"

    webEngine = WebEngine(config=webEngineConfig)
    webEngine.start()

    # Create gundamhobby session and execute
    gundamhobbyCaSession = WwwGundamhobbyCa()
    gundamhobbySessionData = gundamhobbyCaSession.execute(webEngine)

    # Create DBEngine and save gundamhobby results
    db = DBEngine()
    gundamhobbyCaSession.saveData(db, gundamhobbySessionData)

    # Compare diff against previous run

    # Post notification on discord


if __name__ == '__main__':
    main()