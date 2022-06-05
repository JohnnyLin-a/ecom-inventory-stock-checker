/**
 * Main entrypoint for ecom-inventory-stock-checker
 */
import Ecom from "./internal/ecom/Ecom"
import EcomConfig from "./internal/ecom/EcomConfig"
import EcomMap from "./internal/ecom/EcomMap"
import Item from "./internal/ecom/Item"

const _ecomConfigs = process.env.ECOM_CONFIG
    ? JSON.parse(process.env.ECOM_CONFIG)
    : require("./ecom_configs.json")

const ecomConfigs = _ecomConfigs as EcomConfig[]
const ecomImpls: Ecom[] = []

console.log("Detecting stores...")
ecomConfigs.forEach((config) => {
    if (typeof EcomMap[config.url] !== "undefined") {
        console.log("Found", config.url)
        ecomImpls.push(new EcomMap[config.url](config))
    }
})

ecomImpls.forEach((val) => {
    val.execute()
        .then((items: Item[]) => {
            console.log(JSON.stringify(items))
        })
        .catch((reason) => {
            console.log(reason)
        })
})
