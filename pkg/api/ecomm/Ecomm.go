package ecomm

import "errors"

type Executer interface {
	Execute() error
}

type EcommBase struct {
	url string
}

func (EcommBase) Execute() error {
	return errors.New("Not yet implemented")
}
