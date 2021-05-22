from base64 import b64decode, b64encode

from Crypto.Cipher import PKCS1_v1_5 as PKCS1Cipher
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as PKCS1Signature


def rsa_encrypt(message: str, public_key: str, bits: int = 2048) -> str:
    """
    Encrypt message with given bits and key.

    :param message: Message
    :param public_key: Key string with PEM structure
    :param bits: Bits for RSA algorithm
    :returns: Encrypted message
    """
    key = RSA.importKey(public_key)
    key = PKCS1Cipher.new(key)
    encrypted = key.encrypt(str.encode(message))
    return b64encode(encrypted).decode()


def rsa_decrypt(message: str, private_key: str, bits: int = 2048):
    """
    Decrypt message with given bits and key.

    :param message: Encrypted message with base64 format
    :param private_key: Key string with PEM structure
    :param bits: Bits for RSA algorithm
    :returns: Decrypted message
    """
    key = RSA.importKey(private_key)
    key = PKCS1Cipher.new(key)
    decrypted = key.decrypt(b64decode(str.encode(message)))
    return decrypted.decode()


def generate_signature(message: str, private_key: str) -> str:
    """
    Generate signature of the message by given private key.

    :param message: Message to verify
    :param private_key: Key to sign
    :return: Signature
    """
    key = RSA.importKey(private_key)
    signer = PKCS1Signature.new(key)
    message = str.encode(message)
    hash = SHA256.new(message)

    return b64encode(signer.sign(hash)).decode()


def verify_signature(message: str, signature: str, public_key: str) -> str:
    """
    Verify signature of the message by given private key.

    :param message: Message to verify
    :param private_key: Key to sign
    :return: Signature
    """
    key = RSA.importKey(public_key)
    verifier = PKCS1Signature.new(key)
    message, signature = str.encode(message), b64decode(str.encode(signature))
    hash = SHA256.new(message)

    return verifier.verify(hash, signature)
