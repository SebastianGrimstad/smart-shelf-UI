import requests
import json
from collections import OrderedDict  # Use OrderedDict for sorted grouping

# API Gateway URL & Key
API_URL = "https://z15rivu3vh.execute-api.eu-west-1.amazonaws.com/Smart_Shelf_stage"
API_KEY = "H0fQFzrA2V5VWhOCX1ifd8JcDEvJQPsZ4rqX1iJU"

# Define a struct-like class to store shelf data
class SmartShelfData:
    def __init__(self, time, shelf_id, smart_shelf_id, name, measure_name, measure_value):
        self.time = time
        self.smart_shelf_id = smart_shelf_id
        self.shelf_id = int(shelf_id)  # Ensure shelf_Id is treated as a number
        self.name = name
        self.measure_name = measure_name
        self.measure_value = measure_value

    def __repr__(self):
        return (
            f"SmartShelfData(\n"
            f"    time           = {self.time}\n"
            f"    smart_shelf_id = {self.smart_shelf_id}\n"
            f"    shelf_id       = {self.shelf_id}\n"
            f"    name           = {self.name}\n"
            f"    measure_name   = {self.measure_name}\n"
            f"    measure_value  = {self.measure_value}\n"
            f")"
        )

def fetch_shelf_data(smart_shelf_id):
    """
    Fetches and groups Smart Shelf data from AWS API Gateway.

    Args:
        smart_shelf_id (str): The ID of the smart shelf.

    Returns:
        OrderedDict: Grouped shelf data sorted by shelf_Id.
    """
    # Set up headers and query parameters
    headers = {"x-api-key": API_KEY}
    params = {"smart_shelf_id": smart_shelf_id}

    try:
        # Make the GET request to API Gateway
        response = requests.get(API_URL, headers=headers, params=params)

        if response.status_code == 200:
            response_data = response.json()  # First level of JSON parsing

            # Extract the actual JSON list from 'body' field (which is a string)
            data = json.loads(response_data["body"])

            # Convert JSON response into structured objects
            shelf_data_list = [SmartShelfData(**item) for item in data]

            # Sort the data by `shelf_Id` before grouping
            shelf_data_list.sort(key=lambda x: x.shelf_id)

            # Use OrderedDict to maintain sorted order
            grouped_data = OrderedDict()
            for shelf_data in shelf_data_list:
                if shelf_data.shelf_id not in grouped_data:
                    grouped_data[shelf_data.shelf_id] = []
                grouped_data[shelf_data.shelf_id].append(shelf_data)

            return grouped_data  # ✅ Now returns structured grouped data

        else:
            print(f"Error: {response.status_code}, Message: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None
