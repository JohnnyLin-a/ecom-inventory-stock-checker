interface EcomConfig {
    name: string
    url: string
    webhook_full: string
    webhook_diff: string
}

export default EcomConfig

export const REQUEST_HEADER = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
}