To use cloudformation, specify the key "cloudformation" in config/env.json. e.g.


    "cloudformation": {
        "sqs-lambda-sns": {
          "QueueName": "Insert my queue name",
          "TopicName": "Insert my topic name",
          "PublisherSNSTopicARN": "Insert the publish topic arn"
        }
    }
