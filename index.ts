/**
 * Main entrypoint for ecom-inventory-stock-checker
 */
import axios from "axios"
import { setTimeout } from "timers/promises"
import Ecom from "./internal/ecom/Ecom"
import EcomConfig from "./internal/ecom/EcomConfig"
import EcomMap from "./internal/ecom/EcomMap"
import Item from "./internal/ecom/Item"
import DBEngine from "./internal/database/DBEngine"

const ecomConfigs: EcomConfig[] = process.env.ECOM_CONFIG
    ? JSON.parse(process.env.ECOM_CONFIG)
    : require("./ecom_configs.json")

const ecomImpls: Ecom[] = []
let ecomComplete = 0
interface iDiscordChunks {
    webhook: string
    content: string
}
const discordChunks: iDiscordChunks[] = []

// Start of execution below

;(async () => {
    console.log("Detecting stores...")
    ecomConfigs.forEach((config) => {
        if (typeof EcomMap[config.url] !== "undefined") {
            console.log("Found", config.url)
            ecomImpls.push(new EcomMap[config.url](config))
        }
    })

    ecomImpls.forEach((val) => {
        val.execute()
            .then(async (items: Item[]) => {
                // Save execution data to db
                const saveDataResult = await val.saveData(DBEngine, items)
                
                // Send to discord if save is successful

                // Compare diff against previous run & get full inventory

                // Send to discord in chunk
            })
            .catch((reason) => {
                console.log(reason)
            })
            .finally(() => {
                ecomComplete++
            })
    })

    // Big loop to finish off the discord chunks as long as the ecom scrape has not finished yet, or when there are still chunks to send
    while (ecomComplete !== ecomImpls.length || discordChunks.length !== 0) {
        const reqData = discordChunks.shift()
        if (reqData) {
            const response = await axios.post(reqData.webhook, {
                content: reqData.content,
            })
            if (response.status < 200 || response.status >= 300) {
                console.log("Failed to send content to", reqData.webhook)
            }
            await setTimeout(3000) // 3s is the buffer time for discord
        }
        await setTimeout(1) // Prevents cpu from being pinned at 100%
    }
})()
