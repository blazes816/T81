from functools import reduce

def pack_bytes(byte_array):
    if len(byte_array) == 1:
      return int(str(byte_array[0]), 16)
    
    new_array = bytearray()
    for b in byte_array:
        new_array.extend(unpack_bytes(b))
    byte_array = new_array
    byte_array = bytearray([x for x in byte_array])

    return int(str(reduce(lambda x,y: (x << 8) + y, byte_array, 0x0)), 16)

def unpack_bytes(value, size=None):
    byte_array = bytearray()
    while int(str(value), 16) > 0:
        byte_array.insert(0, value & 0xff)
        value = value >> 8

    if size is not None:
        while len(byte_array) < size:
            byte_array.append(0x0)
        
    return byte_array
