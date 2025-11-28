package data_management

import (
	"encoding/csv"
	"encoding/json"
	"os"
)

// FetchDataFromCSV reads data from a CSV file and returns a slice of Data structures.
func FetchDataFromCSV(filePath string) ([]Data, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var data []Data
	reader := csv.NewReader(file)
	// Read CSV headers (optional, adjust as needed)
	headers, err := reader.Read()
	if err != nil {
		return nil, err
	}

	for {
		row, err := reader.Read()
		if err != nil {
			if err == csv.ErrAtEndOfFile {
				break
			}
			return nil, err
		}

		// Parse each row into a Data struct (adjust fields based on your CSV structure)
		record := Data{
			// Map CSV columns to struct fields (example)
			ID:      row[0],
			Name:    row[1],
			Value:   row[2],
		}
		data = append(data, record)
	}
	return data, nil
}

// FetchDataFromJSON reads JSON data from a file and returns a slice of Data structures.
func FetchDataFromJSON(filePath string) ([]Data, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var data []Data
	decoder := json.NewDecoder(file)
	for decoder.More() {
		var record Data
		err := decoder.Decode(&record)
		if err != nil {
			return nil, err
		}
		data = append(data, record)
	}
	return data, nil
}

// Data represents a financial record (adjust fields based on your requirements)
type Data struct {
	ID      string `json:"id"`
	Name    string `json:"name"`
	Value   string `json:"value"`
	// Add more fields as needed
}
