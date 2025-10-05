from layer1 import layer1_encode, layer1_decode
from layer2 import layer2_encode, layer2_decode  
from layer3 import layer3_encode, layer3_decode

def test_all():
    test_data = b"XPL_01TZ_CTF{Test_Flag}"
    print("Testing Layer 3...")
    l3 = layer3_encode(test_data)
    l3_dec = layer3_decode(l3)
    assert test_data == l3_dec
    print("Layer 3 OK")
    
    print("Testing Layer 2...")
    l2 = layer2_encode(l3)
    l2_dec = layer2_decode(l2)
    assert l3 == l2_dec
    print(" Layer 2 OK")
    
    print("Testing Layer 1...")
    l1 = layer1_encode(l2)
    l1_dec = layer1_decode(l1)
    assert l2 == l1_dec
    print(" Layer 1 OK")
    
    print(" All layers work!")

if __name__ == "__main__":
    test_all()
