class InvalidFile(Exception):
    pass

class EndOfProgram(Exception):
    pass
    
class AssemblyException(Exception):
    pass

class InvalidOperandSize(AssemblyException):
    pass

class InvalidOperandRegister(AssemblyException):
    pass

class InvalidDataSize(AssemblyException):
    pass
