import axios, { AxiosRequestHeaders } from "axios"
import * as cheerio from "cheerio"
import { setTimeout } from "timers/promises"
import Ecom from "./Ecom"
import Item from "./Item"
import { REQUEST_HEADER } from "./EcomConfig"

class GundamhobbyCa extends Ecom {
    async execute(): Promise<Item[]> {
        console.log("execute from GundamhobbyCa")
        const items: Item[] = []
        let nextUrl: string | undefined = this.config.url + "/collections/all"
        let page = 0
        while (typeof nextUrl !== "undefined") {
            console.log(this.config.url, ++page)
            let response = await axios.get(nextUrl, {
                headers: REQUEST_HEADER,
            })
            if (response.status < 200 || response.status >= 300) {
                return Promise.reject(response.status)
            }
            const $ = cheerio.load(response.data)

            nextUrl = $("link[rel='next']").attr("href")
            if (typeof nextUrl !== "undefined") {
                nextUrl = this.config.url + nextUrl
                await setTimeout(1000)
            }

            $("main>.grid>div.grid__item>div>div.grid__item").each(
                (i, elem) => {
                    if (!$(elem).hasClass("sold-out")) {
                        const title = $(elem).find("p.grid-link__title").text()
                        items.push(new Item(1, title))
                    }
                }
            )
        }

        return Promise.resolve(items)
    }
}

export default GundamhobbyCa
