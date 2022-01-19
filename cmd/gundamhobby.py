import json
import time
from dotenv import load_dotenv
from pkg.api.webengine import WebEngine, WebEngineConfig
from pkg.api.ecomm.WwwGundamhobbyCa import WwwGundamhobbyCa
from pkg.api.ecomm.Item import Item
import os
import requests

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
    diff = gundamhobbyCaSession.getDiffFromLast2SuccessfulRuns(db)
    fullInventory = gundamhobbyCaSession.getFullInventory(db)

    # Post notification on discord
    diffMsg = ""
    data = diff['data']
    if len(data['+']) != 0:
        diffMsg += 'New arrivals:\n'
        for plus in data['+']:
            diffMsg += plus + '\n'
        diffMsg += '\n'
    if len(data['-']) != 0:
        diffMsg += 'Recently out of stock:\n'
        for minus in data['-']:
            diffMsg += minus + '\n'
        diffMsg += '\n'
    
    discordWebhookDiff = os.getenv("DISCORD_WEBHOOK_GUNDAMHOBBY_DIFF")
    if discordWebhookDiff != None:
        requests.post(discordWebhookDiff, {'content': "@everyone\n" + diffMsg})

    fullMsgPart = 0
    fullMsg = ['']
    for row in fullInventory:
        if len(fullMsg[fullMsgPart]) + len(row['name']) > 2000:
            fullMsgPart += 1
            fullMsg.append('')
        if len(row['name']) > 2000:
            break
        fullMsg[fullMsgPart] += row['name'] + '\n'
    discordWebhookFull = os.getenv("DISCORD_WEBHOOK_GUNDAMHOBBY_FULL")
    if discordWebhookFull != None:
        time.sleep(1)
        requests.post(discordWebhookFull, {'content': "@everyone Posting full inventory at this time:"})
        for t in fullMsg:
            time.sleep(1)
            requests.post(discordWebhookFull, {'content': t})
    time.sleep(1)
    requests.post(discordWebhookFull, {'content': "End of full inventory"})

    


if __name__ == '__main__':
    main()