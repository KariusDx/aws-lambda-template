from typing import Dict, Any, Callable

import logging
import traceback
import boto3

logger = logging.getLogger()
sqs_client = boto3.client('sqs')


# give a callback that return True on successful processing
def process_messages(
        queue_url: str,
        message_callback: Callable[[Dict[str, Any]], bool]) -> None:
    # Get messages from the queue
    logger.info("Trying to receive messages for queue {0}".format(queue_url))
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
    )
    messages = response.get('Messages', list())
    logger.info("Got {0} message(s)".format(len(messages)))

    # Try to process each message received regardless of failures
    for message in messages:
        try:
            body = message.get('Body')
            if body is None:
                raise Exception("Got a message with no body")

            if message_callback(body) is True:
                logger.info("Deleting message from queue")
                sqs_client.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message.get('ReceiptHandle'),
                )
            else:
                raise Exception("message callback did not return True")
        except Exception as e:
            traceback.print_exc()
            logger.error("Failed to process message. Continuing with remaining messages." + str(e))
            make_message_visible(queue_url, message)


# Set a message's VisibilityTimeout to 0 so it's available again to other consumers
def make_message_visible(queue_url: str, message: Dict[str, Any]) -> None:
    sqs_client.change_message_visibility(
        QueueUrl=queue_url,
        ReceiptHandle=message.get('ReceiptHandle'),
        VisibilityTimeout=0,
    )
