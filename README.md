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
