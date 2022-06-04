package gundamhobbyca

import (
	"log"

	"github.com/JohnnyLin-a/ecom-inventory-stock-checker/internal/ecom"
)

var Impl = GundamhobbyCa{}

type GundamhobbyCa struct {
	ecom.EcomBase
}

func (impl GundamhobbyCa) Execute() ([]ecom.Item, error) {
	log.Println("Execute GundamhobbyCa", impl.Url)
	return []ecom.Item{}, nil
}
