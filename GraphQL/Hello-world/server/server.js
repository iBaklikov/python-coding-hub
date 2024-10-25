import { ApolloServer } from '@apollo/server'
import { startStandaloneServer } from '@apollo/server/standalone'

const typeDefs = `#graphql
    schema {
        query: Query
    }
    type Query {
        greeting: String 
    }
`;

const resolvers = {
   Query: {
    greeting: () => 'Hello world',
   }, 
};

const server = new ApolloServer({ typeDefs: typeDefs, resolvers: resolvers });
const { url } = await startStandaloneServer(server, { listen: { port: 9001} } );
console.log(`Server running at ${url}`);