const AWS = require("aws-sdk");
const DynamoDB = new AWS.DynamoDB({ region: "us-east-1" });

DynamoDB.getItem(
  {
    TableName: "MovieRoles",
    Key: { Actor: { S: "Tom Hanks" }, Movie: { S: "Cast Away" } },
  },
  function (err, data) {
    if (err) console.log(`Error fetching role": ${err}`);
    else if (!data.Item) console.log("Role does not exist");
    else console.log(`Found role: ${JSON.stringify(data.Item, null, 2)}`);
  }
);
