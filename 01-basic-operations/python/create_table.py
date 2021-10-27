import boto3

client = boto3.client("dynamodb", region_name="us-east-1")

try:
    client.create_table(
        TableName="Users",
        AttributeDefinitions=[{"AttributeName": "Username", "AttributeType": "S"}],
        KeySchema=[{"AttributeName": "Username", "KeyType": "HASH"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    print("Table created successfully! 🚀")
except Exception as err:
    print(f"Error creating table: {err}")
