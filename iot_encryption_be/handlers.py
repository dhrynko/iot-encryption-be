import json
from .config import config
from .services import scan_table, put_message, put_encrypted_message, get_message, get_encrypted_message
from .encrypt import encrypt_aes_256, encrypt_des, decrypt_aes_256, decrypt_des


def get_all_messages(event, context):
    messages = scan_table(config.messages_table)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Methods": "GET, OPTIONS"
        },
        "body": json.dumps(messages),
    }


def get_all_encrypted_messages(event, context):
    messages = scan_table(config.encrypted_messages_table)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Methods": "GET, OPTIONS"
        },
        "body": json.dumps(messages),
    }


def add_message(event, context):
    message = json.loads(event["body"])["message"]
    put_message(message)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Methods": "POST, OPTIONS"
        },
        "body": "Successful put",
    }


def encrypt_message_from_db(event, context):
    payload = json.loads(event["body"])

    message_id = event["pathParameters"]["id"]
    encryption = payload["encryption_algorithm"]
    key = payload["encryption_key"]

    message = get_message(message_id)["message"]

    encryption_strategies = {
        "AES-256": encrypt_aes_256,
        "DES": encrypt_des
    }

    encryption_handler = encryption_strategies.get(encryption)
    cypher = encryption_handler(message, key)

    put_encrypted_message(cypher)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Methods": "POST, OPTIONS"
        },
        "body": json.dumps(cypher),
    }


def encrypt_message_from_ui(event, context):
    payload = json.loads(event["body"])

    encryption = payload["encryption_algorithm"]
    key = payload["encryption_key"]
    message = payload["message"]

    put_message(message)

    encryption_strategies = {
        "AES-256": encrypt_aes_256,
        "DES": encrypt_des
    }

    encryption_handler = encryption_strategies.get(encryption)
    cypher = encryption_handler(message, key)

    put_encrypted_message(cypher)

    res_string = cypher.get("cypher", cypher)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Methods": "POST, OPTIONS"
        },
        "body": res_string,
    }


def decrypt_message_from_db(event, context):
    payload = json.loads(event["body"])

    message_id = event["pathParameters"]["id"]
    encryption = payload["encryption_algorithm"]
    key = payload["encryption_key"]

    message = get_encrypted_message(message_id)

    decryption_strategies = {
        "AES-256": decrypt_aes_256,
        "DES": decrypt_des
    }

    encryption_handler = decryption_strategies.get(encryption)
    encrypted = encryption_handler(message, key)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Methods": "POST, OPTIONS"
        },
        "body": encrypted,
    }
