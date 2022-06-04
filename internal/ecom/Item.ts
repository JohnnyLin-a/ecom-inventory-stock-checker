class Item {
    quantity: number;
    name: string;
    category: string;
    
    constructor(quantity: number, name: string, category: string) {
        this.quantity = quantity;
        this.name = name;
        this.category = category;
    }
}

export default Item;