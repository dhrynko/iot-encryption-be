import boto3
import uuid
from dynamodb_json import json_util
from .config import config

dynamo_db = boto3.client('dynamodb')


def scan_table(table):
    items = dynamo_db.scan(TableName=table)["Items"]

    return json_util.loads(items)


def get_message(message_id):
    message = dynamo_db.get_item(
        TableName=config.messages_table,
        Key={"uid": {"S": message_id}})["Item"]

    return json_util.loads(message)


def get_encrypted_message(cypher_id):
    message = dynamo_db.get_item(
        TableName=config.encrypted_messages_table,
        Key={"uid": {"S": cypher_id}})["Item"]

    return json_util.loads(message)


def put_message(message):
    dynamo_db.put_item(
        TableName=config.messages_table,
        Item={"message": {"S": message}, "uid": {"S": str(uuid.uuid4())}}
    )

    return


def put_encrypted_message(cypher):
    if not isinstance(cypher, str):
        dynamo_db.put_item(
            TableName=config.encrypted_messages_table,
            Item={"cypher": {"S": cypher.get("cypher")},
                  "salt": {"S": cypher.get("salt")},
                  "nonce": {"S": cypher.get("nonce")},
                  "tag": {"S": cypher.get("tag")},
                  "uid": {"S": str(uuid.uuid4())}}
        )
    else:
        dynamo_db.put_item(
            TableName=config.encrypted_messages_table,
            Item={"message": {"S": cypher}, "uid": {"S": str(uuid.uuid4())}}
        )

    return
