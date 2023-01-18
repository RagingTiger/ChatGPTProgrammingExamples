package main

import (
	"fmt"
	"net/http"
	"io/ioutil"
	"bytes"
)

func main() {
	url := "https://api.chatgpt.com/v2/message"

	//Previous message/response pair
	prevMessage := "Hello"
	prevResponse := "Hi there!"

	//Create the payload
	payload := []byte(`{"prompt": "` + prevMessage + `", "context": [{"previous_message": "` + prevMessage + `", "previous_response": "` + prevResponse + `"}]}`)

	client := &http.Client{}

	//Create the request
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(payload))

	if err != nil {
		fmt.Println(err)
	}

	//Set request headers
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer <YourAPIKeyHere>")

	//Make the request
	resp, err := client.Do(req)

	if err != nil {
		fmt.Println(err)
	}

	//Read the response
	body, err := ioutil.ReadAll(resp.Body)

	if err != nil {
		fmt.Println(err)
	}

	//Print the response
	fmt.Println(string(body))
}
