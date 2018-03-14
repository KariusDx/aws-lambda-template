# vim: set ft=make :

handler = 'handler.handler'
runtime = 'python3.6'
timeout = '30'
memory = '128'

env = 'dev'

help:
	@echo "just is a convenient command runner. Try just -l"


compress:
	zip -r function.zip handler.* lib/ vendor/ 1>/dev/null


configure:
	#!/bin/bash
	set -euo pipefail
	config="$(cat config/{{env}}.json)"
	function_name="$(echo "$config" | jq -r '."function-name"')"

	aws lambda update-function-configuration \
		--function-name "$function_name" \
		--environment "$(echo "$config" | jq -c '{"Variables": .environment}')" \
		--vpc-config "$(echo "$config" | jq -c '."vpc-config"')"

deploy: compress configure
	#!/bin/bash
	set -euo pipefail
	config="$(cat config/{{env}}.json)"
	function_name="$(echo "$config" | jq -r '."function-name"')"

	aws lambda update-function-code \
		--function-name "$function_name" \
		--zip-file fileb://function.zip

	# Publishing a new Version of the Lambda function
	new_version=`aws lambda publish-version --function-name "$function_name" | jq -r .Version`

	# Updating the Lambda Alias so it points to the new function
	aws lambda update-alias --function-name "$function_name" --function-version "$new_version" --name DEPLOYED


invoke file qualifier='$LATEST':
	#!/bin/bash
	set -euo pipefail
	config="$(cat config/{{env}}.json)"

	function_name="$(echo "$config" | jq -r '."function-name"')"
	aws lambda invoke \
		--function-name "$function_name" \
		--invocation-type RequestResponse \
		--log-type Tail \
		--payload "$(cat {{file}})" --qualifier '{{qualifier}}' \
		lambda-invoke-output.txt | jq -r .LogResult | base64 -d
	cat lambda-invoke-output.txt


setup: compress
	#!/bin/bash
	set -euo pipefail
	if ! test -f config/{{env}}.json ; then
	  echo "expected config file: config/{{env}}.json"
	  exit 1
	fi

	config="$(cat config/{{env}}.json)"
	function_name="$(echo "$config" | jq -r '."function-name"')"

	role="$(echo "$config" | jq -r '."role"')"
	# Create the versioned function
	aws lambda create-function --handler {{handler}} \
		--function-name "$function_name" \
		--zip-file fileb://function.zip \
		--runtime {{runtime}} --timeout {{timeout}} --memory-size {{memory}} --role "$role" \
		--environment "$(echo "$config" | jq -c '{"Variables": .environment}')" \
		--vpc-config "$(echo "$config" | jq -c '."vpc-config"')"
	aws lambda create-alias --name DEPLOYED \
		--function-name "$function_name" \
		--function-version '$LATEST'


destroy:
	#!/bin/bash
	set -euo pipefail
	config="$(cat config/{{env}}.json)"
	function_name="$(echo "$config" | jq -r '."function-name"')"

	aws lambda delete-function \
		--function-name "$function_name" \


schedule_expression = 'rate(5 minutes)'

# Schedule the lambda
# Add this to your setup task
schedule:
	#!/bin/bash
	set -euo pipefail
	config="$(cat config/{{env}}.json)"
	function_name="$(echo "$config" | jq -r '."function-name"')"
	schedule="${function_name}-schedule"

	# Schedule it
	rule=$(aws events put-rule \
		--name "$schedule" \
		--schedule-expression '{{schedule_expression}}' )
	aws lambda add-permission \
		--function-name "$function_name" \
		--statement-id "$schedule" \
		--action 'lambda:InvokeFunction' \
		--principal 'events.amazonaws.com' \
		--source-arn "$(echo "$rule" | jq -r .RuleArn)"
	function=$(aws lambda get-function --function-name "$function_name")
	aws events put-targets --rule "$function_name-schedule" \
	  --targets "Id"="1","Arn"="$(echo "$function" | jq .Configuration.FunctionArn)"


# Remove scheduling
# Add this to your destroy task
unschedule:
	#!/bin/bash
	set -euo pipefail
	config="$(cat config/{{env}}.json)"
	function_name="$(echo "$config" | jq -r '."function-name"')"
	schedule="${function_name}-schedule"

	aws lambda remove-permission \
		--function-name "$function_name" \
		--statement-id "$schedule" \
		|| echo "could not remove permission"
	aws events remove-targets --rule "$schedule" --ids 1 \
		|| echo "could not remove targets"
	aws events delete-rule \
		--name "$schedule" \
		|| echo "could not delete rule"
