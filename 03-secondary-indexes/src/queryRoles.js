const AWS = require("aws-sdk");
const DynamoDB = new AWS.DynamoDB({ region: "us-east-1" });

DynamoDB.query(
  {
    TableName: "MovieRoles",
    IndexName: "GenreYearIndex",
    KeyConditionExpression: "#genre= :genre",
    ExpressionAttributeNames: {
      "#genre": "Genre",
    },
    ExpressionAttributeValues: {
      ":genre": { S: "Drama" },
    },
  },
  function (err, data) {
    if (err) console.log(`Error performing query": ${err}`);
    else
      console.log(
        `Found ${data.Items.length} roles!\n${JSON.stringify(data.Items)}`
      );
  }
);
