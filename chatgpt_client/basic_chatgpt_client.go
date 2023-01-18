package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
)

const openaiEndpoint = "https://api.openai.com/v1/engines/chatbot/completions"

// RequestBody is the json structure for the request body sent to OpenAI
type RequestBody struct {
	Prompt string `json:"prompt"`
	MaxTokens int `json:"max_tokens"`
	Temperature float32 `json:"temperature"`
	TopP float32 `json:"top_p"`
	N int `json:"n"`
}

func main() {
	fmt.Println("Welcome to OpenAI ChatGPT API Client")

	// Get the OpenAI API key
	apiKey := os.Getenv("OPENAI_API_KEY")
	if apiKey == "" {
		fmt.Println("Please provide the OpenAI API key as an environment variable")
		os.Exit(1)
	}

	// Start the interactive prompt
	fmt.Println("Type your query below and press enter to submit:")
	for {
		// Read the input from the user
		var query string
		fmt.Scanln(&query)

		// Create the request body
		requestBody := RequestBody{
			Prompt: query,
			MaxTokens: 1000,
			Temperature: 0.7,
			TopP: 0.9,
			N: 1,
		}

		// Encode the request body as json
		requestBodyBytes, err := json.Marshal(requestBody)
		if err != nil {
			fmt.Printf("Error encoding json: %v\n", err)
			os.Exit(1)
		}

		// Create the http client
		client := &http.Client{}

		// Create the request
		req, err := http.NewRequest("POST", openaiEndpoint, strings.NewReader(string(requestBodyBytes)))
		if err != nil {
			fmt.Printf("Error creating http request: %v\n", err)
			os.Exit(1)
		}

		// Add the API key to the request
		req.Header.Add("Authorization", fmt.Sprintf("Bearer %s", apiKey))

		// Send the request
		resp, err := client.Do(req)
		if err != nil {
			fmt.Printf("Error sending http request: %v\n", err)
			os.Exit(1)
		}

		// Read the response
		respBytes, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			fmt.Printf("Error reading http response: %v\n", err)
			os.Exit(1)
		}

		// Decode the response
		var respBody struct {
			Choices []struct {
				Text string `json:"text"`
				Index int `json:"index"`
			} `json:"choices"`
		}
		err = json.Unmarshal(respBytes, &respBody)
		if err != nil {
			fmt.Printf("Error decoding response: %v\n", err)
			os.Exit(1)
		}

		// Print the response
		fmt.Println("Response:")
		for _, c := range respBody.Choices {
			fmt.Printf("%d: %s\n", c.Index, c.Text)
		}
	}
}
