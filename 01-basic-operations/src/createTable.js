const AWS = require("aws-sdk");
const DynamoDB = new AWS.DynamoDB({ region: "us-east-1" });

DynamoDB.createTable(
  {
    TableName: "Users",
    AttributeDefinitions: [
      {
        AttributeName: "Username",
        AttributeType: "S",
      },
    ],
    KeySchema: [{ AttributeName: "Username", KeyType: "HASH" }],
    ProvisionedThroughput: {
      ReadCapacityUnits: 5,
      WriteCapacityUnits: 5,
    },
  },
  function (err) {
    if (err) console.log(`Error creating table: ${err}`);
    else console.log("Table created succesfully! 🚀");
  }
);
