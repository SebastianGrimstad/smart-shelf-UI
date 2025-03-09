import requests
import json  # Import json to handle nested JSON decoding

# Replace with your actual API Gateway invoke URL
API_URL = "https://m9ab5gi6o4.execute-api.eu-west-1.amazonaws.com/smart_shelf_company/companyInfo"

# Set the company name as a query parameter
params = {"companyName": "Factbird"}

print("Sending request to API...")

try:
    response = requests.get(API_URL, params=params)
    print(f"Response Status Code: {response.status_code}")

    if response.status_code == 200:
        # Decode JSON response
        data = response.json()
        
        print("Raw Response Data:")
        print(data)

        # Extract the 'body' field and parse it as JSON
        body_data = json.loads(data["body"])  # Fix: Decode JSON inside 'body'

        # Extract values into variables
        company_name = body_data.get("CompanyName", "Unknown")
        total_shelves = body_data.get("TotalShelves", 0)
        shelf_names = body_data.get("SmartShelfNames", [])

        # Print extracted values
        print(f"Company Name: {company_name}")
        print(f"Total Shelves: {total_shelves}")
        print(f"Smart Shelf Names: {', '.join(shelf_names) if shelf_names else 'None'}")

    else:
        print(f"Error: {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print("Request failed:", e)
