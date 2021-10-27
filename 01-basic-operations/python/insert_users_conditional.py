import json
import os

import boto3

client = boto3.client("dynamodb", region_name="us-east-1")

lesson_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
users_path = os.path.join(lesson_directory, "users.json")

with open(users_path, "r") as f:
    users = json.load(f)

for user in users:
    try:
        client.put_item(
            TableName="Users",
            Item=user,
            ConditionExpression="attribute_not_exists(Username)",
        )
        print(f"User {user['Username']['S']} created successfully!")
    except Exception as err:
        print(f"Error creating user {user['Username']['S']}: {err}")
