import hashlib
import struct

class XorCipher:
    def __init__(self, key_seed=b"matryoshka_final_key"):
        self.key_seed = key_seed
    
    def _derive_key(self, data_length):
        key = hashlib.sha256(self.key_seed + struct.pack('<I', data_length)).digest()
        return key
    
    def encrypt(self, data):
        key = self._derive_key(len(data))
        encrypted = bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
        return b'L3' + encrypted
    
    def decrypt(self, encrypted_data):
        if encrypted_data[:2] != b'L3':
            raise ValueError("Invalid Layer 3 header")
        encrypted = encrypted_data[2:]
        # Try different length assumptions
        for assumed_len in [len(encrypted), len(encrypted) - 1, len(encrypted) + 1]:
            try:
                key = self._derive_key(assumed_len)
                decrypted = bytes([encrypted[i] ^ key[i % len(key)] for i in range(len(encrypted))])
                # Try to decode as UTF-8 to verify
                decrypted.decode('utf-8')
                return decrypted
            except:
                continue
        raise ValueError("Layer 3 decryption failed")

def layer3_encode(data):
    return XorCipher().encrypt(data)

def layer3_decode(encoded_data):
    return XorCipher().decrypt(encoded_data)
