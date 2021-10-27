const AWS = require("aws-sdk");
const DynamoDB = new AWS.DynamoDB({ region: "us-east-1" });

DynamoDB.createTable(
  {
    TableName: "MovieRoles",
    AttributeDefinitions: [
      {
        AttributeName: "Actor",
        AttributeType: "S",
      },
      {
        AttributeName: "Movie",
        AttributeType: "S",
      },
    ],
    KeySchema: [
      { AttributeName: "Actor", KeyType: "HASH" },
      { AttributeName: "Movie", KeyType: "RANGE" },
    ],
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
