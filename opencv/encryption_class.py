"""
    for higher leve; of security i have used aes encryption.
    Rsa for encrypting the aes decryption key.
    note: i havent added more functionality like encrypting a pdf or a huge doc.

"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


class HybridCryptography:
    def __init__(self):
        self.privatekey = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.publickey = self.privatekey.public_key()

    def get_key(self):
        return self.publickey, self.privatekey

    def genaeskey(self):
        return get_random_bytes(32) # 256 bit key

    def encrypt_data(self, data: bytes):

        aes_key = self.genaeskey()

        cipher = AES.new(aes_key, AES.MODE_GCM) # gcm mode secure than most others
        cipher_text, tag = cipher.encrypt_and_digest(data)

        encrypted_aes = self.publickey.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return {
            'encrypted_key' : encrypted_aes,
            'ciphertext' : cipher_text,
            'nonce' : cipher.nonce,
            'tag' : tag
        }

