# DynamoDB -- Basic Operations

In this first lesson, you will learn the basics of writing to and reading from DynamoDB. This lesson has five steps:

- [Creating a DynamoDB table](#creating-a-dynamodb-table);
- [Loading data using the PutItem operation](#loading-data-using-the-putitem-operation);
- [Reading data using the GetItem operation](#reading-data-using-the-getitem-operation);
- [Preventing overwrites with Condition Expressions](#preventing-overwrites-with-condition-expressions);
- [Deleting your DynamoDB table](#deleting-your-dynamodb-table);

## Creating a DynamoDB table

First, we'll need to create a DynamoDB table. When creating a DynamoDB table, you need to specify the following properties at a minimum:

1. **Table name:** Give your table a name that will be unique within an AWS region.

2. **Primary key:**

   DynamoDB is a schemaless database. Unlike relational databases, this means you don't need to specify the names and types of all attribute that your items will have. Instead, you will manage your schema within your application code.

   However, you do need to define a _primary key_ for your table. Every item in your table must have the primary key for the table, and each item in your table is uniquely identifiable by the primary key.

   There are two types of primary keys:

   - **Simple:** A primary key that consists of a single element (the _partition_ key).

   - **Composite:** A primary key that consists of two elements (a _partition_ key and a _sort_ key).

   To define your table, you must provide two properties:

   - **KeySchema:** This defines the elements of your primary key. It must include a partition (also called a "HASH" key) and may include a sort key (also called a "RANGE" key).

   - **AttributeDefinitions:** For each element in your primary key, you must declare the attribute name and type in the `AttributeDefinitions` property.

3. **Throughput settings:**

   With traditional databases, you often spin up servers. You might specify CPU, RAM, and networking settings for your instance. You need to estimate your traffic and make guesses as to how that translates to computing resources.

   With DynamoDB, it's different. You pay for throughput directly rather than computing resources. This is split into Read Capacity Units (RCUs), which refers to a strongly-consistent read of 4KB of data, and Write Capacity Units (WCUs), which refers to a write of 1KB of data.

   There are two throughput modes you can use with DynamoDB:

   - **Provisioned throughput:** You specify the number of RCUs and WCUs you want available on a per-second basis;

   - **On demand:** You are charged on a per-request basis for each read and write you make. You don't need to specify the amount you want ahead of time.

   On a fully-utilized basis, on-demand billing is more expensive that provisioned throughput. However, it's difficult to get full utilization or anything close to it, particularly if your traffic patterns vary over the time of day or day of week. Many people actually save money with on demand, while also reducing the amount of capacity planning and adjustments you need to do.

### Task

For this part of the workshop, you want to create a DynamoDB table with a simple primary key. This table will store users in your application. Name your table "Users" and give it a primary key with the hash key of "Username".

For the throughput settings, choose to use provisioned throughput with `ReadCapacityUnits` and `WriteCapacityUnits` of `5`. This will fit within the AWS Free Tier and will be more than enough for this demo.

Try it on your own first, but if you want to see an example of this, look at the following files:

- [Node.js](./node/createTable.js).
- [Python](./python/create_table.py).

## Loading data using the PutItem operation

Now that you have your DynamoDB table, let's write some data into it. To write data into DynamoDB, you can use the [PutItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html) operation.

As you insert items into DynamoDB, keep two things in mind:

1. **Primary key requirement:**

   Remember that every item in your DynamoDB table must include your primary key. When you are creating your item in the `PutItem` operation, make sure you have all elements of the primary key included.

2. **DynamoDB object format:**

   Each attribute on a DynamoDB item has a type. This can be simple types, such as strings or numbers, or they can be complex types like arrays, maps, and sets.

   When writing an item to DynamoDB, you need to include the type for each attribute.

   For example, when writing an attribute of "Username" with a type of `string`, your attribute might look as follows:

   ```js
   "Username": { "S": "alexdebrie" },
   ```

   We've used the `"S"` to indicate it's of type `string`.

   If you make a complex object, you need to note the type of the complex attribute as well as the elements within the attribute.

   In the [users.json](./users.json) file in this directory, you can see examples of items. Look at the `Interests` property to see an example of a `list` attribute and the `Address` property to see a `map` attribute.

### Task

There is a file named `users.json` that includes three Users in DynamoDB's object format. Write a script that reads the three Users from the file and inserts them into the table using the `PutItem` operation. Because they are already in the DynamoDB object format, you don't need to add the attribute type information yourself.

If you get stuck, look at the following files for examples:

- [Node.js](./node/insertUsers.js).
- [Python](./python/insert_users.py).

## Reading data using the GetItem operation

By this point, you have data in your DynamoDB table. But data isn't put in your database to sit there -- you want to read it back out to use it! Let's do that here.

To do so, we'll use the [GetItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html) operation in DynamoDB. The `GetItem` operation reads an individual item from DynamoDB.

### Task

Write a script that reads one of your three items from your DynamoDB table. To do so, you must provide the primary key of your item. Recall that the primary key uniquely identifies each item in your table. Further, you must specify the type of your primary key attribute(s).

The usernames of the three items are `alexdebrie`, `the_serena`, and `bigtimebrad`.

If you're having trouble, look at the following files for an example:

- [Node.js](./node/getUser.js).
- [Python](./python/get_user.py).

## Preventing overwrites with Condition Expressions

We've done the basics of both writing to and reading from DynamoDB. We're going to cover one last point before moving on.

Previously, we used the `PutItem` operation to write to DynamoDB. This will write the item to DynamoDB and _completely overwrite_ any existing item that had the same primary key.

At times, this may not be desirable. You may want to prevent overwriting an item if it already exists. To do so, you can use DynamoDB Condition Expressions.

DynamoDB Condition Expressions allow you to specify conditions on write-based operations. These conditions must evaluate to True or the write will be aborted.

The nuances of Condition Expressions are deep, but we won't go too far in this workshop. See this post on [using DynamoDB Condition Expressions](https://www.alexdebrie.com/posts/dynamodb-condition-expressions/) for more information.

### Task

Update your script from the Loading Data step to add a `ConditionExpression` on your `PutItem` request. The Condition Expression should assert that there is not an existing item with the same primary key.

Hint: you should use the [`attribute_not_exists()`](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.OperatorsAndFunctions.html#Expressions.OperatorsAndFunctions.Functions) function.

Check the following files for an example of using the `ConditionExpression`.

- [Node.js](./node/insertUsersConditional.js).
- [Python](./python/insert_users_conditional.py).

## Deleting your DynamoDB Table

We've completed the main steps for this lesson, so let's remove your DynamoDB table. You can use the `DeleteTable` operation to delete your table and avoid incurring charges in your AWS account.

### Task

Write a script to delete your `Users` table. See the following files for an example:

- [Node.js](./node/deleteTable.js).
- [Python](./python/delete_table.py).

## Conclusion

That completes this first lesson! You learned how to use DynamoDB in a key-value store with a simple primary key. You loaded data with the `PutItem` operation and read it back with the `GetItem` operation. Then you saw how to prevent accidental overwrites of your data using Condition Expressions.

In the [next lesson](../02-query/README.md), you will learn how to use a table with a composite primary key to handle more complex access patterns.
