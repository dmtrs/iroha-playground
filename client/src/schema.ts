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

export interface Account {
  readonly __typename?: 'Account';
  readonly uri: Scalars['ID'];
  readonly id: Scalars['String'];
  readonly domain: Domain;
}

export interface Asset {
  readonly __typename?: 'Asset';
  readonly uri: Scalars['ID'];
  readonly precision: Scalars['Int'];
  readonly id: Scalars['String'];
  readonly domain: Domain;
}

export interface Domain {
  readonly __typename?: 'Domain';
  readonly uri: Scalars['ID'];
}

export interface IAsset {
  readonly id: Scalars['String'];
  readonly domain: IDomain;
  readonly precision: Scalars['Int'];
}

export interface IDomain {
  readonly uri: Scalars['ID'];
}

export interface Mutation {
  readonly __typename?: 'Mutation';
  readonly createAsset: Transaction;
}


export interface MutationcreateAssetArgs {
  inputAsset: IAsset;
}

export interface Query {
  readonly __typename?: 'Query';
  readonly asset: Asset;
  readonly transaction: ReadonlyArray<Transaction>;
}


export interface QueryassetArgs {
  uri?: Scalars['ID'];
}


export interface QuerytransactionArgs {
  uris: ReadonlyArray<Scalars['ID']>;
}

export interface Transaction {
  readonly __typename?: 'Transaction';
  readonly uri: Scalars['ID'];
  readonly status: TransactionStatus;
  readonly commands: Scalars['String'];
  readonly creator: Account;
}

export const enum TransactionStatus {
  NONE = 'NONE',
  COMMITTED = 'COMMITTED',
  ENOUGH_SIGNATURES_COLLECTED = 'ENOUGH_SIGNATURES_COLLECTED',
  REJECTED = 'REJECTED',
  STATEFUL_VALIDATION_FAILED = 'STATEFUL_VALIDATION_FAILED',
  STATELESS_VALIDATION_FAILED = 'STATELESS_VALIDATION_FAILED'
};

export type AppQueryVariables = Exact<{ [key: string]: never; }>;


export type AppQueryData = (
  { readonly __typename?: 'Query' }
  & { readonly asset: (
    { readonly __typename?: 'Asset' }
    & Pick<Asset, 'id' | 'uri'>
  ) }
);
