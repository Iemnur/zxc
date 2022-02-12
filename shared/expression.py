class UnaryExpression:
    EQ = 1               # value = value
    NEGATE = 2           # value = -value
    BITWISE_NOT = 0x30   # value = ~value

    MNEMONIC = {
        EQ: U'EQ',
        NEGATE: U'NEG',
        BITWISE_NOT: U'NOT',
    }

    NAME_DICT = {v.upper(): k for k, v in MNEMONIC.iteritems()}

    def __init__(self, value):
        self.value = value
        self.name = self.MNEMONIC[value]
        pass

    @staticmethod
    def get_name(t):
        if t in UnaryExpression.MNEMONIC:
            return UnaryExpression.MNEMONIC[t]

        print 'Unk UnaryExpression: {}'.format(t)
        return hex(t)

    @staticmethod
    def get_value_name(name):
        return UnaryExpression.NAME_DICT.get(name.upper())


class BinaryExpression:
    ADD = 1
    SUB = 2
    MUL = 3
    DIV = 4
    MOD = 5                              # a % b
    EQ = 0x10                            # a == b
    NEQ = 0x11                           # a != b
    GT = 0x12                            # a > b
    GEQ = 0x13                           # a >= b
    LT = 0x14                            # a < b
    LEQ = 0x15                           # a <= b
    AND = 0x20                           # a && b
    OR = 0x21                            # a || b
    BITWISE_AND = 0x31                   # a & b
    BITWISE_OR = 0x32                    # a | b
    BITWISE_XOR = 0x33                   # a ^ b
    BITWISE_SHIFT_LEFT = 0x34            # a << b
    BITWISE_SHIFT_RIGHT = 0x35           # a >> b
    BITWISE_UNSIGNED_SHIFT_RIGHT = 0x36  # a >>> b

    MNEMONIC = {
        ADD: U'ADD',
        SUB: U'SUB',
        MUL: U'MUL',
        DIV: U'DIV',
        MOD: U'MOD',
        EQ: U'EQ',
        NEQ: U'NEQ',
        GT: U'GT',
        GEQ: U'GEQ',
        LT: U'LT',
        LEQ: U'LE',
        AND: U'AND',
        OR: U'OR',
        BITWISE_AND: U'BITAND',
        BITWISE_OR: U'BITOR',
        BITWISE_XOR: U'XOR',
        BITWISE_SHIFT_LEFT: U'SHL',
        BITWISE_SHIFT_RIGHT: U'SAR',  # Shift Arithmetically left (signed shift left)
        BITWISE_UNSIGNED_SHIFT_RIGHT: U'SHR',
    }

    NAME_DICT = {v.upper(): k for k, v in MNEMONIC.iteritems()}

    def __init__(self, value):
        self.value = value
        self.name = self.MNEMONIC[value]
        pass

    @staticmethod
    def get_name(t):
        if t in BinaryExpression.MNEMONIC:
            return BinaryExpression.MNEMONIC[t]

        print 'Unk BinaryExpression: {}'.format(t)
        return hex(t)

    @staticmethod
    def get_value_name(name):
        return BinaryExpression.NAME_DICT.get(name.upper())


class Expression:
    UNARY = 0
    BINARY = 1

    def __init__(self, expr_type, value):
        self.expr_type = expr_type

        if expr_type == self.UNARY:
            self.expr = UnaryExpression(value)
        else:
            self.expr = BinaryExpression(value)
        pass

    @classmethod
    def from_expr_name(cls, expr_type, name):
        value = None
        if expr_type == cls.UNARY:
            value = UnaryExpression.get_value_name(name)
        elif expr_type == cls.BINARY:
            value = BinaryExpression.get_value_name(name)

        if value is None:
            print U'Unknown expression name "{}"'.format(name)
            raise ValueError

        return cls(expr_type, value)
