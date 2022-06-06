import { itemName } from "../ecom/Ecom"

const MAX_CHARS = 2000
export const splitMsg = (
    items: string[] | itemName[],
    head?: string,
    tail?: string
): string[] => {
    let s = ""
    if (head) {
        s = head + "\n"
    }
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

    if (tail) {
        if (s.length + tail.length < MAX_CHARS) {
            s += tail
        } else {
            chunks.push(s)
            s = tail
        }
    }

    if (s !== "") {
        chunks.push(s)
    }
    return chunks
}
