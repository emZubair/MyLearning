const globals = require("globals");
const stylistic = require("@stylistic/eslint-plugin");

module.exports = [
    {
        files: ["**/*.{js,jsx}"],
        languageOptions: {
            ecmaVersion: 2021,
            sourceType: "module",
            globals: {
                ...globals.browser
            }
        },
        plugins: {
            "@stylistic": stylistic
        },
        rules: {
            "no-array-constructor": 2,
            "no-caller": 2,
            "no-labels": 2,
            "no-eval": 2,
            "no-extend-native": 2,
            "no-extra-bind": 2,
            "no-implied-eval": 2,
            "no-iterator": 2,
            "no-label-var": 2,
            "no-lone-blocks": 2,
            "no-loop-func": 2,
            "no-multi-str": 2,
            "no-global-assign": 2,
            "no-new": 2,
            "no-new-func": 2,
            "no-object-constructor": 2,
            "no-new-wrappers": 2,
            "no-octal-escape": 2,
            "no-proto": 2,
            "no-return-assign": 2,
            "no-script-url": 2,
            "no-sequences": 2,
            "no-shadow": 2,
            "no-shadow-restricted-names": 2,
            "no-undef-init": 2,
            "no-use-before-define": 2,
            "no-with": 2,
            "consistent-return": 2,
            "curly": [2, "all"],
            "eqeqeq": 2,
            "new-cap": 2,
            "strict": [2, "function"],
            "yoda": [2, "never"],

            "@stylistic/no-multi-spaces": 2,
            "@stylistic/function-call-spacing": 2,
            "@stylistic/no-trailing-spaces": 2,
            "@stylistic/comma-spacing": 2,
            "@stylistic/eol-last": 2,
            "@stylistic/no-extra-parens": [2, "functions"],
            "@stylistic/key-spacing": [2, { "beforeColon": false, "afterColon": true }],
            "@stylistic/new-parens": 2,
            "@stylistic/semi-spacing": [2, { "before": false, "after": true }],
            "@stylistic/space-infix-ops": 2,
            "@stylistic/keyword-spacing": 2,
            "@stylistic/space-unary-ops": [2, { "words": true, "nonwords": false }]
        }
    }
];
