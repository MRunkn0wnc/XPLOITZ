# The Matryoshka Conspiracy CTF

## Challenge Description
A mysterious PDF file contains hidden secrets buried under multiple layers of obfuscation. 
Your mission: extract the embedded file and unravel the custom encoding layers to find the flag.

**File:** `final_challenge.pdf`  
**Flag Format:** `XPL_01TZ_CTF{...}`  


Solution Path
1. **Extract embedded data** from the PDF using tools like `hexedit`
2. **Analyze the encoding layers** - look for L1, L2, L3 markers
3. **Reverse Layer 1**: Fibonacci XOR + bit rotation
4. **Reverse Layer 2**: Custom byte substitution with markers  
5. **Reverse Layer 3**: XOR cipher with key derivation
6. **Recover the flag**: `XPL_01TZ_CTF{...}`

 Hints
- Start with: `hexedit -a final_challenge.pdf`
- Each layer has a header: L1, L2, L3
- Layer 1 uses Fibonacci sequence for XOR key
- Layer 2 inserts 0xFF markers between data chunks
- Layer 3 uses SHA256 key derivation
- No standard tools will work - custom Python code required
Tools You'll Need
- PDF analysis:hexedit{web based}
- Python for custom decoding scripts
- Cryptography and reverse engineering skills

Note
This challenge tests deep technical skills in file forensics, custom encoding schemes, and cryptographic reverse engineering.

## Flag Format
The flag follows the pattern: `XPL_01TZ_CTF{...}`

def layer1_encode(data):
    """
    Encodes data using Fibonacci-based XOR and bit rotation
    
    Steps:
    1. Calculate CRC32 checksum of original data
    2. Generate Fibonacci sequence up to 256 elements
    3. For each byte:
       - XOR with Fibonacci value (position-based)
       - Rotate bits left by 1-7 positions
    4. Prepend header: 'L1' + length + checksum
    
    Args:
        data: bytes to encode
        
    Returns:
        bytes: Encoded data with L1 header
    """
    """
    def layer1_decode(encoded_data):
    """
    Decodes Layer 1 encoded data
    
    Steps:
    1. Verify 'L1' header exists
    2. Extract data length and expected CRC32
    3. Reverse bit rotation (right shift)
    4. Reverse Fibonacci XOR
    5. Verify CRC32 matches
    
    Args:
        encoded_data: L1-encoded bytes
        
    Returns:
        bytes: Decoded data for next layer
    """

    class CustomCompressor:
    """
    Handles custom compression with byte substitution and markers
    """
    
    def _generate_substitution_table(self):
        """
        Creates 1-byte → 2-byte mapping using SHA256
        
        Each input byte maps to 2 output bytes derived from:
        hashlib.sha256(seed + byte).digest()[:2]
        """
    
    def compress(self, data):
        """
        Compression process:
        1. Expand each byte to 2 bytes using substitution table
        2. Insert 0xFF markers every 4 bytes
        3. Base85 encode the result
        4. Prepend 'L2' header
        """
    
    def decompress(self, compressed_data):
        """
        Decompression process:
        1. Base85 decode
        2. Remove 0xFF markers
        3. Reverse byte substitution using lookup table
        """

        class XorCipher:
    """
    XOR cipher with SHA256-based key derivation
    """
    
    def _derive_key(self, data_length):
        """
        Derives encryption key using:
        hashlib.sha256(key_seed + struct.pack('<I', data_length)).digest()
        """
    
    def encrypt(self, data):
        """
        Encryption:
        1. Derive key based on data length
        2. XOR each byte with key bytes (cycling)
        3. Prepend 'L3' header
        """
    
    def decrypt(self, encrypted_data):
        """
        Decryption:
        1. Try multiple length assumptions for key derivation
        2. XOR decrypt with derived key
        3. Validate result (UTF-8 or flag pattern)
        """

        def solve():
    """
    Complete solution process:
    
    1. Extract payload from PDF
    2. Decode Layer 1 (VM Bytecode)
    3. Decode Layer 2 (Custom Assembly) 
    4. Decode Layer 3 (Polymorphic Encoding)
    5. Decode Layer 4 (Control Flow)
    6. Extract flag
    """
