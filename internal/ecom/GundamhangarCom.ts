import axios from "axios"
import { setTimeout } from "timers/promises"
import Ecom from "./Ecom"
import Item from "./EcomItem"
import { REQUEST_HEADER } from "./EcomConfig"

class GundamhangarCom extends Ecom {
    async execute(): Promise<Item[]> {
        console.log(this.config.url, "execute")
        const items: Item[] = []
        let page = 0
        let maxPage = 0
        while (page == 0 || page < maxPage) {
            console.log(this.config.url, ++page, "/", maxPage)
            let nextUrl: string | undefined =
                this.config.url +
                `/api/products?category=&featured=&groupproducts=&gundambaseexclusive=&limit=100&new=&outofstock=&page=${page}&pbandai=&preorder=&rare=&series=&sort=&special=&thirdparty=&thirdpartyname=`
            let response = await axios.get(nextUrl, {
                headers: REQUEST_HEADER,
            })
            if (response.status < 200 || response.status >= 300) {
                return Promise.reject(response.status)
            }
            await setTimeout(1000)
            if (maxPage == 0) {
                maxPage = response.data.pagination.total
            }

            ;(
                response.data as {
                    data: { type: string; title: string; stock: string }[]
                }
            ).data.forEach((item) => {
                if (item.stock != "0") {
                    items.push(new Item(1, item.title))
                }
            })
        }

        return Promise.resolve(items)
    }
}

export default GundamhangarCom
