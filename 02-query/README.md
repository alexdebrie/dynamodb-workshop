# DynamoDB -- Composite Primary key + the Query operation

In the previous lesson, you learned the basics of DynamoDB, including terminology and the basic read and write operations.

In this second lesson, we'll learn some more advanced access patterns. We'll see how to use a table with a composite primary key. Then, we'll see a few different ways to work with multiple items in a single request. In particular, we'll see the power of the Query operation, which is foundational for advanced DynamoDB work.

This lesson has five steps:

- [Creating a DynamoDB table with a composite primary key](#creating-a-dynamodb-table-with-a-composite-primary-key);
- [Loading data into your table](#loading-data-into-your-table)
- [Reading multiple items using the BatchGetItem operation](#reading-multiple-items-using-the-batchgetitem-operation);
- [Reading multiple items with the Query operation](#reading-multiple-items-with-the-query-operation);
- [Deleting your DynamoDB table](#deleting-your-dynamodb-table);

## Creating a DynamoDB table with a composite primary key

Like in the last lesson, we'll start with creating a DynamoDB table. However, this lesson uses a composite primary key, not a simple primary key.

Much of the table creation should be the same, with two differences:

1. Your `KeySchema` property will include both a `HASH` key and a `RANGE` key;

2. The `AttributeDefinitions` property should include both attributes from the key schema.

### Task

In this lesson, we will store data about movie roles. Each item will represent a role played by an actor in a movie.

To begin, create a DynamoDB table with a composite primary key. Name your table `MovieRoles`, and give it a composite primary key with a partition (or hash) key of `Actor` and a sort (or range) key of `Movie`.

Like last time, choose to use provisioned throughput with `ReadCapacityUnits` and `WriteCapacityUnits` of `5`. This will fit within the AWS Free Tier and will be more than enough for this demo.

Try it on your own first, but if you want to see an example of this, look at the following files:

- [Node.js](./node/createTable.js).
- [Python](./python/create_table.py).

## Loading data into your table

Now that you have your DynamoDB table, let's write some data into it.

In the last lesson, you loaded data by calling the `PutItem` operation multiple times. If you want a faster way to load multiple items, you can use the [BatchWriteItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchWriteItem.html) operation. This allows you to combine up to 25 `PutItem` requests into a single request to DynamoDB.

When using the `BatchWriteItem` operation, your writes can succeed and fail independently. After you receive a response, check the `UnprocessedItems` object in the response body. If there are items in this object, they were not processed successfully and need to be retried.

### Task

There is a file named `items.json` that includes four MovieRole items in DynamoDB's object format. Write a script that reads the items and inserts them into DynamoDB using the `BatchWriteItem` operation. Be sure to check for unprocessed items!

If you get stuck, look to the following files for an example:

- [Node.js](./node/insertItems.js).
- [Python](./python/insert_items.py).

## Reading multiple items using the BatchGetItem operation

In the previous lesson, you read individual items from your table using the `GetItem` operation and including the `Username` attribute for the key. You can still use the `GetItem` operation on a table that has a composite primary key. However, you must provide _both_ elements of your primary key to read an individual item.

Additionally, you may have situations where you want to retrieve multiple items at the same time. If you know the full primary key for each item you want to retrieve, you can use the `BatchGetItem` operation to retrieve multiple items in a single request. With the `BatchGetItem` operation, you can retrieve up to 100 items in a single request.

### Task

Write a script that uses `BatchGetItem` to read your items from your DynamoDB table. This is similar to the `GetItem` request you made in the last lesson, but it requires specifying both elements of the primary key for each item you want to retrieve.

The four items in your table have the following primary key values:

1. Actor: Tom Hanks; Movie: Cast Away
2. Actor: Tom Hanks; Movie: Toy Story
3. Actor: Tim Allen; Movie: Toy Story
4. Actor: Natalie Portman; Movie: Black Swan

If you're having trouble, look at the following files for an example:

- [Node.js](./node/getRoles.js).
- [Python](./python/get_roles.py).

## Reading multiple items with the Query operation

So far, we've read specific, individual items from a table. But reading individual items is limiting in your application. Often, you'll want to read multiple, _related_ items in a single request. For example, you might want to satisfy the following access patterns:

- _Give me all the Users that belong to Organization ABC_

- _Retrieve all the Pull Requests in this GitHub repository_

- _Show me all the readings for this IoT device_

In these cases, you may not know the full primary key. To handle this, you can use the [Query](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Query.html) operation to efficiently retrieve multiple items.

The Query operation can be used on a table with a composite primary key, and it can return as many items as match the request (up to 1MB of data). If your Query would match more than 1MB of data, you can make a paginated request to continue your Query where it left off.

To use the Query operation, you need to include a _Key Condition Expression_ in your request. A Key Condition Expression describes the items you want to match in your Query.

When writing a Key Condition Expression, you **must** include an exact match on the partition key. You _may_ include conditions on the sort key as well.

Imagine you had a DynamoDB table that stored temperature readings for an IoT device. You have a composite primary key where the partition key is `DeviceId` and the sort key is `Timestamp`.

If you wanted to fetch all readings for Device `1234` that occurred _after_ January 1, 2021, you could use the following parameters:

```
KeyConditionExpression="#deviceId = :deviceId AND #timestamp > :timestamp",
ExpressionAttributeNames={
    "#deviceId": "DeviceId",
    "#timestamp": "Timestamp"
},
ExpressionAttributeValues={
    ":deviceId": { "N": "1234" },
    ":timestamp": { "S": "2021-01-01" }
}
```

There's a lot going on here, so let's walk through it.

Let's start with `ExpressionAttributeNames` and `ExpressionAttributeValues`. Whenever you're writing an expression in DynamoDB (including Key Condition Expressions, Update Expressions, Condition Expressions, and more), you can use these parameters. They act as variables that will be substituted into your expressions.

`ExpressionAttributeNames` _may be_ used whenever you are referring to the name of an attribute in your expression. Here, we are using `DeviceId` and `Timestamp`, which are the partition key and sort key names, respectively. You don't have to use `ExpressionAttributeNames` in your expressions unless the attribute name is a reserved word. There are a [ton of reserved words in DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ReservedWords.html), including `Timestamp`, which we're using here. I generally recommend using `ExpressionAttributeNames` just to avoid consulting the documentation on reserved words. In your expressions, attribute names that are specified in `ExpressionAttributeNames` must start with a `#`.

`ExpressionAttributeValues` _must be_ used whenever you are referring to the value of an attribute. This is because each attribute in DynamoDB is typed, and you must refer to the table when comparing or setting the value. Given that, it's cleaner to pull the values out into the `ExpressionAttributeValues` property. In your expressions, attribute values specified in `ExpressionAttributeValues` must start with a `:`.

With that background, look at the `KeyCondiionExpression`. Using substitution from the `ExpressionAttributeNames` and `ExpressionAttributeValues`, you can think of the key condition expression as containing two statements:

1. The `DeviceId` property must be `1234`; and
2. The `Timestamp` property must be greater than `2021-01-01`.

This matches our requirements on key condition expressions -- exact match on the partition key, and optional conditions on the sort key.

### Task

Let's see a Query in action. There are two movies -- `Cast Away` and `Toy Story` -- where Tom Hanks played a role. Write a Query to find all of Tom Hanks' movies.

Hint: you don't need to use a sort key condition here -- just the partition key match. If you want to get fancy, try adding a sort key condition to fetch all of Tom Hanks' movies whose titles are before `Forrest Gump` in the alphabet.

If you get stuck, check below for examples of using the Query operation:

- [Node.js](./node/queryRoles.js).
- [Python](./python/query_roles.py).

## Deleting your DynamoDB Table

We've completed the main steps for this lesson, so let's remove your DynamoDB table. You can use the `DeleteTable` operation to delete your table and avoid incurring charges in your AWS account.

### Task

Write a script to delete your `MovieRoles` table. See below for examples.

- [Node.js](./node/deleteTable.js).
- [Python](./python/delete_table.py).

## Conclusion

That completes this second lesson! You saw how to create a DynamoDB table with a composite primary key. You then quickly loaded data with the `BatchWriteItem` operation and read multiple items back with the `BatchGetItem` operation. Finally, you saw the power of a composite primary key when you used the `Query` operation to find multiple items with the same primary key.

In the [next lesson](../03-secondary-indexes/README.md), you will learn how to enable multiple access patterns on the same item using secondary indexes.
