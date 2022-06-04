package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"reflect"

	"github.com/JohnnyLin-a/ecom-inventory-stock-checker/internal/ecom"
	"github.com/JohnnyLin-a/ecom-inventory-stock-checker/internal/ecom/gundamhobbyca"
)



func loadConfig() {

}

func main() {

	for k, ecomEntry := range allEcoms {
		log.Println(k, ecomEntry.Type, ecomEntry.Ptr, ecomEntry.EcomBase.Url)
	}
	ecomConfigFile, err := os.Open("ecom_config.json")
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	ecomConfigBytes, err := ioutil.ReadAll(ecomConfigFile)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	err = json.Unmarshal(ecomConfigBytes, &allEcoms)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	for k, ecomEntry := range allEcoms {
		log.Println(k, ecomEntry.Type, ecomEntry.Ptr, ecomEntry.EcomBase.Url)
	}
}
