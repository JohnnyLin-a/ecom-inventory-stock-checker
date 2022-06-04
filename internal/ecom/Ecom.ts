import Item from "./Item";
import EcomConfig from "./EcomConfig"

abstract class Ecom {
    config: EcomConfig
    
    constructor(config: EcomConfig) {
        this.config = config;
    }

    async execute(): Promise<Item[]> {
        throw "not yet implemented";
    }
}

export default Ecom