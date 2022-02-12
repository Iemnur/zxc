

class HeaderPair:
    def __init__(self, offset, count):
        self.offset = offset
        self.count = count

    @classmethod
    def load(cls, fs):
        offset = fs.read_u32()
        count = fs.read_u32()

        return cls(offset, count)


class VariableType:
    VOID = 0
    INT = 0x0A
    INT_LIST = 0x0B
    INT_REF = 0x0D
    INT_LIST_REF = 0x0E
    STR = 0x14
    STR_LIST = 0x15
    STR_REF = 0x17
    STR_LIST_REF = 0x18
    FRAME_ACTION = 0x04BA
    STAGE_ELEM = 0x0514
    OBJ = 0x051E

    TYPE_NAME = {
        VOID: U'Void',
        INT: U'Int',
        INT_LIST: U'IntList',
        INT_REF: U'IntRef',
        INT_LIST_REF: U'IntListRef',
        STR: U'Str',
        STR_LIST: U'StrList',
        STR_REF: U'StrRef',
        STR_LIST_REF: U'StrListRef',
        OBJ: U'Obj',
        STAGE_ELEM: U'StageElem',
        FRAME_ACTION: U'FrameAction'
    }

    NAME_DICT = {v.upper(): k for k, v in TYPE_NAME.iteritems()}

    def __init__(self, value):
        self.value = value
        self.name = self.get_type_name(value)
        pass

    @staticmethod
    def get_type_name(t):
        if t not in VariableType.TYPE_NAME:
            print 'Unk VariableType: {}'.format(t)
            return hex(t)

        return VariableType.TYPE_NAME[t]

    @staticmethod
    def get_type_value(name):
        return VariableType.NAME_DICT.get(name.upper())

    @classmethod
    def from_type_name(cls, name):
        type_value = cls.get_type_value(name)
        if type_value is None:
            print(U'Type name "{}" invalid!'.format(name))
            raise ValueError
        return cls(type_value)


class Variable:
    def __init__(self, var_type, value):
        self.var_type = VariableType(var_type)
        self.value = value
        pass


class Enum(int):
    def __new__(cls, value):
        if isinstance(value, str):
            return getattr(cls, value)
        elif isinstance(value, int):
            return cls.__index[value]  # type: ignore

    def __str__(self):
        return self.__name  # type: ignore

    def __repr__(self):
        return "%s.%s" % (type(self).__name__, self.__name)  # type: ignore

    class __metaclass__(type):
        def __new__(mcls, name, bases, attrs):
            attrs['__slots__'] = ['_Enum__name']
            cls = type.__new__(mcls, name, bases, attrs)
            cls._Enum__index = _index = {}
            for base in reversed(bases):
                if hasattr(base, '_Enum__index'):
                    _index.update(base._Enum__index)
            # create all of the instances of the new class
            for attr in attrs.keys():
                value = attrs[attr]
                if isinstance(value, int):
                    evalue = int.__new__(cls, value)  # type: ignore
                    evalue._Enum__name = attr
                    _index[value] = evalue
                    setattr(cls, attr, evalue)
            return cls

