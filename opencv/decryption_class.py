"""
    this is for the decryption

"""

from Crypto.Cipher import AES
from cryptography.hazmat.primitives import  hashes
from cryptography.hazmat.primitives.asymmetric import padding

class HybridDecryptor:
    def __init__(self, privatekey):
        self.privatekey = privatekey

    def decrypt(self, encrypted_data: bytes):
        aes_key = self.privatekey.decrypt(
            encrypted_data['encrypted_key'],
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=encrypted_data['nonce'])
        decrypted = cipher.decrypt_and_verify(encrypted_data['ciphertext'], encrypted_data['tag'])
        return decrypted