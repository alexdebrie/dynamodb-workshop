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
      {
        AttributeName: "Genre",
        AttributeType: "S",
      },
      {
        AttributeName: "Year",
        AttributeType: "N",
      },
    ],
    KeySchema: [
      { AttributeName: "Actor", KeyType: "HASH" },
      { AttributeName: "Movie", KeyType: "RANGE" },
    ],
    GlobalSecondaryIndexes: [
      {
        IndexName: "GenreYearIndex",
        KeySchema: [
          { AttributeName: "Genre", KeyType: "HASH" },
          { AttributeName: "Year", KeyType: "RANGE" },
        ],
        ProvisionedThroughput: {
          ReadCapacityUnits: 5,
          WriteCapacityUnits: 5,
        },
        Projection: {
          ProjectionType: "ALL",
        },
      },
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
