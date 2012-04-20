import utils

codeToRegister = {
  0x00: 'eax',
  0x01: 'ax',
  0x02: 'ah',
  0x03: 'al',
  0x04: 'ebx',
  0x05: 'bx',
  0x06: 'bh',
  0x07: 'bl',
}

class Registers(object):
    def __init__(self):
        self.eax = bytearray()
        self.ebx = bytearray()
        self.ecx = bytearray()
        self.edx = bytearray()

        self.pc = bytearray()

        self.registers = {
          'eax': self.eax, 'ebx': self.ebx, 'ecx': self.ecx, 'edx': self.edx,
          'pc': self.pc
        }

        self.registers_available = list(self.registers.keys())

        for r in self.registers.keys():
            for b in range(8):
                getattr(self, r).append(0x00)

    def __getattr__(self, name):
        prefix, name = name[:4], name[4:]
        if prefix == 'set_':
            def setter(value):
                setattr(self, name, value)
            return setter

        elif prefix == 'get_':

            if name in (self.registers.keys()):
                return utils.pack_bytes(self.registers[name])

            if len(name) != 2:
                raise AttributeError

            if (name[0] in ('a', 'b', 'c' 'd') and name[1] in ('h', 'l', 'x')):
                return self.registers

        
    def incrementPC(self, amount=0x01):
        self.pc = (self.get_pc + amount)

    def getPC(self):
        return self.get_pc

    def get(self, reg):
        if len(reg) == 3:
            return self.registers[reg]
        else:
            v = self.registers['e'+reg]
