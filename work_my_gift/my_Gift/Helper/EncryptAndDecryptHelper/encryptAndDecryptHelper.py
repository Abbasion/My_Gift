import base64
import datetime

from cryptography.fernet import Fernet

from my_Gift.settings import Fernet_key


def load_key():
    """
    Load the previously generated key
    """
    return Fernet_key



def encrypt(data):

    key = load_key()
    fernet = Fernet( key)

    encMessage = fernet.encrypt(data.encode())
    return encMessage

def decrypt(data):
    """
    Decrypts an encrypted message
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(data)

    return (decrypted_message.decode())