import axios from "axios"
import { setTimeout } from "timers/promises"
import Ecom from "./Ecom"
import Item from "./EcomItem"
import * as cheerio from "cheerio"
import { REQUEST_HEADER } from "./EcomConfig"

class AgesThreeAndUpCa extends Ecom {
    async execute(): Promise<Item[]> {
        console.log(this.config.url, "execute")

        let page = 0
        let maxPage = 0
        // Fetch in-stock items
        const items: Item[] = []
        while (page == 0 || page < maxPage) {
            console.log(this.config.url, ++page, "/", maxPage)
            const response = await axios.get(
                this.config.url + `/collections/gundam-model-kits?page=${page}`,
                {
                    headers: REQUEST_HEADER,
                }
            )
            if (response.status < 200 || response.status >= 300) {
                return Promise.reject(response.status)
            }
            await setTimeout(1000)

            const $ = cheerio.load(response.data)
            if (maxPage == 0) {
                const pagination = $(".page>a")
                maxPage = Number(
                    $(pagination[pagination.length - 1])
                        .text()
                        .trim()
                )
            }

            $("main>div>div>.grid__item>a.product-card").each((i, product) => {
                if (
                    $(product).find(
                        ".product-card__info>.product-card__availability"
                    ).length == 0
                ) {
                    items.push(
                        new Item(
                            1,
                            $(product)
                                .find(".product-card__info>.product-card__name")
                                .text()
                                .trim()
                        )
                    )
                }
            })
        }

        return Promise.resolve(items)
    }
}

export default AgesThreeAndUpCa
