// module.exports = {
//     "env": {
//         "browser": true,
//         "es6": true
//     },
//     "extends": [
//         "eslint:recommended",
//         "plugin:vue/essential"
//     ],
//     "globals": {
//         "Atomics": "readonly",
//         "SharedArrayBuffer": "readonly"
//     },
//     "parserOptions": {
//         "ecmaVersion": 2018,
//         "sourceType": "module"
//     },
//     "plugins": [
//         "vue"
//     ],
//     "rules": {
//     }
// };


module.exports = {
    root: true,
    env: {
      node: true
    },
    'extends': [
      'plugin:vue/vue3-essential',
      'eslint:recommended'
    ],
    parserOptions: {
      parser: 'babel-eslint'
    },
    rules: {
      // 'no-console': process.env.NODE_ENV === 'development' ? 'error' : 'off',
      'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
     
    }
  }
  
  