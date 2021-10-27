import boto3

client = boto3.client("dynamodb", region_name="us-east-1")

try:
    client.create_table(
        TableName="MovieRoles",
        AttributeDefinitions=[
            {"AttributeName": "Actor", "AttributeType": "S"},
            {"AttributeName": "Movie", "AttributeType": "S"},
            {"AttributeName": "Genre", "AttributeType": "S"},
            {"AttributeName": "Year", "AttributeType": "N"},
        ],
        KeySchema=[
            {"AttributeName": "Actor", "KeyType": "HASH"},
            {"AttributeName": "Movie", "KeyType": "RANGE"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "GenreYearIndex",
                "KeySchema": [
                    {"AttributeName": "Genre", "KeyType": "HASH"},
                    {"AttributeName": "Year", "KeyType": "RANGE"},
                ],
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                },
                "Projection": {"ProjectionType": "ALL"},
            }
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    print("Table created successfully! 🚀")
except Exception as err:
    print(f"Error creating table: {err}")
