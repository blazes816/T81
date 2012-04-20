codeToOperation = {
  0x0: 'mov_r_r',
  0x1: 'mov_r_r'
}

class Operations(object):
    def __init__(self, program_scanner, main_memory,
                 registers):
        self.program_scanner = program_scanner
        self.main_memory = main_memory
        self.registers = registers

    def fromCode(self, code):
        return getattr(self, codeToOperation[code])

    def scanRegister(self):
        r = self.program_scanner[self.registers.getIP()]
        self.registers.incrementIP()
        return r

    def mov_r_r(self):
        a = self.program_scanner.nextRegister()
        b = self.program_scanner.nextRegister()
        print(b)
        print(self.registers.get(b))
