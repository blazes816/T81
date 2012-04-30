from functools import reduce

codeToName = {
  0x00: 'eax',
  0x01: 'ax',
  0x02: 'ah',
  0x03: 'al',
  0x04: 'ebx',
  0x05: 'bx',
  0x06: 'bh',
  0x07: 'bl',
  0x08: 'ecx',
  0x09: 'cx',
  0x0a: 'ch',
  0x0b: 'cl',
  0x0c: 'edx',
  0x0d: 'dx',
  0x0e: 'dh',
  0x0f: 'dl',
}
nameToCode = {codeToName[x]: x for x in codeToName}

class Registers(object):
    @staticmethod
    def codeToName(code):
        return codeToName[code]

    @staticmethod
    def sizeOf(reg):
        if len(reg) == 3:
            return 4
        elif reg[1] == 'x':
            return 2
        return 1

    @staticmethod
    def nextSize(reg):
        if len(reg) == 2:
            if reg[1] == 'h' or reg[1] == 'l':
                return "%s%s" % reg[0], 'x'
            else:
                return "e%sx" % reg[0]

    def __init__(self):
        self.eax = 0
        self.ebx = 0
        self.ecx = 0
        self.edx = 0

        self.pc = 0

        self.stack = []
        self.sp = 0

        self.registers = {
          'eax': self.eax, 'ebx': self.ebx, 'ecx': self.ecx, 'edx': self.edx,
          'pc': self.pc, 'sp': self.sp
        }

        self.registers_available = list(self.registers.keys())

    def incrementPC(self, amount=0x01):
        self.pc = (self.pc + amount)

    def set(self, name, value):
        if name in list(self.registers.keys()):
            self.registers[name] = value
        elif len(name) == 2:
            suffix, name = name[1], 'e%sx' % name[0]
            if suffix == 'x':
                self.registers[name] = (self.registers[name] & 0xffff0000) + value
            elif suffix == 'l':
                self.registers[name] = (self.registers[name] & 0xffffff00) + value
            elif suffix == 'h':
                self.registers[name] = (self.registers[name] & 0xffff00ff) + (value << 8)
            else:
                self.registers[name] = value

    def get(self, name):
        if type(name) is int:
            name = self.codeToName(name)

        if name in list(self.registers.keys()):
            return self.registers[name]
        elif len(name) == 2:
            suffix, name = name[1], 'e%sx' % name[0]
            if suffix == 'x':
                return self.registers[name] & 0xFFFF
            elif suffix == 'l':
                return self.registers[name] & 0xFF
            elif suffix == 'h':
                return self.registers[name] & 0xFF00

    def __repr__(self):
        view = ["%s: 0x%0.6x" % (x, self.registers[x]) for x in self.registers.keys()]
        view = "{%s}" % ', '.join(view)
        return view
