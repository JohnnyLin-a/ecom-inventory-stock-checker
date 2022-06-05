class Item {
    quantity: number
    name: string
    id?: number

    constructor(quantity: number, name: string) {
        this.quantity = quantity
        this.name = name
    }
}

export default Item
