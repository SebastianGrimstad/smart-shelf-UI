import boto3
import json
import time

# AWS IoT Region
AWS_REGION = "eu-west-1"

# AWS IAM Credentials (Replace with your IAM user credentials)
AWS_ACCESS_KEY = "AKIAXZ5NGBYJ3NT6BHOR"
AWS_SECRET_KEY = "9TPCTIMV8RXI0+hcFw3NtZ9hSXEcXUVSBRbvoTRK"

# Define the topic
MQTT_TOPIC = "smart_shelf_demo/sub"

# Define the message
message_payload = json.dumps({"message": "Hello from UI 2"})

# Initialize AWS IoT Data Client
client = boto3.client(
    "iot-data",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Publish Message
response = client.publish(
    topic=MQTT_TOPIC,
    qos=1,
    payload=message_payload
)

print("✅ UI Published Message to AWS IoT:", response)
