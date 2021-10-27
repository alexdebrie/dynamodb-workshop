import json

import boto3

client = boto3.client("dynamodb", region_name="us-east-1")

try:
    response = client.get_item(TableName="Users", Key={"Username": {"S": "alexdebrie"}})
    if response["Item"]:
        print(f"Found user: {json.dumps(response['Item'], indent=2)}")
    else:
        print("User does not exist!")
except Exception as err:
    print(f"Error fetching user: {err}")
