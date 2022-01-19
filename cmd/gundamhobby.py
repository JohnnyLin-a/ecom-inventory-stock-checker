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

    webEngine = WebEngine(config=webEngineConfig)
    webEngine.start()

    # Create gundamhobby session and execute
    gundamhobbyCaSession = WwwGundamhobbyCa()
    gundamhobbySessionData = gundamhobbyCaSession.execute(webEngine)
    webEngine.driver.quit()

    # Create DBEngine and save gundamhobby results
    db = DBEngine()
    result = gundamhobbyCaSession.saveData(db, gundamhobbySessionData)
    if not (result['error'] == None and result['execution_id'] != 0):
        print('Run unsuccessful, exitting app...')
        os._exit(1)
    db.get().execute('UPDATE executions SET successful = true WHERE id = %s', (result['execution_id']))

    # Compare diff against previous run
    
    # Post notification on discord


if __name__ == '__main__':
    main()