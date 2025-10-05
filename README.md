The Matryoshka Conspiracy CTF
Challenge Description

A mysterious PDF file contains hidden secrets buried under multiple layers of obfuscation. Your mission is to extract the embedded file and unravel the custom encoding layers to find the flag.

File: final_challenge.pdf
Flag Format: XPL_01TZ_CTF{...}
Solution Path

    Extract embedded data from the PDF

    Analyze the encoding layers - look for L1, L2, L3 markers

    Reverse Layer 1: Fibonacci XOR + bit rotation

    Reverse Layer 2: Custom byte substitution with markers

    Reverse Layer 3: XOR cipher with key derivation

    Recover the flag

Hints

    Start with hex analysis of the PDF file

    Each layer has a header: L1, L2, L3

    Layer 1 uses Fibonacci sequence for XOR key

    Layer 2 inserts 0xFF markers between data chunks

    Layer 3 uses SHA256 key derivation

    Custom Python code required for decoding

Tools Needed

    PDF analysis tools or hex editors

    Python for custom decoding scripts

    Cryptography and reverse engineering skills

Technical Details
Layer 1: Fibonacci XOR + Bit Rotation

    Uses Fibonacci sequence modulo 256 for XOR operations

    Applies bit rotation (1-7 bits) based on byte position

    Includes CRC32 checksum for data integrity

    Header format: L1 + data length + checksum

Layer 2: Custom Compression

    Implements byte substitution using SHA256 mapping

    Expands each byte to 2 bytes

    Inserts 0xFF marker bytes at regular intervals

    Uses Base85 encoding for text representation

    Header format: L2

Layer 3: XOR Cipher

    Uses SHA256-based key derivation

    Key depends on data length parameter

    Simple XOR encryption with derived key

    Header format: L3

Note

This challenge tests advanced skills in file forensics, custom algorithm reversal, and cryptographic analysis. Success requires systematic approach and custom tool development.
Flag Format

The flag follows the pattern: XPL_01TZ_CTF{...}
