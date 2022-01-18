import json
from dotenv import load_dotenv
from pkg.api.webengine import WebEngine, WebEngineConfig
from pkg.api.ecomm.WwwGundamhobbyCa import WwwGundamhobbyCa
from pkg.api.ecomm.Item import Item
import os

from pkg.database.DBEngine import DBEngine

def main():
    load_dotenv()
    load_dotenv("postgres.env")

    # Start webdriver
    webEngineConfig = WebEngineConfig()
    webEngineConfig.headless = os.getenv("DEBUG").upper() != "TRUE"

    # webEngine = WebEngine(config=webEngineConfig)
    # webEngine.start()

    # Create gundamhobby session and execute
    gundamhobbyCaSession = WwwGundamhobbyCa()
    # gundamhobbySessionData = gundamhobbyCaSession.execute(webEngine)

    # Use json cache instead of executing for 10min
    with open('./2022-01-16.json.log') as f:
        gundamhobbySessionDataJson = json.load(f)
    gundamhobbySessionData = {}
    for category, itemsRaw in gundamhobbySessionDataJson.items():
        gundamhobbySessionData[category] = []
        for itemRaw in itemsRaw:
            gundamhobbySessionData[category].append(Item(1,itemRaw['name'],itemRaw['category']))

    # Create DBEngine and save gundamhobby results
    db = DBEngine()
    val = gundamhobbyCaSession.saveData(db, gundamhobbySessionData)
    
    print(val)
    # Compare diff against previous run

    # Post notification on discord


if __name__ == '__main__':
    main()