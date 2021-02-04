# DynamoDB Workshop

This repository contains materials for a workshop to learn the basics about DynamoDB. It is focused on core concepts and API operations, but it doesn't dive deep into advanced data modeling concepts such as single-table design. If you want to know more about data modeling with DynamoDB, check out [The DynamoDB Book](https://www.dynamodbbook.com/) or some of the [DynamoDB content on my blog](https://www.alexdebrie.com/).

There are slides that go along with this workshop, but you can _probably_ get along without them. You might just have to Google a few concepts if you don't understand them.

This workshop is separated into three lessons with are to be completed in order:

1. **Basic Operations**

   In this lesson, you will learn some of the core vocabulary of DynamoDB, including primary keys, attributes, and provisioned throughput. Then, you will create your first DynamoDB table with a simple primary key. Finally, you will interact with the DynamoDB API by writing to and reading from your table. You'll see how to use condition expressions to avoid overwriting existing data.

   [Start Lesson 1 here](./01-basic-operations/README.md)

2. **Composite primary keys and the Query operation**

   In the second lesson, you'll learn how to use DynamoDB as more than a key-value store. You'll create a DynamoDB table with a composite primary key and use the Query operation to retrieve multiple items in a single request. This will lay the foundation for more advanced use cases in your applications.

   [Start Lesson 2 here](./02-query/README.md)

3. **Handling additional access patterns with secondary indexes**

   In the third and final lesson, you'll see how to handle multiple access pattern on the same items. You'll use secondary indexes to reshape your data and handle even more complex access patterns.

   [Start Lesson 3 here](./03-secondary-indexes/README.md)
