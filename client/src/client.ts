import type { NormalizedCacheObject } from '@apollo/client/core';

import { ApolloClient, InMemoryCache, HttpLink, from } from '@apollo/client/core';
import { onError } from "@apollo/client/link/error";

import { locationVar } from './router';

const uri =
  'http://localhost:8000/graphql';

export const link = new HttpLink({ uri });


const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors)
    graphQLErrors.forEach(({ message, locations, path }) =>
      console.log(
        `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`,
      ),
    );

  if (networkError) console.log(`[Network error]: ${networkError}`);
});

const cache =
  new InMemoryCache({
    typePolicies: {
      Query: {
        /**
        fields: {
          location(): Location {
            return locationVar();
          },
        },
        **/
      },
    }
  });

export const client =
  new ApolloClient({
    link: from([ errorLink, link ]),
    cache,
  });

declare global {
  interface Window {
    __APOLLO_CLIENT__?: ApolloClient<NormalizedCacheObject>;
  }
}
