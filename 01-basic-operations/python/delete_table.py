import boto3

client = boto3.client("dynamodb", region_name="us-east-1")

try:
    client.delete_table(
        TableName="Users",
    )
    print("Table deleted successfully! 🙌")
except Exception as err:
    print(f"Error deleting table: {err}")
