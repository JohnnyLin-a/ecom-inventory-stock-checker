import axios, { AxiosRequestHeaders } from "axios"
import * as cheerio from "cheerio/lib/slim"
import { setTimeout } from "timers/promises"
import Ecom from "./Ecom"
import Item from "./Item"

class GundamhobbyCa extends Ecom {
    static get REQUEST_HEADER(): AxiosRequestHeaders {
        return {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
        }
    }

    async execute(): Promise<Item[]> {
        console.log("execute from GundamhobbyCa")
        let nextUrl: string | undefined = this.config.url + "/collections/all"

        while (typeof nextUrl !== "undefined") {
            await setTimeout(1000)
            let response = await axios.get(nextUrl, {
                headers: GundamhobbyCa.REQUEST_HEADER,
            })
            if (response.status < 200 || response.status >= 300) {
                return Promise.reject(response.status)
            }
            const $ = cheerio.load(response.data)

            nextUrl = $("link[rel='next']").attr("href")
            if (typeof nextUrl !== "undefined") {
                nextUrl = this.config.url + nextUrl
            }

            $("main>.grid>div.grid__item>div>div.grid__item").each(
                (i, elem) => {
                    if (!$(elem).hasClass("sold-out")) {
                        const title = $(elem).find("p.grid-link__title").text()
                        console.log(title)
                    }
                }
            )
            break
        }

        return Promise.resolve([])
    }
}

export default GundamhobbyCa
