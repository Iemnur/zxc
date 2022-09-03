import os
from handler import *
from bytecode import SSOpTable
from funcdef import FunctionDef
from shared.config import SSIniConfig
from shared.common import *


class Disassembler:

    DEFAULT_RESOURCE_FOLDER = U'resources'

    def __init__(self, pck_file_path, key16=None, func_def_path=None, resource_out_folder=None):
        # type: (str or unicode, list, unicode, unicode) -> None

        self.pck = PCK('r').read(pck_file_path, key16)
        self.inst_table = SSOpTable
        self.inst_disassembled = []  # type: List[Instruction]
        self.inst_disassembled_offset = {}  # type: Dict[int, Instruction]
        self.fs = None
        self.inst_text = []
        self.resource_out_folder = self.DEFAULT_RESOURCE_FOLDER
        self.func_def = FunctionDef()

        if func_def_path:
            self.func_def.load(func_def_path)

        if resource_out_folder:
            self.resource_out_folder = full_path(resource_out_folder)

        pass

    def __pre_handler_inst(self, ctx):
        # type: (DisassemblerHandlerContext) -> None

        pos = ctx.offset
        ss = ctx.ss
        if pos == 0:
            self.inst_text = []
            self.inst_text.append(U'; Start:')

        if pos > 0 and pos in ss.entrypoints_dict:
            self.inst_text.append(U'')
            self.inst_text.append(U'#Z{:02d}:'.format(ss.entrypoints_dict[pos]))
            ctx.stackVM.clear_local_var()

        if pos in ss.labels_dict:
            for lb_idx in ss.labels_dict[pos]:
                self.inst_text.append(U'LABEL_{}:'.format(lb_idx))

        if ctx.ss_idx in self.pck.global_func_info and \
                pos in self.pck.global_func_info[ctx.ss_idx]:
            func_id, func_name = self.pck.global_func_info[ctx.ss_idx][pos]
            self.inst_text.append(U'')
            self.inst_text.append(U'global function {}:'.format(func_name))
            ctx.stackVM.clear_local_var()
        elif pos in ss.local_funcs:
            func_id, func_name = ss.local_funcs[pos]
            self.inst_text.append(U'')
            self.inst_text.append(U'function {}:'.format(func_name))
            ctx.stackVM.clear_local_var()
        pass

    def __post_handler_inst(self, ctx, debug=True):
        # type: (DisassemblerHandlerContext, bool) -> None

        inst_text = ctx.instruction.text
        inst_comment = ctx.instruction.comment
        if inst_text is not None:
            if debug:
                inst_text = U'0x{:08X}   {}'.format(ctx.offset, inst_text)

            if inst_comment is not None:
                inst_comment = inst_comment.replace(U'\n', U'\\n').replace(U'\r', U'')
                inst_text = U'{} ; {}'.format(inst_text, inst_comment)

            self.inst_text.append(inst_text)

    def __update_global_data(self, ss, ss_idx):
        # type: (SSScript, int) -> SSScript
        ss.add_global_var_names(self.pck.global_var_types, self.pck.global_var_name)
        global_func_locations_info = {}
        global_ref_func_names = {func_id: func_name
                                 for func_id, func_name in enumerate(self.pck.global_func_names)}
        if ss_idx in self.pck.global_func_info:
            global_func_locations_info = self.pck.global_func_info[ss_idx]  # type: Dict[int, Tuple[int, unicode]]
            for func_offset in global_func_locations_info:
                func_id, func_name = global_func_locations_info[func_offset]
                global_ref_func_names.pop(func_id)

        ss.add_global_func(global_func_locations_info, global_ref_func_names)

        return ss

    def __dump_resources(self, ss, ss_idx):
        # type: (SSScript, int) -> tuple

        ini = SSIniConfig()
        ini.set_section_write(SSIniConfig.SECTION_LOCAL)
        ini.write_data(SSIniConfig.FIELD_LABEL_COUNT, len(ss.labels))
        ini.write_data(SSIniConfig.FIELD_ENTRY_COUNT, len(ss.entrypoints))

        if len(ss.functions_id_offset):
            local_funcs = []
            for func_idx in sorted(ss.functions_id_offset):
                func_offset = ss.functions_id_offset[func_idx]
                func_id, func_name = ss.local_funcs.get(func_offset) or (None, None)
                if func_name is None and func_offset not in ss.global_funcs_info:
                    raise ValueError('Unk function name!')

                if func_name:
                    local_funcs.append(U'{} {}'.format(func_idx, func_name))

            if local_funcs:
                ini.write_data(SSIniConfig.LIST_LOCAL_FUNC, local_funcs)

        if len(ss.static_vars):
            static_vars = []
            for var_type, var_name, var_length in ss.static_vars:
                static_vars.append(U'{} {} {}'.format(var_type, var_name, var_length))
            ini.write_data(SSIniConfig.LIST_STATIC_VARS, static_vars)

        if len(ss.local_var_names):
            ini.write_data(SSIniConfig.LIST_LOCAL_VAR_NAMES, ss.local_var_names)

        if ss_idx in self.pck.global_func_info:
            global_funcs = []
            ini.set_section_write(SSIniConfig.SECTION_GLOBAL)
            funcs_info = self.pck.global_func_info[ss_idx]
            for func_offset in sorted(funcs_info,
                                      key=lambda offs: funcs_info[offs][0]):
                func_id, func_name = funcs_info[func_offset]
                global_funcs.append(U'{} {}'.format(func_id, func_name))
            ini.write_data(SSIniConfig.LIST_GLOBAL_FUNCTION, global_funcs)

        return ini.get_ini_data(), ss.dump_strings()

    def disassembler_ss_idx(self, ss_idx):
        # type: (int) -> Tuple[unicode, unicode, unicode]

        # ss_path = U'data/script/{}.ss'.format(self.pck.scene_names[ss_idx])
        # ss = SSScript.from_file(ss_path)
        # self.__update_global_data(ss, ss_idx)

        ss = self.pck.get_ss_info(ss_idx)
        self.__update_global_data(ss, ss_idx)
        ss.fs.seek(ss.header.bytecode_index.offset)
        bytecode_size = ss.header.bytecode_index.count
        bytecode = ss.fs.read(bytecode_size)

        self.fs = FileStream(bytecode, 'm')
        self.inst_disassembled = []
        self.inst_disassembled_offset = {}
        handler_ctx = DisassemblerHandlerContext()
        handler_ctx.ss = ss
        handler_ctx.pck = self.pck
        handler_ctx.ss_idx = ss_idx
        handler_ctx.instructionTable = self.inst_table
        handler_ctx.fs = self.fs
        handler_ctx.instruction_disassembled = self.inst_disassembled
        handler_ctx.stackVM = StackInstructionVM()
        handler_ctx.func_def = self.func_def

        while True:
            pos = self.fs.tell()
            if pos >= bytecode_size:
                break

            opcode = self.inst_table.read_opcode(self.fs)
            desc = self.inst_table.get_inst_desc(opcode)

            inst = Instruction(opcode)
            inst.offset = pos
            inst.descriptor = desc

            handler_ctx.offset = pos
            handler_ctx.instruction = inst
            handler_ctx.descriptor = desc

            self.__pre_handler_inst(handler_ctx)

            inst = desc.handler(handler_ctx)
            inst.size = self.fs.tell() - pos

            self.inst_disassembled.append(inst)
            # self.inst_disassembled_offset[pos] = inst

            self.__post_handler_inst(handler_ctx)
            # handler_ctx.stackVM.run(pos, ss, inst)

        ss_ini, ss_strings = self.__dump_resources(ss, ss_idx)

        if ss_ini or ss_strings:
            i = 0
            if ss_ini:
                self.inst_text.insert(i, U'include ini "{}/{}.ini"'
                                      .format(self.resource_out_folder, self.pck.scene_names[ss_idx]))
                i += 1

            if ss_strings:
                self.inst_text.insert(i, U'include strings "{}/{}.strings.txt"'
                                      .format(self.resource_out_folder, self.pck.scene_names[ss_idx]))
                i += 1

            self.inst_text.insert(i, U'')

        return U'\r\n'.join(self.inst_text), ss_ini, ss_strings

    def disassembler_all_file(self, out_folder):
        if self.resource_out_folder == self.DEFAULT_RESOURCE_FOLDER:
            resources_out_path = U'{}/{}'.format(out_folder, self.DEFAULT_RESOURCE_FOLDER)
        else:
            resources_out_path = self.resource_out_folder

        make_dirs(resources_out_path)

        for i, f_name in enumerate(self.pck.scene_names):
            asm_out_path = U'{}/{}.ss.asm'.format(out_folder, f_name)
            print asm_out_path
            asm_text, ss_ini, ss_strings = self.disassembler_ss_idx(i)

            open(asm_out_path, 'wb').write(asm_text.encode('utf8'))
            open(U'{}/{}.ini'.format(resources_out_path, f_name), 'wb').write(ss_ini.encode('utf8'))
            open(U'{}/{}.strings.txt'.format(resources_out_path, f_name), 'wb').write(ss_strings.encode('utf8'))

        global_ini_path = U'{}/{}'.format(resources_out_path, self.pck.DEFAULT_GLOBAL_INI_FILE)
        print 'Dump global data!'
        print global_ini_path
        self.pck.dump_info(global_ini_path)
        pass
