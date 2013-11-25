__author__ = 'Chilaxus'
from Crypto.Cipher import AES
import string
import base64
import time
#import modules
PADDING = '{'
BLOCK_SIZE = 32
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
#prepare crypto method
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
#set encryption/decryption variables
private_key = "1234567890123456"

def encryt(data):
    cipher = AES.new(private_key)
    # encode a string
    encoded = EncodeAES(cipher, data)
    return encoded

def decrypt(encoded):
    cipher = AES.new(private_key)
    decoded = DecodeAES(cipher, encoded)
    return decoded


msg = 'this is the msg'
print msg
print decrypt(encryt(msg))