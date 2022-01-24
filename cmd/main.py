import time
from dotenv import load_dotenv
from pkg.api.ecomm.Ecomm import EcommInterface
from pkg.api.ecomm.MetrohobbiesCa import MetrohobbiesCa
from pkg.api.ecomm.NiigsCa import NiigsCa
from pkg.api.ecomm.WwwGundamhobbyCa import WwwGundamhobbyCa
from pkg.api.webengine import WebEngine, WebEngineConfig
import os
import requests

from pkg.database.DBEngine import DBEngine

def execEcom(ecomSession: EcommInterface, db: DBEngine):
    # Start webdriver
    webEngineConfig = WebEngineConfig()
    webEngineConfig.headless = os.getenv("DEBUG").upper() != "TRUE"

    webEngine = WebEngine(config=webEngineConfig)
    webEngine.start()

    # Create ecomm session and execute
    ecomSessionData = ecomSession.execute(webEngine)
    webEngine.driver.quit()

    # Create DBEngine and save niigs results
    result = ecomSession.saveData(db, ecomSessionData)
    if not (result['error'] == None and result['execution_id'] != 0):
        print('Run unsuccessful, exitting execution...')
        return
    db.get().execute('UPDATE executions SET successful = true WHERE id = %s', (result['execution_id']))

    # Compare diff against previous run
    diff = ecomSession.getDiffFromLast2SuccessfulRuns(db)
    fullInventory = ecomSession.getFullInventory(db)

    # Post notification on discord
    diffMsg = 0
    diffMsgParts = ['']
    data = diff['data']

    if len(data['+']) != 0:
        diffMsgParts[diffMsg] += '@everyone\nNew arrivals:\n'
        for plus in data['+']:
            if len(diffMsgParts[diffMsg]) + len(plus) > 2000:
                diffMsg += 1
                diffMsgParts.append('')
            if len(plus) > 2000:
                break
            diffMsgParts[diffMsg] += plus + '\n'
        if len(diffMsgParts[diffMsg]) + 1 > 2000:
            diffMsg += 1
            diffMsgParts.append('')
        diffMsgParts[diffMsg] += '\n'

    if len(data['-']) != 0:
        if len(diffMsgParts[diffMsg]) + 23 > 2000:
            diffMsg += 1
            diffMsgParts.append('')
        diffMsgParts[diffMsg] += 'Recently out of stock:\n'
        for minus in data['-']:
            if len(diffMsgParts[diffMsg]) + len(minus) > 2000:
                diffMsg += 1
                diffMsgParts.append('')
            if len(minus) > 2000:
                break
            diffMsgParts[diffMsg] += minus + '\n'
        if len(diffMsgParts[diffMsg]) + 1 > 2000:
            diffMsg += 1
            diffMsgParts.append('')
        diffMsgParts[diffMsg] += '\n'
    
    discordWebhookDiff = os.getenv(ecomSession.webhookDiff)
    if discordWebhookDiff != None:
        for diffMsgPart in diffMsgParts:
            time.sleep(1)
            requests.post(discordWebhookDiff, {'content': diffMsgPart})  

    fullMsgPart = 0
    fullMsg = ['']
    for row in fullInventory:
        if len(fullMsg[fullMsgPart]) + len(row['name']) > 2000:
            fullMsgPart += 1
            fullMsg.append('')
        if len(row['name']) > 2000:
            break
        fullMsg[fullMsgPart] += row['name'] + '\n'

    if len(data['+']) + len(data['-']) != 0:
        discordWebhookFull = os.getenv(ecomSession.webhookFull)
        if discordWebhookFull != None:
            time.sleep(1)
            requests.post(discordWebhookFull, {'content': "Posting full inventory at this time:"})
            for t in fullMsg:
                time.sleep(1)
                requests.post(discordWebhookFull, {'content': t})
            time.sleep(1)
            requests.post(discordWebhookFull, {'content': "End of full inventory"})


def main():
    load_dotenv()
    load_dotenv("postgres.env")
    ecoms = [
        NiigsCa(),
        MetrohobbiesCa(),
        WwwGundamhobbyCa(),
    ]
    db = DBEngine()
    for ecom in ecoms:
        print("Execute: " + str(ecom.__class__.__name__))
        execEcom(ecom, db)


if __name__ == '__main__':
    main()