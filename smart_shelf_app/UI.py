from flask import Flask, request, jsonify, render_template
import json
import boto3
import requests
from API import fetch_shelf_data

app = Flask(__name__)

# AWS IoT Region
AWS_REGION = "eu-west-1"
# API Gateway URL & Key
API_COMPANY_INFO_URL = "https://m9ab5gi6o4.execute-api.eu-west-1.amazonaws.com/smart_shelf_company/companyInfo"
API_UPDATE_INFO_URL = "https://hz2hc4sr80.execute-api.eu-west-1.amazonaws.com/smart_shelf_stage/"
API_KEY = "H0fQFzrA2V5VWhOCX1ifd8JcDEvJQPsZ4rqX1iJU"

def get_smart_shelves(username):
    """Fetch Smart Shelf data from API dynamically."""
    try:
        response = requests.get(API_COMPANY_INFO_URL, params={"companyName": username})
        if response.status_code == 200:
            data = response.json()
            body_data = json.loads(data["body"])  # Decode the nested JSON

            total_shelves = body_data.get("TotalShelves", 0)
            smart_shelves = body_data.get("SmartShelfNames", [])  # Keep list format

            return total_shelves, smart_shelves
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return 0, []  # Default values on failure

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return 0, []

@app.route('/')
def home():
    """ Serves the login page """
    return render_template("index.html")

@app.route('/fetch_shelf_data', methods=['GET'])
def fetch_shelf_data_api():
    """ Fetches Smart Shelf Data and returns it as JSON """
   
    # ✅ Get the smart_shelf_id from request arguments (query params)
    smart_shelf_id = request.args.get("smart_shelf_id", "")  # Default to smart_shelf_1 if not provided

    # 🔍 Debug: Print what smart_shelf_id is received
    print(f"Fetching data for: {smart_shelf_id}")

    grouped_data = fetch_shelf_data(smart_shelf_id)  # 🔹 Now it takes a variable input

    if not grouped_data:
        return jsonify({"error": "No data found"}), 404

    response_data = {
        shelf_id: [
            {
                "smart_shelf_id": item.smart_shelf_id,
                "measure_name": item.measure_name,
                "measure_value": item.measure_value,
                "time": item.time,
                "name": item.name
            } for item in shelf_items
        ] for shelf_id, shelf_items in grouped_data.items()
    }

    return jsonify(response_data)

@app.route('/login/<username>', methods=['GET', 'POST'])
def login(username):
    
    formatted_username = username.replace("-", " ")

    # ✅ Fetch Smart Shelf Data from API instead of hardcoding
    total_shelves, smart_shelves = get_smart_shelves(username)
    
    formatted_username = username.replace("-", " ")

    if request.method == 'POST':
        smart_shelf_1_name = request.form.get('smart_shelf_1_name', '')
        smart_shelf_2_name = request.form.get('smart_shelf_2_name', '')
        smart_shelf_3_name = request.form.get('smart_shelf_3_name', '')
        weight_item_1 = request.form.get('weight_item_1', '')
        weight_item_2 = request.form.get('weight_item_2', '')
        weight_item_3 = request.form.get('weight_item_3', '')
        lower_limet_1 = request.form.get('lower_limet_1', '')
        lower_limet_2 = request.form.get('lower_limet_2', '')
        lower_limet_3 = request.form.get('lower_limet_3', '')

        # Topic for mqtt
        topic = request.form.get("selected_topic", "")

        message_payload = {
            "body": json.dumps({
                "topic": topic,
                "smart_shelf_1_name": smart_shelf_1_name,
                "smart_shelf_2_name": smart_shelf_2_name,
                "smart_shelf_3_name": smart_shelf_3_name,
                "weight_item_1": weight_item_1,
                "weight_item_2": weight_item_2,
                "weight_item_3": weight_item_3,
                "lower_limet_1": lower_limet_1,
                "lower_limet_2": lower_limet_2,
                "lower_limet_3": lower_limet_3,
            })
        }
        
        headers = {"x-api-key": API_KEY}
        
        response = requests.post(API_UPDATE_INFO_URL, headers=headers, json=message_payload)

        print("✅ UI Published Message to AWS IoT:", response)

        return render_template("login.html", username=formatted_username, smart_shelves=smart_shelves, success=True)

    return render_template("login.html", username=formatted_username, smart_shelves=smart_shelves, total_shelves=total_shelves)

if __name__ == '__main__':
    app.run(debug=True)
