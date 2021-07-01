export type Maybe<T> = T | null;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
/** All built-in and custom scalars, mapped to their actual values */
export interface Scalars {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
}

export interface Location {
  readonly __typename?: 'Location';
  readonly pathname?: Maybe<Scalars['String']>;
  readonly search?: Maybe<Scalars['String']>;
  readonly origin?: Maybe<Scalars['String']>;
  readonly hash?: Maybe<Scalars['String']>;
  readonly host?: Maybe<Scalars['String']>;
  readonly hostname?: Maybe<Scalars['String']>;
  readonly href?: Maybe<Scalars['String']>;
  readonly port?: Maybe<Scalars['Int']>;
  readonly protocol?: Maybe<Scalars['String']>;
}

export interface Query {
  readonly __typename?: 'Query';
  readonly location?: Maybe<Location>;
}

export type AppQueryVariables = Exact<{ [key: string]: never; }>;


export type AppQueryData = (
  { readonly __typename?: 'Query' }
  & { readonly location?: Maybe<(
    { readonly __typename?: 'Location' }
    & Pick<Location, 'pathname'>
  )> }
);
