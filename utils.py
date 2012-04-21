from functools import reduce

def pack_bytes(byte_array):
    if len(byte_array) == 1:
      return int(str(byte_array[0]), 16)

    byte_array = bytearray([int(str(x), 16) for x in byte_array])
    return int(str(reduce(lambda x,y: (x << 8) + y, byte_array, 0x0)), 16)
