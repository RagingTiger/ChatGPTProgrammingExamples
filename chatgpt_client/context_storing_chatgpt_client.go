package main

import (
	"fmt"
	"net/http"
	"io/ioutil"
	"encoding/json"
	"os"
	"io"
)

// Global variable to store the chat history
var history []string

// Global variable to store the API key
var apiKey string

// Function to make a post request to the ChatGPT API
func makePostRequest(url string, payload map[string]string) (map[string]interface{}, error) {
	// Create a new http request
	req, err := http.NewRequest("POST", url, nil)
	if err != nil {
		return nil, err
	}

	// Set headers
	req.Header.Add("Content-Type", "application/json")
	req.Header.Add("X-API-KEY", apiKey)

	// Encode the payload
	payloadBytes, err := json.Marshal(payload)
	if err != nil {
		return nil, err
	}

	// Set the body of the request
	req.Body = ioutil.NopCloser(bytes.NewBuffer(payloadBytes))

	// Make the request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}

	// Read the response
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	// Unmarshal the response
	var data map[string]interface{}
	err = json.Unmarshal(body, &data)
	if err != nil {
		return nil, err
	}

	return data, nil
}

// Function to read the config file to get the API key
func readConfig(filename string) error {
	// Open the file
	file, err := os.Open(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	// Read the file
	reader := bufio.NewReader(file)
	for {
		line, err := reader.ReadString('\n')
		if err != nil {
			if err == io.EOF {
				break
			}
			return err
		}

		// Check the line for the API key
		if strings.HasPrefix(line, "API_KEY=") {
			apiKey = strings.TrimPrefix(line, "API_KEY=")
			break
		}
	}

	return nil
}

// Function to get the previous messages from the chat history
func getPreviousMessages(num int) []string {
	start := len(history) - num
	if start < 0 {
		start = 0
	}
	return history[start:]
}

// Function to send a message to the ChatGPT API
func sendMessage(message string) (map[string]interface{}, error) {
	// Add the message to the history
	history = append(history, message)

	// Set the API URL
	url := "https://api.chatgpt.com/v1/message"

	// Set the payload
	payload := map[string]string{
		"message": message,
		"previous_messages": getPreviousMessages(5),
	}

	// Make the request
	data, err := makePostRequest(url, payload)
	if err != nil {
		return nil, err
	}

	return data, nil
}

func main() {
	// Read the config file
	err = readConfig("config.txt")
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	// Get user input
	fmt.Print("Enter your message: ")
	message, _ := reader.ReadString('\n')

	// Send a message to the ChatGPT API
	response, err := sendMessage(message)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	// Print the response
	fmt.Println(response)
}
