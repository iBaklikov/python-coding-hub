// Importing the ApolloServer class from the @apollo/server package. 
// This class helps create a GraphQL server.
import { ApolloServer } from '@apollo/server';

// Importing the startStandaloneServer function from the @apollo/server/standalone package. 
// This function makes it easy to start a simple standalone GraphQL server.
import { startStandaloneServer } from '@apollo/server/standalone';

// Define the GraphQL schema using SDL (Schema Definition Language). 
// The 'schema' section defines the entry point (root query type). 
// The 'Query' type contains one field 'greeting' which returns a String.
const typeDefs = `#graphql
    schema {
        query: Query
    }
    type Query {
        greeting: String 
    }
`;

// Define the resolver functions for the GraphQL queries. 
// The 'greeting' resolver is responsible for returning the string 'Hello world' 
// when the 'greeting' field is queried.
const resolvers = {
   Query: {
    // The 'greeting' field resolver, which returns a static string.
    greeting: () => 'Hello world',
   }, 
};

// Create an instance of ApolloServer with the provided type definitions (schema) 
// and resolvers (the logic to resolve queries).
const server = new ApolloServer({ typeDefs: typeDefs, resolvers: resolvers });

// Start the server using the 'startStandaloneServer' function. 
// This function listens on port 9001 and returns an object containing the server URL.
// The 'await' keyword is used because starting the server is an asynchronous operation.
const { url } = await startStandaloneServer(server, { listen: { port: 9001} });

// Log the server's running URL to the console. 
// This allows you to know where your GraphQL server is accessible.
console.log(`Server running at ${url}`);
