import json
from .services import scan_messages_table, put_message, put_encrypted_message, get_message, get_encrypted_message
from .encrypt import encrypt_aes_256, encrypt_des, decrypt_aes_256, decrypt_des


def get_all_messages(event, context):
    messages = scan_messages_table()

    return {
        "statusCode": 200,
        "body": json.dumps(messages),
    }


def add_message(event, context):
    message = json.loads(event["body"])["message"]
    put_message(message)

    return {
        "statusCode": 200,
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
        "body": json.dumps(cypher),
    }


def decrypt_message_from_db(event, context):
    payload = json.loads(event["body"])

    message_id = event["pathParameters"]["id"]
    encryption = payload["encryption_algorithm"]
    key = payload["encryption_key"]

    message = get_encrypted_message(message_id)

    print(message)

    decryption_strategies = {
        "AES-256": decrypt_aes_256,
        "DES": decrypt_des
    }

    encryption_handler = decryption_strategies.get(encryption)
    encrypted = encryption_handler(message, key)

    return {
        "statusCode": 200,
        "body": encrypted,
    }
