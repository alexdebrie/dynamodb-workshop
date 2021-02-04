const AWS = require("aws-sdk");
const DynamoDB = new AWS.DynamoDB({ region: "us-east-1" });

DynamoDB.getItem(
  {
    TableName: "Users",
    Key: { Username: { S: "alexdebrie" } },
  },
  function (err, data) {
    if (err) console.log(`Error fetching user": ${err}`);
    else if (!data.Item) console.log("User does not exist");
    else console.log(`Found user: ${JSON.stringify(data.Item, null, 2)}`);
  }
);
