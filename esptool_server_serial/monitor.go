package main

import (
	"fmt"
	"log"

	"github.com/tarm/serial"
)

func main() {
	c := &serial.Config{Name: "COM11", Baud: 115200}
	s, err := serial.OpenPort(c)
	if err != nil {
		log.Fatal(err)
	}

	n, err := s.Write([]byte("test"))
	if err != nil {
		log.Fatal(err)
	}

	for true {
		buf := make([]byte, 1280)
		n, err = s.Read(buf)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("%q", buf[:n])
		// log.Printf("%q", buf[:n])
	}
}
