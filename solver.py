import sys
import os
sys.path.append(os.path.dirname(__file__))

from layer1 import layer1_decode
from layer2 import layer2_decode
from layer3 import layer3_decode

def extract_embedded_file(pdf_path):
    with open(pdf_path, 'rb') as f:
        data = f.read()
    obj5_start = data.find(b'5 0 obj')
    stream_start = data.find(b'stream\n', obj5_start) + 7
    stream_end = data.find(b'\nendstream', stream_start)
    return data[stream_start:stream_end]

def solve():
    pdf_path = "public/final_challenge.pdf"
    if not os.path.exists(pdf_path):
        print("❌ Challenge PDF not found")
        return
    
    print("Solving Matryoshka Conspiracy...")
    try:
        layer1_data = extract_embedded_file(pdf_path)
        print("Extracted embedded file")
        
        layer2_data = layer1_decode(layer1_data)
        print(" Decoded Layer 1")
        
        layer3_data = layer2_decode(layer2_data)
        print(" Decoded Layer 2")
        
        flag_data = layer3_decode(layer3_data)
        print(" Decoded Layer 3")
        
        flag = flag_data.decode('utf-8')
        print(f" FLAG: {flag}")
        
    except Exception as e:
        print(f" Failed: {e}")

if __name__ == "__main__":
    solve()
