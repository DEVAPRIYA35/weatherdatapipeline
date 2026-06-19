import json
import boto3

s3 = boto3.client('s3')

BUCKET_NAME = "openweatherbucket-250847880906-us-east-1-an"

def lambda_handler(event, context):

    cleaned_items = []

    for record in event['Records']:

        if record['eventName'] != 'INSERT':
            continue

        item = record['dynamodb']['NewImage']

        data = {}

        for key, value in item.items():

            # Convert DynamoDB format
            if 'S' in value:
                data[key] = value['S']
            elif 'N' in value:
                data[key] = value['N']

        # Remove null/empty values
        data = {
            k:v for k,v in data.items()
            if v not in ["", None, "null"]
        }

        # Remove unwanted fields
        data.pop("debug", None)
        data.pop("tempField", None)

        cleaned_items.append(data)

    if cleaned_items:

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f"weather/{event['Records'][0]['eventID']}.json",
            Body=json.dumps(cleaned_items)
        )

    return {
        "statusCode": 200
    }