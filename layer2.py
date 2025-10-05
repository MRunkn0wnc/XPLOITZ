import base64
import hashlib

class CustomCompressor:
    def __init__(self):
        self.substitution_table = self._generate_substitution_table()
    
    def _generate_substitution_table(self):
        table = {}
        seed = b'matryoshka_seed_2024'
        for i in range(256):
            key = hashlib.sha256(seed + bytes([i])).digest()
            table[bytes([i])] = key[:2]  # 2 bytes per input byte
        return table
    
    def compress(self, data):
        expanded = bytearray()
        for byte in data:
            expanded.extend(self.substitution_table[bytes([byte])])
        
        # Add simple markers
        result = bytearray()
        for i in range(0, len(expanded), 4):
            chunk = expanded[i:i+4]
            if len(chunk) == 4:
                result.append(0xFF)  # Marker
                result.extend(chunk)
            else:
                result.extend(chunk)
        
        custom_b85 = base64.b85encode(bytes(result))
        return b'L2' + custom_b85
    
    def decompress(self, compressed_data):
        if compressed_data[:2] != b'L2':
            raise ValueError("Invalid Layer 2 header")
        
        data = base64.b85decode(compressed_data[2:])
        
        # Remove markers
        cleaned = bytearray()
        i = 0
        while i < len(data):
            if data[i] == 0xFF:
                i += 1  # Skip marker
                if i + 3 < len(data):
                    cleaned.extend(data[i:i+4])
                    i += 4
            else:
                cleaned.append(data[i])
                i += 1
        
        # Reverse substitution
        reverse_table = {}
        seed = b'matryoshka_seed_2024'
        for i in range(256):
            key = hashlib.sha256(seed + bytes([i])).digest()[:2]
            reverse_table[key] = bytes([i])
        
        decoded = bytearray()
        for i in range(0, len(cleaned), 2):
            if i + 1 < len(cleaned):
                chunk = bytes(cleaned[i:i+2])
                if chunk in reverse_table:
                    decoded.extend(reverse_table[chunk])
        
        return bytes(decoded)

def layer2_encode(data):
    return CustomCompressor().compress(data)

def layer2_decode(encoded_data):
    return CustomCompressor().decompress(encoded_data)
