import json

import boto3

client = boto3.client("dynamodb", region_name="us-east-1")

try:
    response = client.query(
        TableName="MovieRoles",
        IndexName="GenreYearIndex",
        KeyConditionExpression="#genre= :genre",
        ExpressionAttributeNames={"#genre": "Genre"},
        ExpressionAttributeValues={":genre": {"S": "Drama"}},
    )
    print(
        f"Found {len(response['Items'])} roles!\n{json.dumps(response['Items'], indent=2)}"
    )
except Exception as err:
    print(f"Error fetching roles: {err}")
