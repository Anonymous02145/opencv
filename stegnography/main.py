from encryption_class import HybridCryptography
from decryption_class import HybridDecryptor

if __name__ == '__main__':
    encryptor = HybridCryptography()

    public_key, private_key = encryptor.get_key()
    print(f"public key: {public_key} || private_key: {private_key}")
    message = b"Confidential message of nsa, fbi, cia is stored somewhere"

    encrypted = encryptor.encrypt_data(message)
    print(encrypted)

    while True:
        ask = input("do you want to decrypt the data(y/n) : ")
        if ask == 'y' or ask == 'yes':
            decryptor = HybridDecryptor(private_key)
            decrypted = decryptor.decrypt(encrypted)
            print("Decrypted : ", decrypted.decode())
        if ask == 'n' or ask == 'no':
            break

    # print("Decrypted : ", decrypted.decode())