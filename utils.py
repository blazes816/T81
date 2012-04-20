from functools import reduce

def pack_bytes(byte_array):
    return reduce(lambda x,y: (x << 8) + int(y, 16), byte, 0x0)
