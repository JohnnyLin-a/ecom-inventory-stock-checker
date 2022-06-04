package common

import "reflect"

func TypeOf(i interface{}) reflect.Type {
	return reflect.ValueOf(i).Type()
}

func PtrOf(i interface{}) reflect.Value {
	return reflect.ValueOf(i)
}
