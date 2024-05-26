/* eslint-env node */
require('@rushstack/eslint-patch/modern-module-resolution')

module.exports = {
  root: true,
  extends: [
    'plugin:vue/vue3-essential',
    // 'plugin:@typescript-eslint/recommended',
    'eslint:recommended',
    // 'plugin:vue/vue3-recommended',
    'plugin:prettier/recommended',
    '@vue/eslint-config-typescript',
    '@vue/eslint-config-prettier',
    'prettier'
  ],
  plugins: ['prettier'],
  parserOptions: {
    ecmaVersion: 'latest'
  },
  rules: {
    'no-console': 'off',
    'import/prefer-default-export': 'off',
    'no-restricted-syntax': 'off',
    'vue/html-indent': 'off',
    'vue/max-attributes-per-line': [
      'error',
      {
        singleline: 5, // 한 줄에 최대 5개의 속성을 허용
        multiline: 2
      }
    ],
    'prettier/prettier': 'off',
    'import/no-cycle': 'off',
    '@typescript-eslint/no-unused-vars': [
      'error',
      {
        argsIgnorePattern: '_'
      }
    ],
    '@typescript-eslint/explicit-function-return-type': [
      'error',
      {
        allowExpressions: true,
        allowTypedFunctionExpressions: true,
        allowHigherOrderFunctions: true,
        allowDirectConstAssertionInArrowFunctions: true,
        allowConciseArrowFunctionExpressionsStartingWithVoid: false
      }
    ],
    'max-len': [
      'error',
      {
        code: 180,
        ignoreStrings: true,
        ignorePattern: 'class="[^"]*"'
      }
    ],
    'sort-imports': [
      'error',
      {
        ignoreCase: true,
        ignoreDeclarationSort: false,
        ignoreMemberSort: false,
        memberSyntaxSortOrder: ['none', 'all', 'multiple', 'single'],
        allowSeparatedGroups: true
      }
    ],
    'vue/first-attribute-linebreak': 'off'
  }
}
