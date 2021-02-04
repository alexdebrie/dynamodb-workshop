const AWS = require("aws-sdk");
const DynamoDB = new AWS.DynamoDB({ region: "us-east-1" });

const fs = require("fs");
const path = require("path");

const data = fs.readFileSync(path.join(__dirname, "../users.json"));
const users = JSON.parse(data);

users.forEach((user) => {
  DynamoDB.putItem(
    {
      TableName: "Users",
      Item: user,
      ConditionExpression: "attribute_not_exists(Username)",
    },
    function (err) {
      if (err) console.log(`Error creating user ${user.Username.S}: ${err}`);
      else console.log(`User ${user.Username.S} created successfully!`);
    }
  );
});
