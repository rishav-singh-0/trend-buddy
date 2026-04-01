package domain

type Decimal string

type Currency string

func (d Decimal) String() string {
	return string(d)
}
