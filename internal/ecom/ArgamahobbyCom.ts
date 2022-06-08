import axios from "axios"
import { setTimeout } from "timers/promises"
import Ecom from "./Ecom"
import Item from "./EcomItem"
import * as cheerio from "cheerio"
import { REQUEST_HEADER } from "./EcomConfig"

class ArgamahobbyCom extends Ecom {
    async execute(): Promise<Item[]> {
        console.log(this.config.url, "execute")

        let page = 0
        let maxPage = 0
        // Fetch in-stock items
        const items: Item[] = []
        while (page == 0 || page < maxPage) {
            console.log(this.config.url, ++page, "/", maxPage)
            const response = await axios.get(
                this.config.url +
                    `/collections/model-kits?page=${page}&view=view-48&grid_list=grid-view`,
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
                const pagination = $("a.pagination--item")
                maxPage = Number(
                    $(pagination[pagination.length - 2])
                        .text()
                        .trim()
                )
            }

            $(".productitem").each((i, product) => {
                if (
                    $(product).find("a>figure>span.productitem__badge--soldout")
                        .length == 0
                ) {
                    items.push(
                        new Item(
                            1,
                            $(product)
                                .find(
                                    ".productitem--info>.productitem--title>a"
                                )
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

export default ArgamahobbyCom
