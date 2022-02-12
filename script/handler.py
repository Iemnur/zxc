from pack.pck import PCK
from pack.ss import SSScript
from instruction import *
from shared.filestream import FileStream
from stack import StackInstructionVM
from typing import List, Optional, Dict, Tuple
from shared.config import SSIniConfig
import script


class Action:
    Disassemble = 0
    Parse = 1
    Assemble = 2

    def __init__(self, value):
        self.value = value


class HandlerAction:
    def __init__(self, action, handler):
        self.action = action
        self.handler = handler


class HandlerContext(object):
    def __init__(self, action, descriptor=None):
        self.action = action                     # type: Action
        self.instructionTable = None             # type: Optional[InstructionTable]
        self.descriptor = descriptor             # type: Optional[InstructionDescriptor]
        self.instruction = None                  # type: Optional[Instruction]


class DisassemblerHandlerContext(HandlerContext):
    def __init__(self, descriptor=None):
        super(DisassemblerHandlerContext, self).__init__(Action.Disassemble, descriptor)
        self.instruction_disassembled = []        # type: List[Instruction]
        self.ss = None                            # type: Optional[SSScript]
        self.offset = Instruction.InvalidOffset   # type: int
        self.ss_idx = -1                          # type: int
        self.fs = None                            # type: Optional[FileStream]
        self.pck = None                           # type: Optional[PCK]
        self.stackVM = None                       # type: Optional[StackInstructionVM]
        self.func_def = None                      # type: Optional[script.FunctionDef]
        pass


class ParseHandlerContext(HandlerContext):
    def __init__(self, line_idx, line, descriptor=None):
        super(ParseHandlerContext, self).__init__(Action.Parse, descriptor)
        self.line_idx = line_idx                         # type: int
        self.line = line                                 # type: unicode
        self.line_c = line.split(U';', 1)[0].rstrip()    # type: unicode

        pass


class AssembleHandlerContext(HandlerContext):
    def __init__(self, line_idx, line, descriptor=None):
        super(AssembleHandlerContext, self).__init__(Action.Assemble, descriptor)
        self.line_idx = line_idx  # type: int
        self.line = line  # type: unicode

        self.writer = None  # type: Optional[FileStream]
        self.strings = []
        self.ini = None  # type: Optional[SSIniConfig]
        self.labels_offset = []

        self.assembler = None  # type: Optional[script.Assembler]
        pass
