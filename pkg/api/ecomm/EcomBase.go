package ecomm

import (
	"github.com/JohnnyLin-a/ecom-inventory-stock-checker/pkg/api/ecomm/niigsca"
	"github.com/JohnnyLin-a/ecom-inventory-stock-checker/pkg/api/ecomm/scifianimeca"
	"github.com/JohnnyLin-a/ecom-inventory-stock-checker/pkg/api/ecomm/wwwgundamhobbyca"
)

var AllEcoms = map[string]EcomBase{
	"wwwgundamhobbyca": {Execute: wwwgundamhobbyca.Execute},
	"niigsca":          {Execute: niigsca.Execute},
	"scifianimeca":     {Execute: scifianimeca.Execute},
}

type EcomBase struct {
	Url         string `json:"url"`
	WebhookFull string `json:"webhook_full"`
	WebhookDiff string `json:"webhook_diff"`
	Execute     func() error `json:"-"`
}
