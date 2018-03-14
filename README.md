# A lambda function deployer

Deploying a lambda function is actually pretty simple: just look at the justfile.
Any related infrastructure should be created with infrastructure tooling (e.g. terraform).
Note that this does include support for setting up a cloudwatch cron.

Supports a multi-environment setup. The environment defaults to "dev".

# Dependencies

* [just](https://github.com/casey/just#installation), a command runner
* [aws cli](https://github.com/aws/aws-cli/releases)
* [jq](https://stedolan.github.io/jq/download/), a cli json parser
* bash


# Setup

This is tested to work with Python 3.6, but should work with any runtime. Just change the (runtime)
configuration variables at the top of the `justfile`.
Fill out [config/dev.json](./config/dev.json) with a `role` and a `function-name`. Create the IAM
role (see the Appendix section)

    just setup
    just schedule

Run the latter command if you want your lambda to be invoked by a cloudwatch cron.


# Workflow

Edit the code. Check changes with MyPy. You can test running the code with:

    just invoke test.json

Deploy:

    just deploy

For an environment other than dev set the `env` variable.

    just env=staging deploy

Per-environment configuration is in `config/*.json`

Destroy the lambda deployment:

    just unschedule  # If you created the scheduler
    just destroy



## Apendix: IAM Role

We manage the IAM role an associated infrastructure in terraform and recommend you do the same.
However, to test this out, you can create a role with this policy:

    {
      "Version": "2008-10-17",
      "Statement": [
        {
          "Action": "sts:AssumeRole",
          "Principal": {
            "Service": [
              "lambda.amazonaws.com"
            ]
          },
          "Effect": "Allow"
        }
      ]
    }

Attach the policy

    arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole
