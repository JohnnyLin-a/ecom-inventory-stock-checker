import Ecom from "./Ecom";
import Item from "./Item";

class NiigsCa extends Ecom {
    async execute(): Promise<Item[]> {
        return new Promise(function(resolve, reject) {
            console.log("execute from NiigsCa")
            setTimeout(() => {
                console.log("done from NiigsCa")
                resolve([])
            }, 3000)
        });
    }
}

export default NiigsCa