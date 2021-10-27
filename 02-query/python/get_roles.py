import json

import boto3

client = boto3.client("dynamodb", region_name="us-east-1")

try:
    response = client.batch_get_item(
        RequestItems={
            "MovieRoles": {
                "Keys": [
                    {"Actor": {"S": "Tom Hanks"}, "Movie": {"S": "Cast Away"}},
                    {"Actor": {"S": "Tom Hanks"}, "Movie": {"S": "Toy Story"}},
                    {"Actor": {"S": "Tim Allen"}, "Movie": {"S": "Toy Story"}},
                    {
                        "Actor": {"S": "Natalie Portman"},
                        "Movie": {"S": "Black Swan"},
                    },
                ]
            }
        }
    )
    if not response["Responses"]:
        print("Roles do not exist")
    else:
        print(f"Found roles: {json.dumps(response['Responses'], indent=2)}")
except Exception as err:
    print(f"Error fetching roles: {err}")
