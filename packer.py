import sys
import os
sys.path.append(os.path.dirname(__file__))

from layer1 import layer1_encode
from layer2 import layer2_encode
from layer3 import layer3_encode

def create_challenge():
    # Updated flag format
    flag = "XPL_01TZ_CTF{D33p_F1l3_F0r3ns1cs_M4try0shk4}"
    print("Creating Matryoshka payload...")
    
    layer3_data = layer3_encode(flag.encode())
    layer2_data = layer2_encode(layer3_data)
    layer1_data = layer1_encode(layer2_data)
    
    with open('public/conspiracy_theory.pdf', 'rb') as f:
        pdf_template = f.read()
    
    marker = b'REPLACE_THIS_AREA_WITH_PAYLOAD'
    pdf_final = pdf_template.replace(marker, layer1_data)
    
    obj5_start = pdf_final.find(b'5 0 obj')
    if obj5_start != -1:
        length_pattern = b'/Length 0000'
        length_pos = pdf_final.find(length_pattern, obj5_start)
        if length_pos != -1:
            new_length = f"/Length {len(layer1_data)}".encode()
            while len(new_length) < len(length_pattern):
                new_length += b' '
            pdf_final = pdf_final[:length_pos] + new_length + pdf_final[length_pos + len(length_pattern):]
    
    with open('public/final_challenge.pdf', 'wb') as f:
        f.write(pdf_final)
    
    print(f"Challenge created: public/final_challenge.pdf")
    print(f" Payload size: {len(layer1_data)} bytes")
    print(f" Flag embedded: {flag}")

if __name__ == "__main__":
    create_challenge()
