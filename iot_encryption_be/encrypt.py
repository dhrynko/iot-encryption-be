import scrypt
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Cipher import DES
from Cryptodome.Random import get_random_bytes


def encrypt_aes_256(message, key):
    salt = get_random_bytes(AES.block_size)
    private_key = scrypt.hash(key.encode(), salt=salt, N=2 ** 14, r=8, p=1, buflen=32)
    cipher_config = AES.new(private_key, AES.MODE_GCM)
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(message, 'utf-8'))
    return {
        'cypher': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }


def decrypt_aes_256(enc_dict, password):
    salt = b64decode(enc_dict['salt'])
    cipher_text = b64decode(enc_dict['cypher'])
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])
    private_key = scrypt.hash(password.encode(), salt=salt, N=2 ** 14, r=8, p=1, buflen=32)
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)
    return decrypted


def encrypt_des(message, key):
    if len(key) != 8:
        raise Exception
    else:
        while len(message) % 8 != 0:
            message += ' '
        cipher = DES.new(key, DES.MODE_ECB)
        encrypted = cipher.encrypt(bytes(message, 'utf-8'))
        return encrypted


def decrypt_des(encrypted, password):
    if len(password) != 8:
        raise Exception
    else:
        cipher = DES.new(password, DES.MODE_ECB)
        decrypted = cipher.decrypt(encrypted)
        return decrypted


# def main():
#     password = "stas"
#     encrypted = encrypt_aes_256("Sample string", password)
#     print(encrypted)
#     decrypted = decrypt_aes_256(encrypted, password)
#     print(bytes.decode(decrypted))
#
#     password = "12345678"
#     password2 = bytes(password, 'utf-8')
#     encrypted = encrypt_des("Sample string 2", password2)
#     print(encrypted)
#     decrypted = decrypt_des(encrypted, password2)
#     print(bytes.decode(decrypted))
#
#
# main()
