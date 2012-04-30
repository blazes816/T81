from utils import unpack_bytes, pack_bytes

codeToInt = {
    0x00: 'print_string',
    0x01: 'print_int', 
    0x10: 'read_int',
    0x20: 'print_registers',
}

class Interrupts(object):
    def __init__(self, registers, memory):
        self.registers = registers
        self.memory = memory

    def print_string(self):
        a = self.registers.get('ax')
        index = 0
        string = ''
        char = self.memory[a]
        while char != 0x00:
            string += chr(char)
            index += 1
            char = self.memory[a + index]
        print(string)

    def print_int(self):
        a = self.registers.get('ax')
        print(a)

    def print_word(self):
        print(hex(self.registers.get('ax')))


    def read_int(self):
        a = pack_bytes(unpack_bytes(int(input("")), 2, 2))
        self.registers.set('ax', a)

    def print_registers(self):
        print(self.registers)
