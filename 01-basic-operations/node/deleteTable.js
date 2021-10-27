const AWS = require("aws-sdk");
const DynamoDB = new AWS.DynamoDB({ region: "us-east-1" });

DynamoDB.deleteTable(
  {
    TableName: "Users",
  },
  function (err) {
    if (err) console.log(`Error deleting table: ${err}`);
    else console.log("Table deleted successfully! 🙌");
  }
);
