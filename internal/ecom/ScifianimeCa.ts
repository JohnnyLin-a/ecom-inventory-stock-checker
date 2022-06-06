import axios from "axios"
import { setTimeout } from "timers/promises"
import Ecom from "./Ecom"
import Item from "./Item"
import * as cheerio from "cheerio"

class ScifianimeCa extends Ecom {
    async execute(): Promise<Item[]> {
        console.log(this.config.url, "execute")
        let maxPage = 0

        // Find maxPage
        let response = await axios.get(
            this.config.url + "/page/1/?post_type=product&s=&product_cat="
        )
        if (response.status < 200 || response.status >= 300) {
            return Promise.reject(response.status)
        }
        const $ = cheerio.load(response.data)
        const pagination = $("ul.page-numbers>li")
        maxPage = Number(
            $(pagination[pagination.length - 2])
                .find("a")
                .text()
                .trim()
        )
        console.log(this.config.url, "maxPage", maxPage)

        // Find in-stock items
        const items: Item[] = []
        for (let page = 1; page <= maxPage; page++) {
            console.log(this.config.url, page, "/", maxPage)
            response = await axios.get(
                this.config.url +
                    "/page/" +
                    page +
                    "/?post_type=product&s=&product_cat="
            )
            await setTimeout(1000)

            const $ = cheerio.load(response.data)
            $("ul.products>li").each((i, itemGrid) => {
                if (
                    $(itemGrid).find("a.button").text().trim() == "Add to cart"
                ) {
                    items.push({
                        name: $(itemGrid).find("a>h2").text().trim(),
                        quantity: 1,
                    })
                }
            })
        }
        return Promise.resolve(items)
    }
}

export default ScifianimeCa
