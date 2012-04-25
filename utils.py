from functools import reduce

def pack_bytes(byte_array):
    if len(byte_array) < 2:
        try:
          return int(str(byte_array[0]), 16)
        except IndexError:
          return 0
    
    return int(reduce(lambda x, y: (x << 8) + y, byte_array[1:], byte_array[0]))

def unpack_bytes(value, size=1, base=16):
    byte_array = bytearray()

    if type(value) is str:
        value = int(str(value), 16)

    if value == 0:
      return bytearray([0] * size)

    while value > 0:
        byte_array.append(value & 0xff)
        value = value >> 8

    if size != 1:
        while len(byte_array) < size:
            byte_array.append(0x0)
        
    return byte_array[::-1]

def clean_memory(memory):
    return memory[1:-1]
