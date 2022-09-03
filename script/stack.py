from pack.ss import SSScript
from script.bytecode import Opcode
from script.instruction import Instruction
from shared.types import VariableType
from typing import List


class Stack:
    def __init__(self, values=None):
        self.values = []
        if values is not None:
            self.values = values
        pass

    @property
    def size(self):
        return len(self.values)

    def push(self, value):
        self.values.append(value)

    def pop(self):
        if self.size == 0:
            raise ValueError('Stack empty!')
        value_pop = self.pop()
        return value_pop

    def peek(self, idx=-1):
        return self.values[idx]


class StackFrame(object):
    def __init__(self):
        self._frames = [0]  # type: List[int]
        self._values = []   # type: List[Instruction]

    @property
    def frame_begin(self):
        return self._frames[-1]

    @property
    def frame_size(self):
        """
        Size of stack values in current frame
        :return: int
        """

        return len(self._values[self.frame_begin:])

    @property
    def size(self):
        return len(self._values)

    def get_value_in_frame(self, idx = 0):
        return self._values[self.frame_begin + idx]

    def open(self):
        self._frames.append(len(self._values))

    def close(self):
        if self.size == 0:
            raise ValueError('StackFrame empty!')

        depth = self._frames.pop()
        self._values = self._values[:depth]

        return depth

    def duplicate(self):
        self.open()
        self._values.extend(self._values[self.frame_begin:])

    def clear(self):
        self._frames = [0]
        self._values = []

    def push(self, value):
        # type: (Instruction) -> int
        self._values.append(value)

        return self.size

    def pop(self):
        # type: () -> Instruction
        if self.size < self.frame_begin:
            raise ValueError('Frame negative!')
        return self._values.pop()

    # def get_frame(self, idx=-1):
    #     return self.frames[idx]


class StackInstructionVM(StackFrame):
    def __init__(self):
        super(StackInstructionVM, self).__init__()
        # self.stack.open()
        self.local_var_type = []  # type: List[VariableType]
        self.local_var_name = []  # type: List[unicode]

    def get_local_var_name(self, idx):
        return self.local_var_name[idx]

    def clear_local_var(self):
        self.local_var_type = []
        self.local_var_name = []

    def add_local_var_type(self, vt):
        # type: (VariableType) -> None
        self.local_var_type.append(vt)
        pass

    def add_local_var_name(self, name):
        # type: (unicode) -> None
        self.local_var_name.append(name)
        pass
