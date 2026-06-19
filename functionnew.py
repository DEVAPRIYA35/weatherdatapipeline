import json
import urllib.request
import boto3
from datetime import datetime

# OpenWeather API Key
API_KEY = "97544bf7022d557dfc136ea1b896b9a8"

# DynamoDB Connection
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('openweather1')

# Cities List
cities = ["Kochi", "Mumbai", "Delhi", "Bangalore", "Chennai"]

def lambda_handler(event, context):

    result = []

    for city in cities:

        # OpenWeather API URL
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"

        try:
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())

            # Store data in DynamoDB
            item = {
                "city": city,
                "openweather_id": str(data["id"]),
                "temperature": str(data["main"]["temp"]),
                "humidity": str(data["main"]["humidity"]),
                "weather": data["weather"][0]["description"],
                "country": data["sys"]["country"],
                "time": datetime.utcnow().isoformat()
            }

            # Insert item into DynamoDB
            table.put_item(Item=item)

            result.append(item)

        except Exception as e:

            result.append({
                "city": city,
                "error": str(e)
            })

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }