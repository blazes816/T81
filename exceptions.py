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

class UnknownVariable(AssemblyException):
    pass

class RegisterSizeMismatch(AssemblyException):
    pass

class InvalidDataSectionPlacement(AssemblyException):
    pass
