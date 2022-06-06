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
import * as DiscordHelper from "./internal/common/discordhelper"

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

    ecomImpls.forEach((ecomImpl) => {
        ecomImpl
            .execute()
            .then(async (items: Item[]) => {
                console.log("done exec")
                // Save execution data to db
                await ecomImpl.saveData(DBEngine, items)
                console.log("saved")
                // Compare diff against previous run
                const diffs = await ecomImpl.getDiffFromLast2SuccessfulRuns(
                    DBEngine
                )
                console.log("diffs", diffs)
                // Send to discord

                // Send inventory change (diffs)
                if (diffs["+"].length != 0) {
                    console.log("New stock")
                    discordChunks.push({
                        webhook: ecomImpl.config.webhook_diff,
                        content: "@everyone\nNew arrivals:\n",
                    })
                    const splits = DiscordHelper.splitMsg(diffs["+"])
                    for (let split of splits) {
                        discordChunks.push({
                            webhook: ecomImpl.config.webhook_diff,
                            content: split,
                        })
                    }
                }
                if (diffs["-"].length != 0) {
                    console.log("oos")
                    discordChunks.push({
                        webhook: ecomImpl.config.webhook_diff,
                        content: "Recently out of stock:\n",
                    })
                    const splits = DiscordHelper.splitMsg(diffs["-"])
                    for (let split of splits) {
                        discordChunks.push({
                            webhook: ecomImpl.config.webhook_diff,
                            content: split,
                        })
                    }
                }
                if (diffs["+"].length + diffs["-"].length > 0) {
                    discordChunks.push({
                        webhook: ecomImpl.config.webhook_diff,
                        content: "End of stock change",
                    })

                    // Send full inventory
                    const fullInventory = await ecomImpl.getFullInventory(
                        DBEngine
                    )
                    console.log("full inv")
                    const splits = DiscordHelper.splitMsg(fullInventory)
                    discordChunks.push({
                        webhook: ecomImpl.config.webhook_full,
                        content: "Posting full inventory at this time:",
                    })
                    for (let split of splits) {
                        discordChunks.push({
                            webhook: ecomImpl.config.webhook_full,
                            content: split,
                        })
                    }
                    discordChunks.push({
                        webhook: ecomImpl.config.webhook_full,
                        content: "End of full inventory",
                    })
                    console.log("end", ecomImpl.config.url)
                }
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
                console.log(
                    response.status,
                    "Failed to send content to",
                    reqData.webhook
                )
            }
            await setTimeout(1000) // 3s is the buffer time for discord
        }
        await setTimeout(1) // Prevents cpu from being pinned at 100%
    }
})()
