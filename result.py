#!/usr/bin/env python3
"""
The Matryoshka Conspiracy - Robust Solver
"""

import os
import struct
import zlib
import base64
import hashlib

def extract_payload_simple(pdf_path):
    """Simple and robust PDF payload extraction"""
    with open(pdf_path, 'rb') as f:
        data = f.read()
    
    print("🔍 Simple PDF Analysis:")
    print(f"File size: {len(data)} bytes")
    
    # Find all streams
    streams = []
    pos = 0
    while True:
        stream_start = data.find(b'stream\n', pos)
        if stream_start == -1:
            break
        stream_start += 7
        stream_end = data.find(b'\nendstream', stream_start)
        if stream_end != -1:
            stream_data = data[stream_start:stream_end]
            streams.append(stream_data)
            pos = stream_end + 1
        else:
            break
    
    print(f"Found {len(streams)} streams")
    
    # Look for streams with L1 header or large size
    for i, stream in enumerate(streams):
        print(f"Stream {i}: {len(stream)} bytes")
        if stream.startswith(b'L1'):
            print(f"✅ Found L1 header in stream {i}")
            return stream
        if len(stream) > 100:  # Large stream likely contains payload
            print(f"📊 Large stream {i}: {len(stream)} bytes")
            # Check if it contains L1 somewhere
            l1_pos = stream.find(b'L1')
            if l1_pos != -1:
                print(f"✅ Found L1 at position {l1_pos} in stream {i}")
                return stream[l1_pos:]
    
    # If no L1 found, return the largest stream
    if streams:
        largest = max(streams, key=len)
        print(f"⚠️  No L1 header found. Using largest stream: {len(largest)} bytes")
        return largest
    
    raise ValueError("No suitable stream found in PDF")

def layer1_decode(encoded_data):
    """Decode Layer 1: Fibonacci XOR + Bit Rotation"""
    print(f"\n📍 Layer 1 Decoding:")
    print(f"Input size: {len(encoded_data)} bytes")
    
    # Find L1 header if not at start
    if not encoded_data.startswith(b'L1'):
        l1_pos = encoded_data.find(b'L1')
        if l1_pos != -1:
            print(f"L1 header found at position {l1_pos}")
            encoded_data = encoded_data[l1_pos:]
        else:
            print(f"First 50 bytes (hex): {' '.join(f'{b:02x}' for b in encoded_data[:50])}")
            raise ValueError("L1 header not found")
    
    if len(encoded_data) < 10:
        raise ValueError(f"Data too short: {len(encoded_data)} bytes")
    
    try:
        data_len = struct.unpack('<I', encoded_data[2:6])[0]
        expected_checksum = struct.unpack('<I', encoded_data[6:10])[0]
        rotated = encoded_data[10:]
    except Exception as e:
        raise ValueError(f"Header parsing failed: {e}")
    
    print(f"Data length: {data_len}, Expected checksum: {expected_checksum:08x}")
    
    # Reverse bit rotation
    encoded = bytearray()
    for i, byte in enumerate(rotated):
        shift = (i % 7) + 1
        encoded.append(((byte >> shift) | (byte << (8 - shift))) & 0xFF)
    
    # Generate Fibonacci sequence
    fib = [1, 1]
    while len(fib) < 256:
        fib.append(fib[-1] + fib[-2])
    
    # Reverse Fibonacci XOR
    decoded = bytearray()
    for i, byte in enumerate(encoded):
        if i >= data_len: 
            break
        fib_val = fib[i % len(fib)] % 256
        decoded.append(byte ^ fib_val)
    
    # Verify checksum
    actual_checksum = zlib.crc32(decoded)
    if actual_checksum != expected_checksum:
        raise ValueError(f"Checksum mismatch. Expected: {expected_checksum:08x}, Got: {actual_checksum:08x}")
    
    print(f"✅ Layer 1 decoded: {len(decoded)} bytes")
    return bytes(decoded)

def layer2_decode(compressed_data):
    """Decode Layer 2: Custom Compression"""
    print(f"\n📍 Layer 2 Decoding:")
    print(f"Input size: {len(compressed_data)} bytes")
    
    if not compressed_data.startswith(b'L2'):
        raise ValueError(f"Invalid Layer 2 header: {compressed_data[:10]}")
    
    try:
        # Decode Base85
        data = base64.b85decode(compressed_data[2:])
        print(f"Base85 decoded: {len(data)} bytes")
    except Exception as e:
        raise ValueError(f"Base85 decode failed: {e}")
    
    # Remove 0xFF markers
    cleaned = bytearray()
    i = 0
    while i < len(data):
        if data[i] == 0xFF:
            i += 1  # Skip marker
            if i + 3 < len(data):
                cleaned.extend(data[i:i+4])
                i += 4
            else:
                break
        else:
            cleaned.append(data[i])
            i += 1
    
    print(f"After marker removal: {len(cleaned)} bytes")
    
    # Reverse byte substitution
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
    
    print(f"✅ Layer 2 decoded: {len(decoded)} bytes")
    return bytes(decoded)

def layer3_decode(encrypted_data):
    """Decode Layer 3: XOR Cipher"""
    print(f"\n📍 Layer 3 Decoding:")
    print(f"Input size: {len(encrypted_data)} bytes")
    
    if not encrypted_data.startswith(b'L3'):
        raise ValueError(f"Invalid Layer 3 header: {encrypted_data[:10]}")
    
    encrypted = encrypted_data[2:]
    key_seed = b"matryoshka_final_key"
    
    print("Trying different length assumptions...")
    
    for assumed_len in [len(encrypted), len(encrypted) - 1, len(encrypted) + 1, len(encrypted) // 2]:
        try:
            key = hashlib.sha256(key_seed + struct.pack('<I', assumed_len)).digest()
            decrypted = bytes([encrypted[i] ^ key[i % len(key)] for i in range(len(encrypted))])
            
            # Check if result contains flag pattern
            if b'XPL_01TZ_CTF' in decrypted:
                print(f"✅ Success with assumed_len={assumed_len}")
                return decrypted
            
            # Try UTF-8 decode as secondary check
            decrypted.decode('utf-8')
            print(f"✅ Valid UTF-8 with assumed_len={assumed_len}")
            return decrypted
            
        except Exception:
            continue
    
    raise ValueError("Layer 3 decryption failed")

def brute_force_layer3(encrypted_data):
    """Brute force approach for Layer 3"""
    print("🔓 Attempting brute force on Layer 3...")
    
    encrypted = encrypted_data[2:] if encrypted_data.startswith(b'L3') else encrypted_data
    
    # Try common keys and patterns
    for key_byte in range(256):
        try:
            decrypted = bytes([b ^ key_byte for b in encrypted])
            if b'XPL_01TZ_CTF' in decrypted:
                print(f"✅ Brute force success with key 0x{key_byte:02x}")
                return decrypted
        except:
            pass
    
    # Try XOR with simple key derivation
    for key_seed in [b"matryoshka_final_key", b"oracle_secret", b"secret"]:
        for assumed_len in range(1, 1000, 10):
            try:
                key = hashlib.sha256(key_seed + struct.pack('<I', assumed_len)).digest()
                decrypted = bytes([encrypted[i] ^ key[i % len(key)] for i in range(len(encrypted))])
                if b'XPL_01TZ_CTF' in decrypted:
                    print(f"✅ Success with key_seed={key_seed}, assumed_len={assumed_len}")
                    return decrypted
            except:
                pass
    
    return None

def solve_matryoshka(pdf_path):
    """Main solver function"""
    print("🔍 The Matryoshka Conspiracy - Solver")
    print("=" * 50)
    
    try:
        # Step 1: Extract payload
        print("\n📍 Step 1: PDF Payload Extraction")
        layer1_data = extract_payload_simple(pdf_path)
        
        # Step 2: Decode Layer 1
        print("\n📍 Step 2: Layer 1 - Fibonacci XOR + Bit Rotation")
        layer2_data = layer1_decode(layer1_data)
        print(f"Layer 2 preview: {layer2_data[:30]}")
        
        # Step 3: Decode Layer 2
        print("\n📍 Step 3: Layer 2 - Custom Compression")
        layer3_data = layer2_decode(layer2_data)
        print(f"Layer 3 preview: {layer3_data[:30]}")
        
        # Step 4: Decode Layer 3
        print("\n📍 Step 4: Layer 3 - XOR Cipher")
        try:
            flag_data = layer3_decode(layer3_data)
        except Exception as e:
            print(f"Standard decode failed: {e}")
            print("Trying brute force...")
            flag_data = brute_force_layer3(layer3_data)
            if not flag_data:
                raise ValueError("All Layer 3 decryption attempts failed")
        
        # Extract flag
        flag = flag_data.decode('utf-8', errors='ignore').strip()
        
        # Clean up flag (remove null bytes and extra characters)
        flag = flag.split('\\x00')[0]  # Remove null bytes
        flag = flag.rstrip('\\x00')    # Remove trailing nulls
        
        print(f"\n🎉 RAW FLAG DATA: {flag_data}")
        print(f"🎉 CLEANED FLAG: {flag}")
        
        # Verify flag format
        if 'XPL_01TZ_CTF{' in flag and '}' in flag:
            # Extract just the flag part
            start = flag.find('XPL_01TZ_CTF{')
            end = flag.find('}', start) + 1
            if end > start:
                final_flag = flag[start:end]
                print(f"✅ FINAL FLAG: {final_flag}")
                return final_flag
        
        return flag
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    import sys
    pdf_file = sys.argv[1] if len(sys.argv) > 1 else "final_challenge.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"❌ File not found: {pdf_file}")
        print("Please provide the path to final_challenge.pdf")
        sys.exit(1)
    
    result = solve_matryoshka(pdf_file)
    
    if result:
        print(f"\n✅ Success! Flag: {result}")
    else:
        print(f"\n❌ Failed to solve the challenge")
