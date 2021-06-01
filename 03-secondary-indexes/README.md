# DynamoDB -- Handling additional access patterns with secondary indexes

In the previous lesson, you learned how to use DynamoDB as more than a key-value store by using the composite primary key and Query operation. We saw that the primary key structure is important as it drives access patterns for your items.

However, what if you need to allow multiple, different access pattern for a certain type of items? How can you enable these patterns with only a single primary key?

In this final lesson, we'll learn how to enable multiple access patterns on the same item using secondary indexes.

This lesson has four steps:

- [Creating a DynamoDB table with a secondary index](#creating-a-dynamodb-table-with-a-secondary-index);
- [Loading data into your table](#loading-data-into-your-table)
- [Using the Query operation on your secondary index](#using-the-query-operation-on-your-secondary-index);
- [Deleting your DynamoDB table](#deleting-your-dynamodb-table);

## Creating a DynamoDB table with a secondary index

In this lesson, we will start by creating a DynamoDB table. The table will be similar as the one in the last lesson with one difference -- we'll be adding a global secondary index.

> Note: there are two types of secondary indexes -- global and local. In almost all occasions, you'll want to use a global secondary index. For the rest of this lesson, I'll use "global secondary index" and "secondary index" interchangeably. For more on the types of indexes, check out [Local or Global: Choosing a secondary index type in DynamoDB](https://www.dynamodbguide.com/local-or-global-choosing-a-secondary-index-type-in-dynamo-db/).

A secondary index is something you create on your DynamoDB table that gives you additional access patterns on the items in your table. When you add a secondary index to your table, you will declare the primary key schema for the secondary index. When an item is written into your table, DynamoDB will check if the item has the attributes for your secondary index's primary key schema. If it does, the item will be copied into the secondary index with the primary key for the secondary index. You can then issue read requests against your secondary index to access items with secondary access patterns.

In essence, a secondary index gives you an additional, read-only view on your data.

There are a few main differences to note between your base table and your secondary indexes:

1. Unlike your base table, attributes for your secondary index key schema are not required on each item. If an item is written to your table but is missing one or both of the elements to your secondary index, it won't be written to your secondary index. This is often helpful in a pattern called a "sparse index".

2. Primary key values for your secondary index do not have to be unique. You can have multiple items with the same key schema values in your secondary index.

3. You cannot do writes to your secondary index -- only reads. All write operations need to go through your base table.

4. Data is asychronously replicated to your secondary indexes, so you could see slightly stale data in your secondary index.

Your DynamoDB table may have up to 20 global secondary indexes and up to 5 local secondary indexes. Global and local secondary indexes may be added when you create the table, and global secondary indexes may be added to your table after creation.

To add a secondary index, you need to specify:

- The index name;
- The key schema for your secondary index;
- The provisioned throughput (if your table is not using on-demand billing);
- The index projection (do you want the entire item copied over or a subset?)

Additionally, if you use attributes in your secondary index that are not already used in the primary key or another secondary index, you will need to specify them in `AttributeDefinitions` when creating your table.

For specifics on each of these properties, [check out the CreateTable docs](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_CreateTable.html#DDB-CreateTable-request-GlobalSecondaryIndexes).

### Task

In this lesson, we will continue with our movie roles example from the last lesson. Each item with represent a role played by an actor in a movie.

Recall that our primary key for the last lesson used a partition key of `Actor` and a sort key of `Movie`. This allowed us to fetch all movie roles for a particular Actor.

But what if we have additional access patterns? For example, we may want to get all the movie roles for a particular genre, or even the movies for a genre for a specific year or range of years.

We can handle these additional access patterns with a secondary index.

Write and execute a script that will create a `MovieRoles` table. You can build on the script you wrote in the last lesson. This script should include a global secondary index called `GenreYearIndex` whose key schema uses `Genre` for the partition key and `Year` for the sort key.

Try it on your own first, but if you want to see an example of this, look at [this file](./src/createTable.js).

## Loading data into your table

We're going to re-use the data from the last lesson, so use the same script to insert the `items.json` items into your table.

### Task

There is a file named `items.json` that includes four MovieRole items in DynamoDB's object format. Write a script that reads the items and inserts them into DynamoDB using the `BatchWriteItem` operation. Be sure to check for unprocessed items!

If you get stuck, [look here](./src/insertItems.js) for an example.

## Using the Query operation on your secondary index

Just like in the last lesson, we have an access pattern -- "Fetch all roles in a given genre" -- that is a "fetch many" access pattern. To handle this, we'll use the Query operation again. In this case, we'll be running the Query against our secondary index.

### Task

Use the Query operation on your secondary index to query for all roles for a given genre. The structure around `KeyConditionExpression` should be similar to the last one. The biggest difference here is that you'll need to pass an `IndexName` property into the Query operation to indicate you want to use the secondary index.

Use the genre of `Drama` to execute your queries. It should return two roles -- Tom Hanks in Cast Away and Natalie Portman in Black Swan.

If you get stuck, check [here](./src/queryRoles.js) for an example of using Query.

## Deleting your DynamoDB Table

We've completed the main steps for this lesson, so let's remove your DynamoDB table. You can use the `DeleteTable` operation to delete your table and avoid incurring charges in your AWS account.

### Task

Write a script to delete your `MovieRoles` table. See [here](./src/deleteTable.js) for an example.

## Conclusion

This completes the third lesson and the workshop. In this lesson, we learned about supporting additional access patterns in our data via secondary indexes. We learned some specifics about secondary indexes, including how to add them to our table. Finally, we used the Query operation against our secondary index.

This completes the DynamoDB workshop. At this point, you should be familiar with some of the core concepts around DynamoDB, including primary keys, expressions, and secondary indexes. You should also be familiar with some of the core operations against DynamoDB, such as GetItem, PutItem, and Query.

There's a lot more to learn about effective data modeling with DynamoDB, so don't stop learning here! :)
