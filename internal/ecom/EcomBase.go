package ecom

type EcomBase struct {
	Url         string `json:"url"`
	WebhookFull string `json:"webhook_full"`
	WebhookDiff string `json:"webhook_diff"`
}

type Execute interface {
	Execute() ([]Item, error)
}
