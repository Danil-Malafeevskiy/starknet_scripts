from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from getpass import getpass

key = urlsafe_b64encode(getpass("Введите пароль для шифрации 32х символов: ").encode())

with open("data/private_key.txt", 'r') as file:
    priv_keys = [line.rstrip() for line in file]

new_keys = []

for priv_key in priv_keys:
    new_keys.append(Fernet(key).encrypt(priv_key.encode()).decode())

with open("data/private_key_shiphr.txt", 'w') as file:
    file.write("\n".join(new_keys))

print("Приватники зашифрованы и записаны в файл: private_key_shiphr.txt")