import codecs
import io
from handler import *
from bytecode import SSOpTable, Opcode
from typing import List, Dict, Tuple
from marco import ScriptMacros
from shared.config import SSIniConfig
from shared.common import remove_dup_space


class Assembler:
    def __init__(self):
        self.inst_table = SSOpTable
        self.strings = []                              # type: List[unicode]
        self.ini = SSIniConfig()
        self.labels_offset = []                        # type: List[Tuple[int, unicode]]
        self.label_statements = {}                     # type: Dict[unicode, Label]
        # entry_idx: entry
        self.entrypoints = {}                          # type: Dict[int, Entrypoint]

        # func_offset: func
        self.functions = {}                            # type: Dict[int, Function]
        self.instructions = []                         # type: List[Instruction]
        self.statements = []
        self.bytecode_writer = FileStream(None, 'm')
        # add_text_id: [(line_code, string_id)]
        self.line_read_flags = {}                      # type: Dict[int, List[Tuple[int, Optional[int]]]]
        self.namae_strings_idx = []                    # type: List[int]
        self.current_line_code = 0
        self.current_add_text_id = 0
        self.fix_add_text_id_offset = []
        self._macro = ScriptMacros()
        self._cwd = U'./'
        pass

    def execute(self, buff):
        # type: (str) -> Assembler
        lines = io.StringIO(buff.decode('utf8')).readlines()

        self.assembler_lines(lines)
        self._resolve_label()

        return self

    @property
    def cwd(self):
        return self._cwd

    @cwd.setter
    def cwd(self, value):
        # type: (unicode) -> None
        self._cwd = value

    @classmethod
    def from_file(cls, asm_file_path):
        # type: (str or unicode) -> Assembler

        buff = open(asm_file_path, 'rb').read()
        cwd_arr = asm_file_path.replace('\\', '/').split('/')[:-1]
        assembler = cls()
        assembler.cwd = '/'.join(cwd_arr)
        return assembler.execute(buff)

    @staticmethod
    def load_strings_db(strings_path):
        strings_dict = {}
        lines = codecs.open(strings_path, 'rb', encoding='utf8').readlines()
        for i, line in enumerate(lines):
            line = line.lstrip().rstrip(U'\r\n').split(U'//', 1)[0]
            if line.startswith(U'<'):
                end_tag = line.find(U'>')
                if end_tag == -1:
                    print 'Read string db error, end tag ">" not found in line {}'.format(i + 1)
                    raise ValueError

                string_id = int(line[1:end_tag])
                string_value = line[end_tag + 1:]
                if len(string_value) > 0 and string_value[0] == U' ':
                    # Skip first space
                    string_value = string_value[1:]

                if string_id not in strings_dict:
                    strings_dict[string_id] = string_value
                else:
                    print '[WARNING] Duplicate string id in line {}'.format(i + 1)
            elif line.strip() != U'':
                print '[WARNING] Skip line {}'.format(i + 1)

        # convert to list
        string_list = []
        for string_id in sorted(strings_dict):
            value = strings_dict[string_id]
            list_size = len(string_list)
            if string_id != list_size:
                string_list.extend([U''] * (string_id - list_size))

            string_list.append(value)

        return string_list

    def get_macro_name_by_alias(self, alias_name):
        return self._macro.get_name_by_alias(alias_name)

    def execute_macro(self, line, alias_name=False):
        line = line[1:]
        macro_name = line.strip()
        argv_str = U''
        operands = line.split(U' ', 1)
        if len(operands) == 2:
            macro_name, argv_str = operands

        if alias_name:
            macro_name = self._macro.get_name_by_alias(macro_name)
            if macro_name is None:
                return False

        argv = []
        i = 0
        v = []
        while i < len(argv_str):
            c = argv_str[i]
            if c == U',':
                argv.append(U''.join(v))
            elif c == U'"':
                i += 1
                v = [c]
                while i < len(argv_str):
                    c = argv_str[i]
                    if c == U'\\' and i + 1 < len(argv_str):
                        next_c = argv_str[i+1]
                        if next_c == U'"':
                            i += 1
                            v.append(c)
                            v.append(next_c)
                        else:
                            v.append(c)
                    elif c == U'"':
                        v.append(c)
                        i += 1
                        break
                    else:
                        v.append(c)

                    i += 1
            else:
                if c != U' ':
                    v.append(c)

            i += 1

        if len(v):
            argv.append(U''.join(v))

        self._macro.execute(macro_name, argv, self.assembler_lines)
        return True

    def assembler_lines(self, lines):
        # type: (List[unicode]) -> Assembler

        for line_idx, line in enumerate(lines):
            line = line.strip()
            if line.startswith(U'0x'):
                line = line.split(U' ', 1)[1].strip()

            line_c = remove_dup_space(line.split(U';', 1)[0].rstrip())  # line with clear comment + duplicate space.
            if not line_c:
                continue

            if line[:2].upper() == U'#Z':
                entry_idx = int(line_c[2:-1])
                entry = Entrypoint(entry_idx, line_c[:-1], self.bytecode_writer.tell())
                self.statements.append(entry)
                self.entrypoints[entry_idx] = entry
            elif line.startswith(U'include'):
                _, inc_type, inc_value = line_c.split(U' ', 2)
                start_pos = inc_value.find(U'"')
                end_pos = inc_value.rfind(U'"')
                inc_path = U'{}/{}'.format(self.cwd, inc_value[start_pos+1:end_pos])

                if inc_type == U'macro':
                    self._macro.load(inc_path)
                elif inc_type == U'ini':
                    self.ini.read(inc_path)
                elif inc_type == U'strings':
                    self.strings = self.load_strings_db(inc_path)
                else:
                    print U'Unknown include type "{}"'.format(inc_type)
                    raise ValueError

            elif line[0] == U'@':
                self.execute_macro(line)
            elif line.startswith(U'global function'):
                g_func_name = line_c.split(U'global function', 1)[1][:-1].strip()
                g_func_offset = self.bytecode_writer.tell()
                g_func = Function(None, g_func_name, g_func_offset, FunctionType.GLOBAL)
                self.statements.append(g_func)
                self.functions[g_func_offset] = g_func
            elif line.startswith(U'function'):
                func_name = line_c.split(U'function', 1)[1][:-1].strip()
                func_offset = self.bytecode_writer.tell()
                func = Function(None, func_name, func_offset, FunctionType.STATIC)
                self.statements.append(func)
                self.functions[func_offset] = func
            else:
                mnemonic = line.split(U' ', 1)[0].upper()
                opcode = Opcode.get_opcode(mnemonic)
                if opcode is not None:
                    desc = self.inst_table.get_inst_desc(opcode)
                    inst = Instruction(opcode)
                    inst.descriptor = desc
                    inst.text = line

                    handler_ctx = AssembleHandlerContext(line_idx + 1, line)
                    handler_ctx.instruction = inst
                    handler_ctx.descriptor = desc
                    handler_ctx.strings = self.strings
                    handler_ctx.ini = self.ini
                    handler_ctx.labels_offset = self.labels_offset
                    handler_ctx.writer = self.bytecode_writer
                    handler_ctx.assembler = self

                    inst = desc.handler(handler_ctx)

                    if inst:
                        self.statements.append(inst)
                else:
                    if line_c[-1] == U':' and line_c.find(U' ') == -1:
                        lb_name = line_c[:-1]
                        lb = Label(None, lb_name, self.bytecode_writer.tell())
                        self.statements.append(lb)
                        self.label_statements[lb_name] = lb
                    elif line_c != U'':
                        print U'Skip line {}'.format(line_idx + 1)

        return self

    def _resolve_label(self):
        idx_labels = {}
        idx = 0

        def get_empty_idx():
            ii = idx
            while True:
                if ii not in idx_labels:
                    return ii
                ii += 1

        # Resolve label index in bytecode
        for lb_pos, lb_name in self.labels_offset:
            lb = self.label_statements[lb_name]
            if lb_name.upper().startswith(U'LABEL_'):
                lb_idx = int(lb_name.split(U'_', 1)[1])
                if lb_idx in idx_labels and idx_labels[lb_idx] != lb_name:
                    prev_lb_name = idx_labels[lb_idx]
                    fix_idx = get_empty_idx()
                    idx_labels[fix_idx] = prev_lb_name
                    idx = fix_idx + 1
                idx_labels[lb_idx] = lb_name
            else:
                lb_idx = get_empty_idx()
                idx_labels[lb_idx] = lb.name
                idx = lb_idx + 1

            self.bytecode_writer.seek(lb_pos)
            self.bytecode_writer.write_u32(lb_idx)

        # Update label index for ss header
        idx_labels_rev = {v.upper(): k for k, v in idx_labels.iteritems()}
        for lb_name in self.label_statements:
            if lb_name in idx_labels_rev:
                self.label_statements[lb_name].idx = idx_labels_rev[lb_name]
            else:
                lb_idx = get_empty_idx()
                self.label_statements[lb_name].idx = lb_idx
                idx = lb_idx + 1

        pass

    def _process_entrypoint(self):
        if self.ini.entry_count:
            entrypoints_result = [0] * self.ini.entry_count
        else:
            entrypoints_result = [0] * 1000

        for entry_offset in self.entrypoints:
            entry = self.entrypoints[entry_offset]
            if entry.idx >= 0 and entry.offset >= 0:
                entrypoints_result[entry.idx] = entry.offset

        return entrypoints_result

    def _process_labels(self):
        labels_result = []

        for lb_name, lb in sorted(self.label_statements.items(), key=lambda v: v[1].idx):
            if len(labels_result) != lb.idx:
                labels_result.extend([0] * (lb.idx - len(labels_result)))

            labels_result.append(lb.offset)

        return labels_result

    def _process_function(self):
        if self.functions and not (self.ini.local_function or self.ini.global_func):
            print 'Require define function from ini file!'
            raise ValueError

        # func_id: offset
        functions_index = {}                  # type: Dict[int, int]
        # func_offset: func_name
        local_funcs = {}                     # type: Dict[int, Tuple[int, unicode]]
        # func_offset: (func_idx, func_name)
        global_funcs = {}                     # type: Dict[int, Tuple[int, unicode]]
        for func_offset in self.functions:
            func = self.functions[func_offset]

            # != global function -> save it
            if func.type != FunctionType.GLOBAL:
                func_id = self.ini.local_function[func.name]
                local_funcs[func.offset] = (func_id, func.name)
            else:
                func_id = self.ini.global_func[func.name]
                global_funcs[func_offset] = (func_id, func.name)

            func.idx = func_id
            functions_index[func_id] = func.offset

        return functions_index, local_funcs, global_funcs

    def _process_static_vars(self):
        return self.ini.static_vars

    def _process_local_vars_name(self):
        if self.ini.local_var_names:
            return self.ini.local_var_names

        return []

    def _process_namae(self):
        return self.namae_strings_idx
        pass

    def _process_read_flags(self):
        res = []

        idx = 0
        for add_text_id in sorted(self.line_read_flags):
            if add_text_id == -1:
                continue

            line_code, string_idx = self.line_read_flags[add_text_id][0]
            while idx < add_text_id + 1:
                res.append(line_code)
                idx += 1

        if len(self.fix_add_text_id_offset):
            fix_id = idx + 5  # padding id = 5
            current_pos = self.bytecode_writer.tell()
            for i, offset in enumerate(self.fix_add_text_id_offset):
                line_code, string_idx = self.line_read_flags[-1][i]
                while idx < fix_id + 1:
                    res.append(line_code)
                    idx += 1
                self.bytecode_writer.seek(offset)
                self.bytecode_writer.write_u32(fix_id)
                fix_id += 1

            self.bytecode_writer.seek(current_pos)

        return res

    def to_file(self, ss_out_path):
        # type: (str or unicode) -> SSScript

        ss = SSScript()
        ss.strings = self.strings
        ss.entrypoints = self._process_entrypoint()
        ss.labels = self._process_labels()
        ss.static_vars = self._process_static_vars()
        ss.local_var_names = self._process_local_vars_name()
        ss.namae = self._process_namae()
        ss.read_flags = self._process_read_flags()

        functions_id, local_funcs, global_funcs = self._process_function()
        ss.functions_id_offset = functions_id
        ss.local_funcs = local_funcs

        if global_funcs:
            ss.add_global_func(global_funcs)

        ss.bytecode = self.bytecode_writer.get_values()
        ss.to_file(ss_out_path)

        return ss

