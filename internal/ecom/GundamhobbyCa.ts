import Ecom from "./Ecom";
import Item from "./Item";

class GundamhobbyCa extends Ecom {
    async execute(): Promise<Item[]> {
        return new Promise(function(resolve, reject) {
            console.log("execute from GundamhobbyCa")
            setTimeout(() => {
                console.log("done from GundamhobbyCa")
                resolve([])
            }, 5000)
        });
    }
}

export default GundamhobbyCa