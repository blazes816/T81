from functools import reduce

def pack_bytes(byte_array):
    if len(byte_array) < 2:
        try:
          return int(byte_array[0])
          return int(str(byte_array[0]), 16)
        except IndexError:
          return 0
    
    return int(reduce(lambda x, y: (x << 8) + y, byte_array[1:], byte_array[0]))

def unpack_bytes(value, min=1, max=None):
    byte_array = bytearray()

    if type(value) is str:
        value = int(str(value), 16)
    elif type(value) is bytearray:
        value = pack_bytes(value)

    if value == 0:
      return bytearray([0] * min)

    while value > 0:
        byte_array.append(value & 0xff)
        value = value >> 8

    while len(byte_array) < min:
        byte_array.append(0x0)

    if max is None:
        max = -(len(byte_array) + 1)
    else:
        max = -(max + 1)
        
    return byte_array[-1:max:-1]

def clean_memory(memory):
    return int(str(memory[1:-1]), 16)
