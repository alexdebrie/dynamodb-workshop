import json
import os

import boto3

client = boto3.client("dynamodb", region_name="us-east-1")

lesson_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
items_path = os.path.join(lesson_directory, "items.json")

with open(items_path, "r") as f:
    roles = json.load(f)

requests = [{"PutRequest": {"Item": role}} for role in roles]

try:
    response = client.batch_write_item(RequestItems={"MovieRoles": requests})
    if response["UnprocessedItems"].get("MovieRoles"):
        print(
            f"Unprocessed items. Run again. {json.dumps(response['UnprocessedItems']['MovieRoles'])}"
        )
    else:
        print("Movie role items created successfully!")
except Exception as err:
    raise err
    print(f"Error creating items: {err}")
