import struct
import zlib

def layer1_encode(data):
    # Calculate checksum on original data
    original_checksum = zlib.crc32(data)
    
    encoded = bytearray()
    fib = [1, 1]
    while len(fib) < 256:
        fib.append(fib[-1] + fib[-2])
    
    for i, byte in enumerate(data):
        fib_val = fib[i % len(fib)] % 256
        encoded.append(byte ^ fib_val)
    
    rotated = bytearray()
    for i, byte in enumerate(encoded):
        shift = (i % 7) + 1
        rotated.append(((byte << shift) | (byte >> (8 - shift))) & 0xFF)
    
    header = b'L1' + struct.pack('<I', len(data)) + struct.pack('<I', original_checksum)
    return header + bytes(rotated)

def layer1_decode(encoded_data):
    if encoded_data[:2] != b'L1':
        raise ValueError(f"Invalid Layer 1 header. Got: {encoded_data[:10]}")
    
    data_len = struct.unpack('<I', encoded_data[2:6])[0]
    expected_checksum = struct.unpack('<I', encoded_data[6:10])[0]
    rotated = encoded_data[10:]
    
    # Reverse bit rotation
    encoded = bytearray()
    for i, byte in enumerate(rotated):
        shift = (i % 7) + 1
        encoded.append(((byte >> shift) | (byte << (8 - shift))) & 0xFF)
    
    # Reverse Fibonacci XOR
    fib = [1, 1]
    while len(fib) < 256:
        fib.append(fib[-1] + fib[-2])
    
    decoded = bytearray()
    for i, byte in enumerate(encoded):
        if i >= data_len: 
            break
        fib_val = fib[i % len(fib)] % 256
        decoded.append(byte ^ fib_val)
    
    # Verify checksum
    actual_checksum = zlib.crc32(decoded)
    if actual_checksum != expected_checksum:
        raise ValueError(f"Layer 1 checksum mismatch. Expected: {expected_checksum:08x}, Got: {actual_checksum:08x}")
    
    return bytes(decoded)
