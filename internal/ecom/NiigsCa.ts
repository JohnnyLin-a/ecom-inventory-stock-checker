import axios from "axios"
import { setTimeout } from "timers/promises"
import Ecom from "./Ecom"
import Item from "./EcomItem"
import * as cheerio from "cheerio"
import { REQUEST_HEADER } from "./EcomConfig"

class NiigsCa extends Ecom {
    async execute(): Promise<Item[]> {
        console.log(this.config.url, "execute")

        // Get last page number
        let lastPageNumber = 0
        let response = await axios.get(
            this.config.url +
                "/collections/all-availible-items?sort_by=title-ascending&page=1",
            {
                headers: REQUEST_HEADER,
            }
        )
        if (response.status < 200 || response.status >= 300) {
            return Promise.reject(response.status)
        }
        const $ = cheerio.load(response.data)
        const pagination = $("ul.pagination-custom>li")
        lastPageNumber = Number(
            $(pagination[pagination.length - 2])
                .text()
                .trim()
        )
        console.log(this.config.url, "lastPageNumber", lastPageNumber)

        // Fetch in-stock items
        const items: Item[] = []
        for (let page = 1; page <= lastPageNumber; page++) {
            console.log(this.config.url, page, "/", lastPageNumber)
            response = await axios.get(
                this.config.url +
                    "/collections/all-availible-items?sort_by=title-ascending&page=" +
                    page
            )
            await setTimeout(1000)

            const $ = cheerio.load(response.data)
            $(".grid-uniform>div.grid-item").each((i, itemGrid) => {
                items.push({
                    name: $(itemGrid).find("a>p").text().trim(),
                    quantity: 1,
                })
            })
        }

        return Promise.resolve(items)
    }
}

export default NiigsCa
