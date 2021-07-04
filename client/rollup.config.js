import alias from '@rollup/plugin-alias';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import html from '@open-wc/rollup-plugin-html';
import graphql from '@apollo-elements/rollup-plugin-graphql';
import litcss from 'rollup-plugin-lit-css';
import esbuild from 'rollup-plugin-esbuild';
import injectProcessEnv from 'rollup-plugin-inject-process-env';

export default {
  input: 'index.html',

  output: {
    dir: 'build',
    format: 'es',
    sourcemap: true,
  },

  plugins: [
    alias({
      entries: [
        { find: 'elements', replacement: 'src/elements/index.js' },
      ],
    }),
    resolve(),
    esbuild({ ts: true, target: 'es2019', minify: true }),
    html(),
    commonjs(),
    graphql(),
    litcss(),
    injectProcessEnv({
      NODE_ENV: 'production',
    }),
  ],
};
