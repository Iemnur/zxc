from typing import Callable, List, Optional
from shared.expression import *
from shared.types import Enum


class Operand:
    def __init__(self, value, size):
        self.size = size
        self.value = value
        pass


class Label(object):
    def __init__(self, idx, name, offset):
        self.idx = idx
        self.name = name
        self.offset = offset
        pass


class Entrypoint(Label):
    def __init__(self, idx, name, offset):
        super(Entrypoint, self).__init__(idx, name, offset)
        pass


class FunctionType(Enum):
    GLOBAL = 0
    STATIC = 1


class Function(Label):
    def __init__(self, idx, name, offset, func_type):
        super(Function, self).__init__(idx, name, offset)
        self.type = func_type
        pass


class InstructionDescriptor:
    def __init__(self, opcode, mnemonic, handler):
        self.opcode = opcode
        self.mnemonic = mnemonic         # type: str
        self.handler = handler           # type: Callable[[any], Instruction]


class InstructionTable:
    def __init__(self, inst_list):
        # type: (List[InstructionDescriptor]) -> None
        self.table = {}
        self.update(inst_list)

    def update(self, inst_list):
        # type: (List[InstructionDescriptor]) -> InstructionTable
        for i in inst_list:
            self.table[i.opcode] = i

        return self

    def get_inst_desc(self, opcode):
        # type: (int) -> InstructionDescriptor
        return self.table[opcode]

    def read_opcode(self, fs):
        return fs.read_u8()


class Instruction:
    InvalidOffset = None

    def __init__(self, opcode):
        self.opcode = opcode                    # type: int
        self.offset = self.InvalidOffset        # type: int
        self.size = 0                           # type: int
        self.expr = None                        # type: Optional[Expression]
        self.operands = []                      # type: List[Operand]
        self.descriptor = None                  # type: Optional[InstructionDescriptor]
        self.flags = None
        self.text = None                        # type: Optional[unicode]
        self.comment = None                     # type: Optional[unicode]
