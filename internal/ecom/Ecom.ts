import Item from "./Item"
import EcomConfig from "./EcomConfig"

interface saveDataResult {
    error?: string
    execution_id?: number
}
abstract class Ecom {
    config: EcomConfig

    constructor(config: EcomConfig) {
        this.config = config
    }

    async execute(): Promise<Item[]> {
        throw "not yet implemented"
    }

    async saveData(items: Item[]): Promise<saveDataResult> {
        return Promise.resolve({})
    }
}

export default Ecom
