import { esbuildPlugin } from '@web/dev-server-esbuild';
import { fromRollup } from '@web/dev-server-rollup';

import _graphql from '@apollo-elements/rollup-plugin-graphql';
import _commonjs from '@rollup/plugin-commonjs';
import _replace from '@rollup/plugin-replace';
import _litcss from 'rollup-plugin-lit-css';

const commonjs = fromRollup(_commonjs);
const litcss = fromRollup(_litcss);
const graphql = fromRollup(_graphql);
const replace = fromRollup(_replace);

export default {
  nodeResolve: true,
  port: 8004,
  appIndex: 'index.html',
  rootDir: '.',
  mimeTypes: {
    'src/**/*.graphql': 'js',
    'src/components/**/*.css': 'js',
    'src/style.css': 'css',
  },
  plugins: [
    esbuildPlugin({ ts: true }),
    commonjs(),
    graphql({ include: '**/*.graphql' }),
    litcss({
      include: 'src/components/**/*.css',
      exclude: 'src/style.css',
    }),
    replace({
      // setting "include" is important for performance
      'process.env.NODE_ENV': '"development"',
    }),
  ],
};
