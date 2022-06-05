import { setTimeout } from "timers/promises";
import Ecom from "./Ecom";
import Item from "./Item";

class NiigsCa extends Ecom {
    async execute(): Promise<Item[]> {
        console.log("execute from NiigsCa")
        return Promise.resolve([])
    }
}

export default NiigsCa