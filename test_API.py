import requests
import json

# Replace with your actual API Gateway URL
API_GATEWAY_URL = "https://hz2hc4sr80.execute-api.eu-west-1.amazonaws.com/smart_shelf_stage/"
API_KEY = "H0fQFzrA2V5VWhOCX1ifd8JcDEvJQPsZ4rqX1iJU"

headers = {"x-api-key": API_KEY}

# Sample test payload
test_payload = {
  "body": "{ \"topic\": \"smart_shelf_demo/sub\", \"smart_shelf_1_name\": \"hummer\", \"weight_item_1\": \"500\" }"
}

topic = "smart_shelf_demo/sub"

message_payload = {
            "body": json.dumps({
                "topic": topic,
                "smart_shelf_1_name": "hummer 1",
                "smart_shelf_2_name": "hummer 2",
                "smart_shelf_3_name": "hummer 3",
                "weight_item_1": 5,
                "weight_item_2": 10,
                "weight_item_3": 15
            })
        }

# Send POST request to API Gateway
response = requests.post(API_GATEWAY_URL, headers=headers, json=message_payload)

# Print Response
if response.status_code == 200:
    print("✅ API is working! Response received:")
    print(json.dumps(response.json(), indent=4))
else:
    print("🚨 API Test Failed!")
    print(f"Status Code: {response.status_code}")
    print("Response:", response.text)
