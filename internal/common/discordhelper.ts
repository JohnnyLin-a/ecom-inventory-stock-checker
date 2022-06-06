import { itemName } from "../ecom/Ecom"

const MAX_CHARS = 2000
export const splitMsg = (items: string[] | itemName[]): string[] => {
    let s = ""
    let chunks: string[] = []
    for (let item of items) {
        if (
            s.length +
                (typeof item === "string" ? item.length : item.name.length) >
            MAX_CHARS
        ) {
            chunks.push(s)
            s = ""
        }
        s += (typeof item === "string" ? item : item.name) + "\n"
    }
    if (s !== "") {
        chunks.push(s)
    }
    return chunks
}
