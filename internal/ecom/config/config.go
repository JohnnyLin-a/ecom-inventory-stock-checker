package config

import (
	"reflect"

	"github.com/JohnnyLin-a/ecom-inventory-stock-checker/internal/common"
	"github.com/JohnnyLin-a/ecom-inventory-stock-checker/internal/ecom"
	"github.com/JohnnyLin-a/ecom-inventory-stock-checker/internal/ecom/gundamhobbyca"
)

var allEcoms = map[string]struct {
	EcomBase *ecom.EcomBase
	Type     reflect.Type
	Ptr      reflect.Value
}{
	"gundamhobbyca": {
		EcomBase: &gundamhobbyca.Impl.EcomBase,
		Type:     common.TypeOf(gundamhobbyca.Impl),
		Ptr:      common.PtrOf(&gundamhobbyca.Impl),
	},
}
