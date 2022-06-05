import Item from "./Item"
import EcomConfig from "./EcomConfig"
import { Pool } from "pg"
import { RowID } from "../database/DBEngine"

interface saveDataResult {
    error?: string
    execution_id?: number
}
interface diffFromLast2SuccessfulRuns {
    "-": string[]
    "+": string[]
}
interface itemName {
    name: string
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

    async getDiffFromLast2SuccessfulRuns(
        pool: Pool
    ): Promise<diffFromLast2SuccessfulRuns> {
        const diff: diffFromLast2SuccessfulRuns = { "+": [], "-": [] }
        const client = await pool.connect()
        let res = await client.query(
            `SELECT second_last_run_items.item_id as "second_last_run_items.item_id", second_last_run_items.name as "second_last_run_items.name", last_run_items.item_id as "last_run_items.item_id", last_run_items.name as "last_run_items.name"
        FROM (
        SELECT execution_item_stocks.item_id, items.name
        FROM execution_item_stocks
        INNER JOIN executions on execution_item_stocks.execution_id = executions.id
        inner join items on items.id = execution_item_stocks.item_id
        WHERE executions.id IN (
            SELECT executions.id FROM executions
            inner join ecoms on ecoms.id = executions.ecom_id
            WHERE executions.successful = true AND ecoms.website = $1
            ORDER BY executions.id DESC
            LIMIT 1
            OFFSET 1 ROWS
        )) AS second_last_run_items
        FULL OUTER JOIN (SELECT execution_item_stocks.item_id, items.name
        FROM execution_item_stocks
        INNER JOIN executions on execution_item_stocks.execution_id = executions.id
        inner join items on items.id = execution_item_stocks.item_id
        WHERE executions.id IN (
            SELECT executions.id FROM executions
            inner join ecoms on ecoms.id = executions.ecom_id
            WHERE executions.successful = true AND ecoms.website = $1
            ORDER BY executions.id DESC
            LIMIT 1
        )) AS last_run_items ON last_run_items.item_id = second_last_run_items.item_id
        WHERE second_last_run_items.item_id IS NULL OR last_run_items.item_id IS NULL;`,
            [this.config.url]
        )

        client.release()

        for (let r of res.rows) {
            if (r["second_last_run_items.item_id"] != null) {
                diff["-"].push(r["second_last_run_items.name"])
            } else {
                diff["+"].push(r["last_run_items.name"])
            }
        }
        return Promise.resolve(diff)
    }

    async getFullInventory(pool: Pool): Promise<itemName[]> {
        const itemnames: itemName[] = []
        const client = await pool.connect()

        const res = await client.query(
            `SELECT items.name as "name"
        FROM execution_item_stocks
        INNER JOIN executions on execution_item_stocks.execution_id = executions.id
        inner join items on items.id = execution_item_stocks.item_id
        WHERE executions.id IN (
            SELECT executions.id FROM executions
            inner join ecoms on ecoms.id = executions.ecom_id
            WHERE executions.successful = true AND ecoms.website = $1
            ORDER BY executions.id DESC
            LIMIT 1
        )
        ORDER BY items.name`,
            [this.config.url]
        )
        client.release()
        return Promise.resolve(res.rows)
    }
}

export default Ecom
