import json

import boto3

client = boto3.client("dynamodb", region_name="us-east-1")

try:
    response = client.query(
        TableName="MovieRoles",
        KeyConditionExpression="#actor = :actor",
        ExpressionAttributeNames={"#actor": "Actor"},
        ExpressionAttributeValues={":actor": {"S": "Tom Hanks"}},
    )
    print(
        f"Found {len(response['Items'])} roles!\n{json.dumps(response['Items'], indent=2)}"
    )
except Exception as err:
    print(f"Error fetching roles: {err}")
