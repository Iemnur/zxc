from instruction import *
from shared.common import *
import script
import re

PAT_PUSH_STRING = r'(\\\w+{[^}]*})|(\\\w)'


class Opcode:
    OP_0 = 0x0
    LINE = 0x1
    PUSH = 0x2
    POP = 0x3
    DUP_VALUE = 0x4
    CLOSE_FRAME = 0x5
    DUP_FRAME = 0x6
    DECLARE_VAR = 0x7
    OPEN_FRAME = 0x8
    PARAMS_END = 0x9
    JUMP = 0x10
    JUMP_IF_NOT_ZERO = 0x11
    JUMP_IF_ZERO = 0x12
    SHORT_CALL_13 = 0x13
    SHORT_CALL_14 = 0x14
    RETURN = 0x15
    END = 0x16
    ASSIGNMENT = 0x20
    UNARY_EXPR = 0x21
    BINARY_EXPR = 0x22
    FUNC_CALL = 0x30
    TEXT = 0x31
    SET_NAME = 0x32
    OP_33 = 0x33
    OP_34 = 0x34

    _MNEMONIC = {
        OP_0: U'OP_0',  # error
        LINE: U'LINE',
        PUSH: U'PUSH',
        POP: U'POP',
        DUP_VALUE: U'DUPVAL',
        CLOSE_FRAME: U'CLOSE',
        DUP_FRAME: U'DUPFRAME',
        DECLARE_VAR: U'VAR',
        OPEN_FRAME: U'OPEN',
        PARAMS_END: U'PARAMSEND',
        JUMP: U'JMP',
        JUMP_IF_NOT_ZERO: U'JNZ',
        JUMP_IF_ZERO: U'JZ',
        SHORT_CALL_13: U'SCALL13',
        SHORT_CALL_14: U'SCALL14',
        RETURN: U'RET',
        END: U'END',
        ASSIGNMENT: U'MOV',
        UNARY_EXPR: U'UEXPR',
        BINARY_EXPR: U'BEXPR',
        FUNC_CALL: U'CALL',
        TEXT: U'TEXT',
        SET_NAME: U'NAME',
        OP_33: U'NOP_33',
        OP_34: U'NOP_34',
    }

    MNEMONIC = {k: v.upper() for k, v in _MNEMONIC.iteritems()}
    NAME_DICT = {v.upper(): k for k, v in MNEMONIC.iteritems()}

    def __init__(self, value):
        self.value = value
        self.name = self.get_name(value)

    @staticmethod
    def get_name(op):
        return Opcode.MNEMONIC.get(op)

    @staticmethod
    def get_opcode(name):
        return Opcode.NAME_DICT.get(name)


def handler_line_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    fs = ctx.fs
    line_number = fs.read_u32()
    inst = ctx.instruction

    inst.operands = [Operand(line_number, 4)]
    inst.text = U'{} {}'.format(Opcode.get_name(inst.opcode), line_number)
    ctx.stackVM.clear()

    return inst


def handler_line_parse(line):
    # type: (unicode) -> Tuple[int, int]

    line_c = line.split(U';', 1)[0].rstrip()  # line with clear comment.
    line_c = remove_dup_space(line_c)
    line_number = str_to_int(line_c.split(U' ')[1])

    return Opcode.LINE, line_number


def handler_line_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction

    _, line_number = handler_line_parse(ctx.line)

    inst.operands = inst.operands = [Operand(line_number, 4)]
    ctx.assembler.current_line_code = line_number

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)
    writer.write_u32(line_number)

    return inst


def handler_push_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    fs = ctx.fs
    value_type = fs.read_u32()
    value = fs.read_u32()

    v = Variable(value_type, value)
    inst = ctx.instruction
    inst.operands = [Operand(v, 8)]
    inst.text = U'{} {} {}'.format(Opcode.get_name(inst.opcode), v.var_type.name, v.value)

    # extra comment info
    if value_type == VariableType.STR:
        inst.comment = U'{}'.format(ctx.ss.strings[value])
    elif value_type == VariableType.INT:
        stack_size = ctx.stackVM.frame_size
        if stack_size == 1:
            top_inst = ctx.stackVM.get_value_in_frame()
            if top_inst.opcode == Opcode.PUSH:
                top_push_type = top_inst.operands[0].value.var_type.value
                top_push_value = top_inst.operands[0].value.value
                if top_push_type == VariableType.INT:
                    if top_push_value == 0x53:
                        store_type = value >> 24
                        store_index = value & 0x00FFFFFF
                        if store_type == 0:
                            inst.comment = U'local_data_{}'.format(store_index)
                        elif store_type == 0x7D:
                            # LocalVarRef
                            # inst.comment = U'local_var[{}]'.format(store_index)
                            inst.comment = U'local var {}'.format(ctx.stackVM.get_local_var_name(store_index))
        elif stack_size == 0:
            v_type = value >> 24
            v_index = value & 0x00FFFFFF
            if v_type == 0x7F:
                # GlobalVarRef
                # inst.comment = U'global_vars[{}]'.format(v_index)
                if v_index < len(ctx.ss.global_var_name):
                    inst.comment = U'global var {}'.format(ctx.ss.global_var_name[v_index])

    ctx.stackVM.push(inst)
    return inst


def handler_push_parse(line):
    # type: (unicode) -> Tuple[int, Variable]
    line_c = line.split(U';', 1)[0].rstrip()  # line with clear comment.
    line_c = remove_dup_space(line_c)
    _, var_type_name, value = line_c.split(U' ', 2)
    value = value.strip()
    var_type = VariableType.get_type_value(var_type_name)
    if var_type is None:
        print(U'Unknown var type "{}" in line: "{}"'.format(var_type_name, line))
        raise ValueError

    if value[0] != U'"':
        value = str_to_int(value)

    v = Variable(var_type, value)

    return Opcode.PUSH, v


# escape_decode
def parse_string(text):
    value_result = []
    pos = text.find(U'"') + 1
    # pos = 0
    line = text
    line_size = len(line)
    while pos < line_size:
        c = line[pos]
        if c == U'\\' and (pos + 1) < line_size:
            next_c = line[pos + 1]
            if next_c in [U'"', U'\\']:
                value_result.append(next_c)
                pos += 1
            else:
                value_result.append(c)
        elif c == U'"':
            break
        else:
            value_result.append(c)
        pos += 1

    return U''.join(value_result)


# escape_encode
def format_string(text):
    dict_trans = {
        U'"': U'\\"',
        U'\n': U'\\n',
        U'\\': U'\\\\'
    }
    value_result = [U'"']
    pos = 0
    line = text
    line_size = len(line)
    while pos < line_size:
        c = line[pos]
        trans = dict_trans.get(c)
        if trans is not None:
            value_result.append(trans)
        else:
            value_result.append(c)
        pos += 1

    value_result.append(U'"')
    return U''.join(value_result)


def write_normal_string(writer, str_idx):
    # type: (FileStream, int) -> int
    offset = writer.tell()
    writer.write_u8(Opcode.PUSH)
    writer.write_u32(VariableType.STR)
    writer.write_u32(str_idx)

    return offset


def handler_push_string_asm(ctx, push_value):
    # type: (script.AssembleHandlerContext, unicode or int) -> Instruction
    inst = ctx.instruction
    from_string_db = True
    if isinstance(push_value, int):
        text_value = ctx.strings[push_value]
    else:
        text_value = parse_string(push_value)
        from_string_db = False

    chunks = re.split(PAT_PUSH_STRING, text_value)
    has_macro = False
    parse_chunks = []
    for chunk in chunks:
        if not chunk:
            continue

        if chunk and chunk[0] == U'\\':
            if len(chunk) == 2:
                macro_name = ctx.assembler.get_macro_name_by_alias(chunk[1])
                if macro_name:
                    parse_chunks.append((1, macro_name))
                    has_macro = True
                else:
                    parse_chunks.append((0, chunk))
            else:
                tk_start = chunk.find(U'{')
                tk_end = chunk.rfind(U'}')
                macro_name = ctx.assembler.get_macro_name_by_alias(chunk[1:tk_start])
                if macro_name:
                    args = chunk[tk_start + 1:tk_end]
                    parse_chunks.append((2, [macro_name, args]))
                    has_macro = True
                else:
                    parse_chunks.append((0, chunk))
        else:
            parse_chunks.append((0, chunk))

    if has_macro is False:
        parse_chunks = [(0, text_value)]

    for i, (p_type, p_value) in enumerate(parse_chunks):
        if p_type == 0:
            # normal string
            text = p_value
            inst.offset = ctx.writer.tell()
            if from_string_db:
                # push_value is int
                str_idx = push_value
                if i != 0:
                    str_idx = len(ctx.strings)
                    ctx.strings.append(text)
                elif len(parse_chunks) > 1:
                    ctx.strings[str_idx] = text
            else:
                # push_value is unicode
                str_idx = len(ctx.strings)
                ctx.strings.append(text)

            write_normal_string(ctx.writer, str_idx)
            v = Variable(VariableType.STR, str_idx)
            inst.operands = [Operand(v, 8)]

            if len(parse_chunks) != 1:
                inst.text = U'{} {} {} ; {}'.format(Opcode.get_name(inst.opcode),
                                                    v.var_type.name,
                                                    str_idx, text)

            if i != len(parse_chunks) - 1:
                ctx.assembler.statements.append(inst)
                # create new inst
                inst = Instruction(Opcode.PUSH)
                inst.descriptor = ctx.descriptor
                inst.text = ctx.line
                ctx.instruction = inst
        elif p_type == 1:
            # no args
            ctx.assembler.execute_macro(U'@{}'.format(p_value))
        elif p_type == 2:
            # has args
            macro_name, args = p_value
            ctx.assembler.execute_macro(U'@{} {}'.format(macro_name, args))

    # macro -> != push str inst -> need return None
    if parse_chunks[-1][0] in [1, 2]:
        inst = None

    return inst


def handler_push_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction
    _, v = handler_push_parse(ctx.line)
    var_type = v.var_type
    value = v.value

    if var_type.value == VariableType.STR:
        return handler_push_string_asm(ctx, value)

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)
    writer.write_u32(var_type.value)
    writer.write_u32(value)

    v = Variable(var_type.value, value)
    inst.operands = [Operand(v, 8)]

    return inst


def handler_pop_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    fs = ctx.fs
    value_type = fs.read_u32()
    vt = VariableType(value_type)

    inst = ctx.instruction
    inst.operands = [Operand(vt, 4)]
    inst.text = U'{} {}'.format(Opcode.get_name(inst.opcode), vt.name)
    ctx.stackVM.push(inst)

    return inst


def handler_pop_parse(line):
    # type: (unicode) -> Tuple[int, VariableType]
    line_c = line.split(U';', 1)[0].rstrip()  # line with clear comment.
    line_c = remove_dup_space(line_c)
    _, var_type_name = line_c.split(U' ', 1)
    var_type = VariableType.get_type_value(var_type_name)
    if var_type is None:
        print(U'Unknown var type "{}" in line "{}"'.format(var_type_name, line))
        raise ValueError

    vt = VariableType(var_type)

    return Opcode.POP, vt


def handler_pop_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction

    _, vt = handler_pop_parse(ctx.line)
    inst.operands = [Operand(vt, 4)]

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)
    writer.write_u32(vt.value)

    return inst


def handler_duplicate_value_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    fs = ctx.fs
    value_type = fs.read_u32()
    vt = VariableType(value_type)

    inst = ctx.instruction
    inst.operands = [Operand(vt, 4)]
    inst.text = U'{} {}'.format(Opcode.get_name(inst.opcode), vt.name)
    ctx.stackVM.push(inst)

    return inst


def handler_duplicate_value_parse(line):
    # type: (unicode) -> Tuple[int, VariableType]
    line_c = line.split(U';', 1)[0].rstrip()  # line with clear comment.
    line_c = remove_dup_space(line_c)
    _, var_type_name = line_c.split(U' ', 1)
    var_type = VariableType.get_type_value(var_type_name)
    if var_type is None:
        print(U'Unknown var type "{}" in line "{}"'.format(var_type_name, line))
        raise ValueError

    vt = VariableType(var_type)

    return Opcode.DUP_VALUE, vt


def handler_duplicate_value_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction

    _, vt = handler_duplicate_value_parse(ctx.line)

    inst.operands = [Operand(vt, 4)]

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)
    writer.write_u32(vt.value)

    return inst


def handler_close_frame_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    inst = ctx.instruction
    inst.text = U'{}'.format(Opcode.get_name(inst.opcode))

    # exec stack
    skip_close = False
    stack_size = ctx.stackVM.frame_size
    if stack_size > 0:
        top_inst = ctx.stackVM.get_value_in_frame()
        second_inst = ctx.stackVM.get_value_in_frame(1) if stack_size > 1 else None

        op1 = top_inst.opcode
        op2 = second_inst.opcode if second_inst else None
        if op1 == Opcode.PUSH:
            def get_inst_push_info(inst_in):
                t = inst_in.operands[0].value.var_type.value
                v = inst_in.operands[0].value.value

                return t, v

            t1, v1 = get_inst_push_info(top_inst)
            t2, v2 = get_inst_push_info(second_inst) if op2 == Opcode.PUSH else (None, None)

            if t1 == VariableType.INT:
                if v1 == 0x53 and t2 == VariableType.INT and (v2 >> 24) == 0x7D:
                    var_idx = v2 & 0x00FFFFFF
                    if ctx.stackVM.local_var_type[var_idx].value in [VariableType.OBJ,
                                                                     VariableType.FRAME_ACTION,
                                                                     VariableType.STAGE_ELEM]:
                        skip_close = True
                elif (v1 >> 24) == 0x7E and second_inst is None:
                    skip_close = True

    if skip_close is False:
        ctx.stackVM.close()

    return inst


def handler_close_frame_parse(line):
    # type: (unicode) -> int

    return Opcode.CLOSE_FRAME


def handler_close_frame_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)

    return inst


def handler_duplicate_stack_frame_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    inst = ctx.instruction
    inst.text = U'{}'.format(Opcode.get_name(inst.opcode))
    ctx.stackVM.duplicate()

    return inst


def handler_duplicate_stack_frame_parse(line):
    # type: (unicode) -> int

    return Opcode.DUP_FRAME


def handler_duplicate_stack_frame_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)

    return inst


def handler_declare_var_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    fs = ctx.fs
    value_type = fs.read_u32()
    name_index = fs.read_u32()
    vt = VariableType(value_type)

    inst = ctx.instruction
    inst.operands = [Operand(vt, 4), Operand(name_index, 4)]
    inst.text = U'{} {} {}'.format(Opcode.get_name(inst.opcode), vt.name, name_index)
    inst.comment = U'{}'.format(ctx.ss.local_var_names[name_index])

    ctx.stackVM.add_local_var_type(vt)
    ctx.stackVM.add_local_var_name(ctx.ss.local_var_names[name_index])
    ctx.stackVM.push(inst)

    return inst


def handler_declare_var_parse(line):
    # type: (unicode) -> Tuple[int, VariableType, int]
    line_c = line.split(U';', 1)[0].rstrip()  # line with clear comment.
    line_c = remove_dup_space(line_c)
    _, var_type_name, name_index = line_c.split(U' ', 2)
    var_type = VariableType.get_type_value(var_type_name)
    if var_type is None:
        print(U'Unknown var type "{}" in line: "{}"'.format(var_type_name, line))
        raise ValueError

    vt = VariableType(var_type)
    idx = str_to_int(name_index)

    return Opcode.DECLARE_VAR, vt, idx


def handler_declare_var_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction
    _, vt, name_index = handler_declare_var_parse(ctx.line)

    inst.operands = [Operand(vt, 4), Operand(name_index, 4)]

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)
    writer.write_u32(vt.value)
    writer.write_u32(name_index)

    return inst


def handler_open_frame_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    inst = ctx.instruction
    inst.text = U'{}'.format(Opcode.get_name(inst.opcode))
    ctx.stackVM.open()

    return inst


def handler_open_frame_parse(line):
    # type: (unicode) -> int

    return Opcode.OPEN_FRAME


def handler_open_frame_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)

    return inst


def handler_params_end_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    inst = ctx.instruction
    inst.text = U'{}'.format(Opcode.get_name(inst.opcode))
    ctx.stackVM.push(inst)

    return inst


def handler_params_end_parse(line):
    # type: (unicode) -> int

    return Opcode.PARAMS_END


def handler_params_end_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)

    return inst


def handler_jump_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    fs = ctx.fs
    jmp_label = fs.read_u32()

    inst = ctx.instruction
    inst.operands = [Operand(jmp_label, 4)]
    inst.text = U'{} LABEL_{}'.format(Opcode.get_name(inst.opcode), jmp_label)
    ctx.stackVM.push(inst)

    return inst


def handler_jump_parse(line):
    # type: (unicode) -> Tuple[int, unicode]
    line_c = line.split(U';', 1)[0].rstrip()  # line with clear comment.
    line_c = remove_dup_space(line_c)
    mnemonic, label_name = line_c.split(U' ', 1)

    return Opcode.get_opcode(mnemonic.strip().upper()), label_name


def handler_jump_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction
    _, label_name = handler_jump_parse(ctx.line)
    inst.operands = [Operand(label_name, 4)]

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)
    ctx.labels_offset.append((writer.tell(), label_name))
    writer.write_u32(0)

    return inst


def read_argv(fs):
    args = []
    num_args = fs.read_u32()
    for ii in range(num_args):
        type_num = fs.read_u32()
        if type_num == 0xFFFFFFFF:
            args.append(read_argv(fs))
        else:
            args.append(VariableType(type_num))

    args.reverse()
    return args


def write_argv(fs, argv):
    # type: (FileStream, List[VariableType]) -> None
    argv.reverse()
    argc = len(argv)
    fs.write_u32(argc)
    for vt in argv:
        if isinstance(vt, list):
            fs.write_u32(0xFFFFFFFF)
            write_argv(fs, vt)
        else:
            fs.write_u32(vt.value)

    pass


def format_argv(argv_in):
    ret = []
    for vv in argv_in:
        if isinstance(vv, list):
            ret.append(U'[{}]'.format(format_argv(vv)))
        else:
            ret.append(vv.name)

    return U', '.join(ret)


def get_chunks_from_line(line):
    res = []
    chunk = U''
    pos = 0
    while pos < len(line):
        c = line[pos]
        if c == U' ':
            pos += 1
            if len(chunk) > 0:
                res.append(chunk)
                chunk = U''
        elif c == U'(':
            end = line.find(U')', pos)
            if end == -1:
                print U'Token ")" not found!'
                raise ValueError
            chunk = line[pos: end + 1]
            res.append(chunk)
            chunk = U''
            pos = end + 1
        elif c == U':':  # ex: CALL 0 (Int, Int, Int, Int, Int) ():Void
            pos += 1
        else:
            chunk += c
            pos += 1

    if len(chunk) > 0:
        res.append(chunk)

    return res


def parse_argv(argv_str, pos=1):
    res = []
    type_name = U''
    while pos < len(argv_str):
        c = argv_str[pos]
        if c == U' ':
            pos += 1
            type_name = U''
        elif c == U'[':
            pos += 1
            type_name = U''
            v_list, pos = parse_argv(argv_str, pos)
            res.append(v_list)
        elif c == U']' or c == U')':
            pos += 1
            if len(type_name) > 0:
                vt = VariableType.from_type_name(type_name)
                res.append(vt)
            break
        else:
            if c == U',':
                pos += 1
                if len(type_name) > 0:
                    vt = VariableType.from_type_name(type_name)
                    res.append(vt)
                    type_name = U''
            else:
                type_name += c
                pos += 1

    return res, pos


def handler_short_call_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    fs = ctx.fs
    call_label = fs.read_u32()
    pos = fs.tell()
    argv = read_argv(fs)

    inst = ctx.instruction
    inst.operands = [Operand(call_label, 4), Operand(argv, fs.tell() - pos)]

    inst.text = U'{} LABEL_{} ({})'.format(Opcode.get_name(inst.opcode), call_label, format_argv(argv))
    ctx.stackVM.push(inst)

    return inst


def handler_short_call_parse(line):
    # type: (unicode) -> Tuple[int, unicode, unicode]
    line_c = line.split(U';', 1)[0].rstrip()  # line with clear comment.
    line_c = remove_dup_space(line_c)
    mnemonic, label_name, argv_str = get_chunks_from_line(line_c)

    return Opcode.get_opcode(mnemonic.strip().upper()), label_name, argv_str


def handler_short_call_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction
    _, label_name, argv_str = handler_short_call_parse(ctx.line)

    argv, _ = parse_argv(argv_str)
    inst.operands = [Operand(label_name, 4), Operand(argv, None)]

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)
    ctx.labels_offset.append((writer.tell(), label_name))
    writer.write_u32(0)  # call label
    write_argv(writer, argv)

    return inst


def handler_return_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    fs = ctx.fs
    pos = fs.tell()
    argv = read_argv(fs)

    inst = ctx.instruction
    inst.operands = [Operand(argv, fs.tell() - pos)]
    inst.text = U'{} ({})\r\n'.format(Opcode.get_name(inst.opcode), format_argv(argv))
    ctx.stackVM.clear()

    return inst


def handler_return_parse(line):
    # type: (unicode) -> Tuple[int, unicode]
    line_c = line.split(U';', 1)[0].rstrip()  # line with clear comment.
    line_c = remove_dup_space(line_c)
    mnemonic, argv_str = get_chunks_from_line(line_c)

    return Opcode.RETURN, argv_str


def handler_return_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction
    _, argv_str = handler_return_parse(ctx.line)

    argv, _ = parse_argv(argv_str)
    inst.operands = [Operand(argv, None)]

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)
    write_argv(writer, argv)

    return inst


def handler_end_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    inst = ctx.instruction
    inst.text = U'{}'.format(Opcode.get_name(inst.opcode))
    ctx.stackVM.clear()

    return inst


def handler_end_parse(line):
    # type: (unicode) -> int

    return Opcode.END


def handler_end_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)

    return inst


def handler_assignment_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    fs = ctx.fs
    _unknown1 = fs.read_u32()
    var_type = fs.read_u32()
    _unknown2 = fs.read_u32()
    vt = VariableType(var_type)

    inst = ctx.instruction
    inst.operands = [Operand(_unknown1, 4), Operand(vt, 4), Operand(_unknown2, 4)]
    inst.text = U'{} {} {} {}'.format(Opcode.get_name(inst.opcode), _unknown1, vt.name, _unknown2)
    ctx.stackVM.push(inst)

    return inst


def handler_assignment_parse(line):
    # type: (unicode) -> Tuple[int, int, VariableType, int]
    line_c = line.split(U';', 1)[0].rstrip()  # line with clear comment.
    line_c = remove_dup_space(line_c)
    _, _unknown1, var_type_name, _unknown2 = line_c.split(U' ', 3)
    _unknown1 = str_to_int(_unknown1)
    _unknown2 = str_to_int(_unknown2)
    vt = VariableType.from_type_name(var_type_name)

    return Opcode.ASSIGNMENT, _unknown1, vt, _unknown2


def handler_assignment_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction
    _, _unknown1, vt, _unknown2 = handler_assignment_parse(ctx.line)
    inst.operands = [Operand(_unknown1, 4), Operand(vt, 4), Operand(_unknown2, 4)]

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)
    writer.write_u32(_unknown1)
    writer.write_u32(vt.value)
    writer.write_u32(_unknown2)

    return inst


def handler_unary_expr_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    fs = ctx.fs
    var_type = fs.read_u32()
    op = fs.read_u8()
    vt = VariableType(var_type)
    expr = Expression(Expression.UNARY, op)

    inst = ctx.instruction
    inst.expr = expr
    inst.operands = [Operand(vt, 4)]

    inst.text = U'{} {} {}'.format(Opcode.get_name(inst.opcode), vt.name, expr.expr.name)
    ctx.stackVM.push(inst)

    return inst


def handler_unary_expr_parse(line):
    # type: (unicode) -> Tuple[int, VariableType, Expression]
    line_c = line.split(U';', 1)[0].rstrip()  # line with clear comment.
    line_c = remove_dup_space(line_c)
    _, var_type_name, expr_name = line_c.split(U' ', 2)
    vt = VariableType.from_type_name(var_type_name)

    expr = Expression.from_expr_name(Expression.UNARY, expr_name)

    return Opcode.UNARY_EXPR, vt, expr


def handler_unary_expr_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction
    _, vt, expr = handler_unary_expr_parse(ctx.line)
    inst.expr = expr
    inst.operands = [Operand(vt, 4)]

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)
    writer.write_u32(vt.value)
    writer.write_u8(expr.expr.value)

    return inst


def handler_binary_expr_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    fs = ctx.fs
    type1 = fs.read_u32()
    type2 = fs.read_u32()
    op = fs.read_u8()

    vt1 = VariableType(type1)
    vt2 = VariableType(type2)
    expr = Expression(Expression.BINARY, op)

    inst = ctx.instruction
    inst.expr = expr
    inst.operands = [Operand(vt1, 4), Operand(vt2, 4)]
    inst.text = U'{} {} {} {}'.format(Opcode.get_name(inst.opcode), vt1.name, vt2.name, expr.expr.name)
    ctx.stackVM.push(inst)

    return inst


def handler_binary_expr_parse(line):
    # type: (unicode) -> Tuple[int, VariableType, VariableType, Expression]
    line_c = line.split(U';', 1)[0].rstrip()  # line with clear comment.
    line_c = remove_dup_space(line_c)
    _, var_type_name1, var_type_name2, expr_name = line_c.split(U' ', 3)
    vt1 = VariableType.from_type_name(var_type_name1)
    vt2 = VariableType.from_type_name(var_type_name2)

    expr = Expression.from_expr_name(Expression.BINARY, expr_name)

    return Opcode.BINARY_EXPR, vt1, vt2, expr


def handler_binary_expr_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction

    _, vt1, vt2, expr = handler_binary_expr_parse(ctx.line)
    inst.expr = expr
    inst.operands = [Operand(vt1, 4), Operand(vt2, 4)]

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)
    writer.write_u32(vt1.value)
    writer.write_u32(vt2.value)
    writer.write_u8(expr.expr.value)

    return inst


def check_function_extra(func_id):
    if func_id in [0x0C, 0x12, 0x13, 0x4C, 0x5A, 0x5B, 0x64, 0x7F]:
        return True
    return False


def find_func_id(inst_list):
    # type: (List[Instruction]) -> int
    ret = -1
    ii = len(inst_list)
    jj = 0
    while ii:
        ii -= 1
        opcode = inst_list[ii].opcode
        if opcode in [Opcode.CLOSE_FRAME, Opcode.FUNC_CALL]:
            jj += 1
        elif opcode in [Opcode.OPEN_FRAME, Opcode.DUP_FRAME]:
            if jj == 0:
                break
            else:
                jj -= 1
        elif opcode == Opcode.PUSH:
            var_type = inst_list[ii].operands[0].value.var_type.value
            if var_type == VariableType.INT:
                ret = inst_list[ii].operands[0].value.value
    return ret


def find_user_function_name(stack, current_inst, ss):
    # type: (script.StackFrame, Instruction, script.SSScript) -> unicode

    top_inst = stack.get_value_in_frame()  # push int
    top_inst_value = top_inst.operands[0].value.value
    v_type = top_inst_value >> 24
    v_index = top_inst_value & 0x00FFFFFF
    r_func_name = None
    if v_type == 0x7E:
        # FunctionRef
        if v_index in ss.functions_id_offset:
            r_func_offset = ss.functions_id_offset[v_index]
            if r_func_offset in ss.local_funcs:
                _, r_func_name = ss.local_funcs[r_func_offset]
            elif r_func_offset in ss.global_funcs_info:
                _, r_func_name = ss.global_funcs_info[r_func_offset]
            else:
                r_func_name = U'unk_func_{}'.format(v_index)
        elif v_index in ss.global_ref_func_names:
            r_func_name = ss.global_ref_func_names[v_index]

        # if r_func_name:
        #     current_inst.comment = U'{}()'.format(r_func_name)
        #     top_inst.comment = U'func_id: {}'.format(r_func_name)

    return r_func_name


def handler_function_call_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    fs = ctx.fs
    option = fs.read_u32()
    pos = fs.tell()
    argv = read_argv(fs)
    argv_size = fs.tell() - pos

    num_extra = fs.read_u32()

    extra_params = []
    for i in range(num_extra):
        extra_params.append(fs.read_u32())

    return_type = VariableType(fs.read_u32())

    inst = ctx.instruction
    operands = [Operand(option, 4), Operand(argv, argv_size), Operand(num_extra, 4),
                Operand(extra_params, 4 * num_extra), Operand(return_type, 4)]

    # func_id = find_func_id(ctx.instruction_disassembled)
    top_inst = ctx.stackVM.get_value_in_frame()  # type: Instruction
    if top_inst.opcode != Opcode.PUSH:
        raise ValueError('find func id')

    func_id = top_inst.operands[0].value.value

    func_ex_param = None
    if check_function_extra(func_id):
        func_ex_param = fs.read_u32()
        operands.append(Operand(func_ex_param, 4))

    inst.operands = operands

    argv_name = format_argv(argv)
    find_func_res = ctx.func_def.find_function(ctx.stackVM, option, U'({})'.format(argv_name))
    fn_name = None
    if find_func_res:
        _, _, fn_name, _ = find_func_res

    """
    - rewrite plus:
        push int  ; func_id
        open
        push int  ; element id                         | 
        push int  ; prop list id                       |  argv 1
        push int  ; array (stage mark??), 0xFFFFFFFF   | 
        push int  ; array index                        |
        push str  ; argv 2
        push int  ; argv 3
        call (obj, str, int)
    - angel beats 1st: _ef_macro
        push int  ; func_id
        open      ; |                                               |
        push int  ; |  element id (stage or frame action object)    |
        push int  ; |                                               |
        close     ; |                                               |  argv 1
        push int  ; prop list id                                    |
        push int  ; array (stage mark??), 0xFFFFFFFF                | 
        push int  ; array index                                     |
        push str  ; argv 2
        push int  ; argv 3
        call (obj, str, int)
    """
    if U'Obj' in argv_name and ctx.stackVM.frame_begin:
        ctx.stackVM.close()

    # try get in static function
    if fn_name is None:
        fn_name = find_user_function_name(ctx.stackVM, inst, ctx.ss)

    sig_func_name = fn_name if fn_name else U'UNK'

    inst.text = U'{} {} {} ({}) ({}):{}'.format(Opcode.get_name(inst.opcode), sig_func_name, option, argv_name,
                                                U', '.join([str(i) for i in extra_params][::-1]),
                                                return_type.name)

    if func_ex_param is not None:
        inst.text += U' {}'.format(str(func_ex_param))

    ctx.stackVM.close()
    return inst


def handler_function_call_parse(line):
    # type: (unicode) -> Tuple[int, unicode, int, List[VariableType], int, List[int], VariableType, Optional[int]]
    line_c = line.split(U';', 1)[0].rstrip()  # line with clear comment.
    line_c = remove_dup_space(line_c)
    chunks = get_chunks_from_line(line_c)

    chunk_count = len(chunks)
    func_ex_param = None
    if chunk_count == 6:
        _, fn_name, option, argv_str, ex_params_str, return_type = chunks
    elif chunk_count == 7:
        _, fn_name, option, argv_str, ex_params_str, return_type, func_ex_param = chunks
    else:
        print U'Instruction error in line "{}"'.format(line)
        raise ValueError

    option = str_to_int(option)

    argv, _ = parse_argv(argv_str)
    ex_params = []
    ex_params_str = ex_params_str.strip()[1:-1]
    if len(ex_params_str):
        for p in ex_params_str.split(U','):
            ex_params.append(int(p.strip()))

    num_extra = len(ex_params)
    return_type = VariableType.from_type_name(return_type.strip())

    if chunk_count == 7:
        func_ex_param = str_to_int(func_ex_param)

    return Opcode.FUNC_CALL, fn_name, option, argv, num_extra, ex_params, return_type, func_ex_param


def handler_function_call_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction
    _, fn_name, option, argv, num_extra, ex_params, return_type, func_ex_param = handler_function_call_parse(ctx.line)

    operands = [Operand(option, 4), Operand(argv, None), Operand(num_extra, 4),
                Operand(ex_params, 4 * num_extra), Operand(return_type, 4)]

    if func_ex_param is not None:
        operands.append(Operand(func_ex_param, 4))

        # read_flags_id_list = sorted(ctx.line_read_flags.keys())
        # if len(read_flags_id_list) == 0 or func_ex_param > read_flags_id_list[-1]:
        line_read_flags = ctx.assembler.line_read_flags
        text_id = func_ex_param
        line_code = ctx.assembler.current_line_code
        if text_id in line_read_flags:
            ctx.assembler.line_read_flags[text_id].append((line_code, None))
        else:
            ctx.assembler.line_read_flags[text_id] = [(line_code, None)]

    inst.operands = operands

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)
    writer.write_u32(option)
    write_argv(writer, argv)
    writer.write_u32(num_extra)
    for p in ex_params[::-1]:
        writer.write_u32(p)

    writer.write_u32(return_type.value)
    if func_ex_param is not None:
        writer.write_u32(func_ex_param)

    return inst


def handler_add_text_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    fs = ctx.fs
    text_id = fs.read_u32()

    inst = ctx.instruction
    inst.operands = [Operand(text_id, 4)]
    inst.text = U'{} {}'.format(Opcode.get_name(inst.opcode), text_id)

    ctx.stackVM.push(inst)

    return inst


def handler_add_text_parse(line):
    # type: (unicode) -> Tuple[int, int]
    line_c = line.split(U';', 1)[0].rstrip()  # line with clear comment.
    line_c = remove_dup_space(line_c)
    text_id = line_c.split(U' ')[1]
    if text_id.lower() == U'[id]':
        text_id = -1
    else:
        text_id = str_to_int(text_id)

    return Opcode.TEXT, text_id


def handler_add_text_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction

    _, text_id = handler_add_text_parse(ctx.line)
    inst.operands = [Operand(text_id, 4)]

    prev_inst = ctx.assembler.statements[-1]  # type: Instruction
    v = prev_inst.operands[0].value  # type: Variable
    if prev_inst.opcode != Opcode.PUSH or v.var_type.value != VariableType.STR:
        print '[WARNING] push str not found in line number {} -> skip TEXT instruction!'.format(ctx.line_idx - 1)

        return None
        # print 'Add dummy push string. Line {}!'.format(ctx.line_idx - 1)
        # push_op = Opcode.PUSH
        # push_line = U'{} {} ""'.format(Opcode.get_name(push_op),
        #                                 VariableType.get_type_name(VariableType.STR))
        # push_string_inst = Instruction(push_op)
        # push_string_inst.descriptor = SSOpTable.get_inst_desc(push_op)
        # push_string_inst.text = push_line

        # ctx.instruction = push_string_inst
        # ctx.descriptor = push_string_inst.descriptor

        # current_line = ctx.line
        # ctx.line = push_line
        # push_string_inst = handler_push_asm(ctx)
        # ctx.assembler.statements.append(push_string_inst)

        # ctx.line = current_line
        # ctx.instruction = inst
        # ctx.descriptor = inst.descriptor

        # v = push_string_inst.operands[0].value

    string_idx = v.value
    line_code = ctx.assembler.current_line_code
    line_read_flags = ctx.assembler.line_read_flags
    if text_id in line_read_flags:
        ctx.assembler.line_read_flags[text_id].append((line_code, string_idx))
    else:
        ctx.assembler.line_read_flags[text_id] = [(line_code, string_idx)]

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)
    if text_id == -1:
        ctx.assembler.fix_add_text_id_offset.append(writer.tell())
        text_id = ctx.assembler.current_add_text_id

    writer.write_u32(text_id)
    ctx.assembler.current_add_text_id = text_id

    return inst


def handler_set_name_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    inst = ctx.instruction
    inst.text = U'{}'.format(Opcode.get_name(inst.opcode))
    ctx.stackVM.push(inst)

    return inst


def handler_set_name_parse(line):
    # type: (unicode) -> int

    return Opcode.SET_NAME


def handler_set_name_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction

    prev_inst = ctx.assembler.statements[-1]  # type: Instruction
    v = prev_inst.operands[0].value  # type: Variable
    if prev_inst.opcode != Opcode.PUSH and v.var_type.value != VariableType.STR:
        raise ValueError('Need push string instruction first. Line {}!'.format(ctx.line_idx - 1))

    ctx.assembler.namae_strings_idx.append(v.value)

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)

    return inst


def handler_op_33_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    inst = ctx.instruction
    inst.text = U'{}'.format(Opcode.get_name(inst.opcode))
    ctx.stackVM.push(inst)

    return inst


def handler_op_33_parse(line):
    # type: (unicode) -> int

    return Opcode.OP_33


def handler_op_33_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)

    return inst


def handler_op_34_disasm(ctx):
    # type: (script.DisassemblerHandlerContext) -> Instruction
    inst = ctx.instruction
    inst.text = U'{}'.format(Opcode.get_name(inst.opcode))
    ctx.stackVM.push(inst)

    return inst


def handler_op_34_parse(line):
    # type: (unicode) -> int

    return Opcode.OP_34


def handler_op_34_asm(ctx):
    # type: (script.AssembleHandlerContext) -> Instruction
    inst = ctx.instruction

    writer = ctx.writer
    inst.offset = writer.tell()
    writer.write_u8(inst.opcode)

    return inst


def base_handler(handler_disasm,  # type: Callable[[script.DisassemblerHandlerContext], Instruction]
                 handler_parse,   # type: Callable[[script.ParseHandlerContext], Instruction]
                 handler_asm      # type: Callable[[script.AssembleHandlerContext], Instruction]
                 ):
    def inner(ctx_handle):
        # type: (any) -> Instruction
        if ctx_handle.action == script.Action.Disassemble:
            return handler_disasm(ctx_handle)
        elif ctx_handle.action == script.Action.Parse:
            return handler_parse(ctx_handle)
        elif ctx_handle.action == script.Action.Assemble:
            return handler_asm(ctx_handle)

    return inner


def add_inst(opcode,  # type: int
             handler_disasm,  # type: Callable[[any], Instruction]
             handler_parse,  # type: Callable[[any], any]
             handler_asm  # type: Callable[[any], Instruction]
             ):
    mnemonic = Opcode.get_name(opcode)
    handler = base_handler(handler_disasm, handler_parse, handler_asm)
    return InstructionDescriptor(opcode, mnemonic, handler)


SSOpTable = InstructionTable([
    add_inst(Opcode.LINE,
             handler_line_disasm,
             handler_line_parse,
             handler_line_asm),

    add_inst(Opcode.PUSH,
             handler_push_disasm,
             handler_push_parse,
             handler_push_asm),

    add_inst(Opcode.POP,
             handler_pop_disasm,
             handler_pop_parse,
             handler_pop_asm),

    add_inst(Opcode.DUP_VALUE,
             handler_duplicate_value_disasm,
             handler_duplicate_value_parse,
             handler_duplicate_value_asm),

    add_inst(Opcode.CLOSE_FRAME,
             handler_close_frame_disasm,
             handler_close_frame_parse,
             handler_close_frame_asm),

    add_inst(Opcode.DUP_FRAME,
             handler_duplicate_stack_frame_disasm,
             handler_duplicate_stack_frame_parse,
             handler_duplicate_stack_frame_asm),

    add_inst(Opcode.DECLARE_VAR,
             handler_declare_var_disasm,
             handler_declare_var_parse,
             handler_declare_var_asm),

    add_inst(Opcode.OPEN_FRAME,
             handler_open_frame_disasm,
             handler_open_frame_parse,
             handler_open_frame_asm),

    add_inst(Opcode.PARAMS_END,
             handler_params_end_disasm,
             handler_params_end_parse,
             handler_params_end_asm),

    add_inst(Opcode.JUMP,
             handler_jump_disasm,
             handler_jump_parse,
             handler_jump_asm),

    add_inst(Opcode.JUMP_IF_NOT_ZERO,
             handler_jump_disasm,
             handler_jump_parse,
             handler_jump_asm),

    add_inst(Opcode.JUMP_IF_ZERO,
             handler_jump_disasm,
             handler_jump_parse,
             handler_jump_asm),

    add_inst(Opcode.SHORT_CALL_13,
             handler_short_call_disasm,
             handler_short_call_parse,
             handler_short_call_asm),

    add_inst(Opcode.SHORT_CALL_14,
             handler_short_call_disasm,
             handler_short_call_parse,
             handler_short_call_asm),

    add_inst(Opcode.RETURN,
             handler_return_disasm,
             handler_return_parse,
             handler_return_asm),

    add_inst(Opcode.END,
             handler_end_disasm,
             handler_end_parse,
             handler_end_asm),

    add_inst(Opcode.ASSIGNMENT,
             handler_assignment_disasm,
             handler_assignment_parse,
             handler_assignment_asm),

    add_inst(Opcode.UNARY_EXPR,
             handler_unary_expr_disasm,
             handler_unary_expr_parse,
             handler_unary_expr_asm),

    add_inst(Opcode.BINARY_EXPR,
             handler_binary_expr_disasm,
             handler_binary_expr_parse,
             handler_binary_expr_asm),

    add_inst(Opcode.FUNC_CALL,
             handler_function_call_disasm,
             handler_function_call_parse,
             handler_function_call_asm),

    add_inst(Opcode.TEXT,
             handler_add_text_disasm,
             handler_add_text_parse,
             handler_add_text_asm),

    add_inst(Opcode.SET_NAME,
             handler_set_name_disasm,
             handler_set_name_parse,
             handler_set_name_asm),

    add_inst(Opcode.OP_33,
             handler_op_33_disasm,
             handler_op_33_parse,
             handler_op_33_asm),

    add_inst(Opcode.OP_34,
             handler_op_34_disasm,
             handler_op_34_parse,
             handler_op_34_asm),
])
