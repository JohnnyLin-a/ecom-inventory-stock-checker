/**
 * Main entrypoint for ecom-inventory-stock-checker
 */
import { config } from "dotenv"
config({ path: "./postgres.env" })

import axios from "axios"
import { setTimeout } from "timers/promises"
import Ecom from "./internal/ecom/Ecom"
import EcomConfig from "./internal/ecom/EcomConfig"
import EcomMap from "./internal/ecom/EcomMap"
import Item from "./internal/ecom/EcomItem"
import DBEngine from "./internal/database/DBEngine"
import * as DiscordHelper from "./internal/common/discordhelper"

const ecomConfigs: EcomConfig[] = process.env.ECOM_CONFIG
    ? JSON.parse(process.env.ECOM_CONFIG as string)
    : require("./ecom_configs.json")

const ecomImpls: Ecom[] = []
let ecomComplete = 0

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
                console.log(ecomImpl.config.url, "done exec")
                // Save execution data to db
                console.log(
                    ecomImpl.config.url,
                    await ecomImpl.saveData(DBEngine, items)
                )
                console.log(ecomImpl.config.url, "saved")
                // Compare diff against previous run
                const diffs = await ecomImpl.getDiffFromLast2SuccessfulRuns(
                    DBEngine
                )
                console.log(ecomImpl.config.url, diffs)

                // Send to discord
                const discordChunks: any = {}
                /*
                Template:
                {
                    `webhook_url`: string[] <- chunks of discord msg to send to that webhook_url
                }
                */
                discordChunks[ecomImpl.config.webhook_diff] = []
                discordChunks[ecomImpl.config.webhook_full] = []

                // Send inventory change (diffs)
                if (diffs["+"].length != 0) {
                    console.log(ecomImpl.config.url, "New stock")
                    const splits = DiscordHelper.splitMsg(
                        diffs["+"],
                        "@everyone\nNew arrivals:"
                    )
                    for (let split of splits) {
                        discordChunks[ecomImpl.config.webhook_diff].push(split)
                    }
                }
                if (diffs["-"].length != 0) {
                    console.log(ecomImpl.config.url, "oos")
                    const splits = DiscordHelper.splitMsg(
                        diffs["-"],
                        "Recently out of stock:"
                    )
                    for (let split of splits) {
                        discordChunks[ecomImpl.config.webhook_diff].push(split)
                    }
                }
                if (diffs["+"].length + diffs["-"].length > 0) {
                    discordChunks[ecomImpl.config.webhook_diff].push(
                        "End of stock change"
                    )

                    // Send full inventory
                    const fullInventory = await ecomImpl.getFullInventory(
                        DBEngine
                    )
                    console.log(ecomImpl.config.url, "full inv")
                    const splits = DiscordHelper.splitMsg(
                        fullInventory,
                        "Posting full inventory at this time:",
                        "End of full inventory"
                    )
                    for (let split of splits) {
                        discordChunks[ecomImpl.config.webhook_full].push(split)
                    }
                }

                // Bazooka all the chunk messages to Discord
                console.log(ecomImpl.config.url, "Sending discord msgs")
                for (let url in discordChunks) {
                    ;(async (endpoint) => {
                        for (let chunk of discordChunks[endpoint]) {
                            const response = await axios.post(endpoint, {
                                content: chunk,
                            })
                            await setTimeout(
                                Number(
                                    response.headers["x-ratelimit-limit"].trim()
                                ) * 1000
                            )
                        }
                    })(url)
                }
                console.log(ecomImpl.config.url, "end")
            })
            .catch((reason) => {
                console.log(reason)
            })
            .finally(() => {
                ecomComplete++
            })
    })

    // Big loop to finish off the discord chunks as long as the ecom scrape has not finished yet, or when there are still chunks to send
})()
