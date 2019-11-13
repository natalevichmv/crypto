from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random
 
 
def generate(l):
    random_generator = Random.new().read
    key = RSA.generate(l, random_generator)
    pub, priv = key.publickey().exportKey(), key.exportKey()
    return (pub, priv)
 
 
def encrypt(key, data):
    key = RSA.importKey(key)
    return PKCS1_OAEP.new(key).encrypt(data)
 
 
def decrypt(key, data):
    key = RSA.importKey(key)
    return PKCS1_OAEP.new(key).decrypt(data)