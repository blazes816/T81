from functools import reduce

def pack_bytes(byte_array):
    if len(byte_array) < 2:
        try:
          return int(str(byte_array[0]), 16)
        except IndexError:
          return 0
    
    return int(reduce(lambda x, y: (x << 8) + y, byte_array[1:], byte_array[0]))

def unpack_bytes(value, size=None):
    byte_array = bytearray()
    while int(str(value), 16) > 0:
        byte_array.insert(0, value & 0xff)
        value = value >> 8

    if size is not None:
        while len(byte_array) < size:
            byte_array.append(0x0)
        
    return byte_array
