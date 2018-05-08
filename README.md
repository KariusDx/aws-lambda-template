# AWS Lambda Template

This repo contains AWS lambda functions that work SQS queues.

## Organization

Most code changes are for these directories
* function/ the lambda functions live here
* library/ code shared between functions
* cfn/ cloudformation templates

Additional directories
* template/ new functions symlink to template files
* vendor/ installed packages shared between functions

## Creating a new function

    just new-function FUNCTION_NAME
    cd function/FUNCTION_NAME
    cat README.md

## Updating all functions after library changes

    just run-all deploy

## Running tests & MyPy

This just type-checks and lints, there are no unit tests yet.

    just test-all

## Installing Python dependencies

For shared dependencies

    pip3 install requests -t vendor

If a dependency is not shared, install it to a vendor directory in your function:

    cd function/my-function
    rm vendor
    mkdir vendor
    pip3 install the-package-i-need -t vendor
