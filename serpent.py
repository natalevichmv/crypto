from __future__ import barry_as_FLUFL

import random

from CryptoPlus.Cipher.blockcipher import *
from CryptoPlus.Cipher.pyserpent import Serpent
 
 
def get_block_size():
    return 16
 
 
class SerpentCBC(BlockCipher):
    def __init__(self, key, IV):
        if len(key) not in (16, 24, 32):
            raise ValueError("Key should be 128, 192 or 256 bits")
        self.blocksize = get_block_size()
        BlockCipher.__init__(self, key, MODE_CBC, IV, None, Serpent, None)
 
 
def create_IV():
    return bytes(random.randrange(256) for i in range(get_block_size()))
 
 
def create_key(l):
    if l not in (16, 24, 32):
        raise ValueError("Key should be 128, 192 or 256 bits")
    return bytes(random.randrange(256) for i in range(l)) + create_IV()
 
 
def encrypt(key, data):
    if isinstance(data, str):
        data = data.encode()
    data = data + bytes(1 for x in range(32))
    IV = key[-16:]
    key = key[:-16]
    bs = get_block_size()
    padding = (bs - len(data) % bs) % bs
    data = data + bytes(0 for x in range(padding))
    return SerpentCBC(key, IV).encrypt(data)
 
 
def decrypt(key, data):
    if isinstance(data, str):
        data = data.encode()
    IV = key[-16:]
    key = key[:-16]
    res = SerpentCBC(key, IV).decrypt(data)
    res = bytearray(res)
    while res and not res[-1]:
        res.pop()
    assert res[-32:] == bytes(1 for x in range(32))
    return bytes(res[:-32]).decode()