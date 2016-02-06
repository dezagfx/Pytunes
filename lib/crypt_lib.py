from Crypto.Cipher import AES
from config import config

key = config.encryption.key
cipher = AES.new(key)

def pad(s):
    return s + ((16-len(s) % 16) * '{')

def encrypt(texto):
    global cipher
    return cipher.encrypt(pad(texto))

def decrypt(textocifrado):
    global cipher
    dec = cipher.decrypt(textocifrado).decode('utf-8')
    l = dec.count('{')
    return dec[:len(dec)-1]
    