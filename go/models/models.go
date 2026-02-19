package models

// Use built-in primitives
type Celsius float64

// Attach new behavior to a new data
func (temp Celsius) IsAboveFreezing() bool {
	return temp > 0
}