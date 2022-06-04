package main

import (
	"log"
	"reflect"

	"github.com/JohnnyLin-a/ecom-inventory-stock-checker/pkg/api/ecom"
	"github.com/JohnnyLin-a/ecom-inventory-stock-checker/pkg/api/ecom/gundamhobbyca"
)

func typeOf(i interface{}) reflect.Type {
	return reflect.ValueOf(i).Type()
}

func ptrOf(i interface{}) reflect.Value {
	return reflect.ValueOf(i)
}

func main() {
	var allEcoms = map[string]struct {
		EcomBase *ecom.EcomBase `json="config"`
		Type     reflect.Type   `json="-"`
		Ptr      reflect.Value  `json="-"`
	}{
		"gundamhobbyca": {
			EcomBase: &gundamhobbyca.Impl.EcomBase,
			Type:     typeOf(gundamhobbyca.Impl),
			Ptr:      ptrOf(&gundamhobbyca.Impl),
		},
	}
	for _, ecomEntry := range allEcoms {
		log.Println(ecomEntry.Type, ecomEntry.Ptr)
	}
}
