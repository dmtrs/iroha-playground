import { ApolloQuery, customElement, html, TemplateResult } from '@apollo-elements/lit-apollo';

import type {
  AppQueryData as Data,
  AppQueryVariables as Variables,
} from './schema';

import AppQuery from './App.query.graphql';
import style from './app.css';

import { Domain } from 'elements';

@customElement('apollo-app')
export class ApolloApp extends ApolloQuery<Data, Variables> {
  static readonly is = 'apollo-app';

  static readonly style = [style];

  query = AppQuery;


  render(): TemplateResult {
    return html`
      ${Domain({ uri:this.data?.asset?.uri ?? '/' })}
    `;
  }
}
