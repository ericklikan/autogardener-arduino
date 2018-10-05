import base64
import hashlib
import json

from cryptography.fernet import Fernet


# Not actually secure, just not storing stuff as plaintext
def store(key: str, value):
    try:
        with open('config.json', 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = {}

    f = Fernet(generate_key())

    try:
        token = f.encrypt(value.encode())
    except AttributeError:
        token = f.encrypt(bytes([value]))

    data[key] = base64.b64encode(token).decode()

    with open('config.json', 'w') as f:
        f.write(json.dumps(data))


def retrieve(key: str):
    try:
        with open('config.json', 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return False

    token = base64.b64decode(data[key])
    f = Fernet(generate_key())

    return f.decrypt(token)


def generate_key():
    with open("/etc/machine-id", "r") as f:
        machine_id = f.read().strip()

    hashed = hashlib.sha256(machine_id.encode())

    return base64.urlsafe_b64encode(hashed.digest())
