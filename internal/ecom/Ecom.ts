import Item from "./Item"
import EcomConfig from "./EcomConfig"
import { Pool } from "pg"
import { RowID } from "../database/DBEngine"

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

    async saveData(dbpool: Pool, items: Item[]): Promise<saveDataResult> {
        let ecom_id = 0
        let dbItems: Map<string, RowID> = new Map<string, RowID>()
        const client = await dbpool.connect()

        // Find ecom_id for this ecom
        let res = await client.query(
            "SELECT id FROM ecoms WHERE website = $1 LIMIT 1;",
            [this.config.url]
        )
        if (res.rowCount == 0) {
            res = await client.query(
                "INSERT INTO ecoms (website) VALUES ($1) RETURNING id;",
                [this.config.url]
            )
        }
        res.rows.forEach((r) => {
            ecom_id = r.id
        })

        if (ecom_id == 0) {
            return Promise.reject("Cannot find ecom_id for " + this.config.url)
        }

        // Find items in db, set existing items
        res = await client.query(
            `select name, id from items where ecom_id = $1;`,
            [ecom_id]
        )
        if (res.rowCount != 0) {
            res.rows.forEach((row) => {
                dbItems.set(row.name, { id: row.id })
            })
        }

        // Save new execution
        let execution_id = 0
        res = await client.query(
            "INSERT INTO executions (ecom_id) VALUES ($1) RETURNING id;",
            [ecom_id]
        )
        res.rows.forEach((r) => {
            execution_id = r.id
        })
        if (execution_id == 0) {
            return Promise.reject(
                "Cannot insert new execution_id for " + this.config.url
            )
        }

        // Insert new items accordingly & fill in item_id in item objects
        for (let i = 0; i < items.length; i++) {
            let item = items[i]
            if (!dbItems.has(item.name)) {
                // insert new item in db
                let item_id = 0
                res = await client.query(
                    "INSERT INTO items (ecom_id, name) VALUES ($1, $2) RETURNING id;",
                    [ecom_id, item.name]
                )
                for (let r of res.rows) {
                    item_id = r.id
                }
                if (item_id == 0) {
                    return Promise.reject(
                        "Cannot insert new item_id for " + this.config.url
                    )
                }

                items[i].id = item_id
            } else {
                const dbItem = dbItems.get(item.name)
                if (typeof dbItem === "undefined") {
                    return Promise.reject(
                        `Cannot find item_id for item ${item.name} ${this.config.url}`
                    )
                }
                items[i].id = dbItem.id
            }
        }

        // Save execution data
        for (let item of items) {
            await client.query(
                "INSERT INTO execution_item_stocks (execution_id, item_id) VALUES ($1, $2);",
                [execution_id, item.id]
            )
        }

        await client.query(
            "UPDATE executions SET successful = TRUE WHERE id = $1",
            [execution_id]
        )

        client.release()

        return Promise.resolve({ execution_id })
    }
}

export default Ecom
