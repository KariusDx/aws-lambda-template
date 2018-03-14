from typing import NamedTuple, Dict, Any, Optional

import json


Message = Dict[str, Any]


class S3TestEvent(str):
    pass


class S3Location(NamedTuple):
    bucket: str
    key: str


# None indicates a test event
# Throws exceptions if it cannot validate the message
def parse_s3_notification(body: str) -> Optional[S3Location]:
    # Ultimately need message.body.Message.Records.[0].s3.object.key - This will contain a
    # path to the file written, such as 170130_NB501185_0200_AHC53KBGX2/RunParameters.xml
    parsed_message_body = json.loads(body)
    parsed_message = json.loads(parsed_message_body.get('Message'))

    records = parsed_message.get('Records')
    if records is None:
        if parsed_message.get('Event') == "s3:TestEvent":
            return None
        else:
            raise Exception("Found no records and not a test event")

    if len(records) != 1:
        raise Exception("Found more than one record in message which should not happen!")

    s3_bucket = records[0].get('s3').get('bucket').get('name')
    filename = records[0].get('s3').get('object').get('key')
    return S3Location(bucket=s3_bucket, key=filename)
