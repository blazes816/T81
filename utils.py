from functools import reduce

def pack_bytes(byte_array):
    byte_array = bytearray([int(x, 16) for x in byte_array if type(x) == 'str'])
    return reduce(lambda x,y: (x << 8) + y, byte_array, 0x0)
