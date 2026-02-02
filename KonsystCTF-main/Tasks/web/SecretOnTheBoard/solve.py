import base64
import random
import sys

def reverse_x(b):
    return bytes([x ^ 0xF0 for x in b])

def reverse_y(b):
    tmp = bytearray(b)
    if len(tmp) > 0:
        last = tmp[-1]
        for j in range(len(tmp)-1, 0, -1):
            tmp[j] = tmp[j-1]
        tmp[0] = last
    return bytes(tmp)

def reverse_z(b):
    return bytes([(x - 1) % 256 for x in b])

def reverse_q(b):
    return b.replace(b'Q', b'a')

def reverse_w(b):
    return bytes([x & 0xF0 for x in b])

def reverse_r(b):
    return bytes(reversed(b))

def reverse_s(b):
    output = bytearray(b)
    for i in range(len(output)):
        output[i] ^= output[-(i+1)]
    return bytes(output)

def decrypt(encrypted_str):
    random.seed(42)
    fs_order = [] 
    
    for _ in range(5):
        fs_order.append(random.choice(['_x', '_y', '_z', '_q', '_w', '_r', '_s']))
    
    data = base64.b64decode(encrypted_str)
    
    if data.endswith(b'%%'):
        data = data[:-2]
    
    reverse_mapping = {
        '_x': reverse_x,
        '_y': reverse_y,
        '_z': reverse_z,
        '_q': reverse_q,
        '_w': reverse_w,
        '_r': reverse_r,
        '_s': reverse_s
    }
    
    for f_name in reversed(fs_order):
        data = reverse_mapping[f_name](data)
    
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return data.decode('utf-8', errors='replace')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encrypted_string>")
        sys.exit(1)
    
    encrypted = sys.argv[1]
    print("Decrypted:", decrypt(encrypted))