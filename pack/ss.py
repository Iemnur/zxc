from shared.common import *
from typing import List, Dict, Tuple, Optional


class SSScript:
    STRING_KEY = 0x7087

    class Header:
        SIZE = 0x84

        def __init__(self, fs):
            self.header_size = fs.read_u32()
            if self.header_size != self.SIZE:
                raise ValueError('Incorrect script format!')

            self.bytecode_index = HeaderPair.load(fs)
            self.string_table = HeaderPair.load(fs)
            self.string_data = HeaderPair.load(fs)

            self.labels = HeaderPair.load(fs)
            self.entrypoints = HeaderPair.load(fs)

            self.function_locations = HeaderPair.load(fs)         # 0x2C: user_cmd_pointer
            self.static_var_types = HeaderPair.load(fs)           # 0x34: user_scn_property_form
            self.static_var_name_table = HeaderPair.load(fs)      # 0x3C: user_scn_property_name
            self.static_var_name_data = HeaderPair.load(fs)

            self.local_func_location = HeaderPair.load(fs)        # 0x4C: user_call_property
            self.local_func_name_table = HeaderPair.load(fs)      # 0x54: user_cmd_name
            self.local_func_name_data = HeaderPair.load(fs)

            self.local_var_name_table = HeaderPair.load(fs)
            self.local_var_name_data = HeaderPair.load(fs)

            self.namae = HeaderPair.load(fs)                      # 0x74: namae
            self.read_flags = HeaderPair.load(fs)                 # 0x7C: read_flag
            pass

    def __init__(self):
        self.fs = None                                   # type: Optional[FileStream]
        self.header = None                               # type: Optional[SSScript.Header]

        # offset
        self.labels = []                                 # type: List[int]
        # offset
        self.entrypoints = []                            # type: List[int]

        # for all local function and global function
        # func_id: offset
        self.functions_id_offset = {}                    # type: Dict[int, int]
        # offset: func_id
        self.functions_offset_id = {}                    # type: Dict[int, int]

        # (var_type, name, length)
        self.static_vars = []                            # type: List[Tuple[int, unicode, int]]
        # func_offset: (func_id, func_name)
        self.local_funcs = {}                            # type: Dict[int, Tuple[int, unicode]]
        self.strings = []                                # type: List[unicode]
        self.local_var_names = []                        # type: List[unicode]
        # string_idx
        self.namae = []                                  # type: List[int]
        # line_no
        self.read_flags = []                             # type: List[int]

        # offset: idx
        self.entrypoints_dict = {}                       # type: Dict[int, int]
        # offset: [idx]
        self.labels_dict = {}                            # type: Dict[int, List[int]]

        self.bytecode = None                             # type: Optional[str]
        self.bytecode_stream = None                      # type: Optional[FileStream]

        # For global data
        # offset: (func_id, func_name)
        self.global_funcs_info = {}                      # type: Dict[int, Tuple[int, unicode]]
        # func_idx: func_name
        self.global_func_names = {}                      # type: Dict[int, unicode]
        # func_idx: func_name
        self.global_ref_func_names = {}                  # type: Dict[int, unicode]

        # var_type_name, var_type, var_length
        self.global_var_types = []                       # type: List[Tuple[int, unicode, int]]
        # var_name
        self.global_var_name = []                        # type: List[unicode]

        self.has_global_function = False
        pass

    def read(self, ss_buff):
        self.fs = FileStream(ss_buff, 'm')
        self.header = self.Header(self.fs)
        self.strings = read_string_with_key(self.fs, self.header.string_table,
                                            self.header.string_data, SSScript.STRING_KEY)
        self.local_var_names = read_strings(self.fs, self.header.local_var_name_table,
                                            self.header.local_var_name_data)

        self.labels = self.read_labels()
        self.entrypoints = self.read_entrypoint()

        self.functions_id_offset, \
        self.functions_offset_id = self.read_functions_id()

        self.static_vars = self.read_static_vars()
        self.local_funcs = self.read_local_funcs()
        self.namae = self.read_namae()
        self.read_flags = self.read_read_flags()

        self.fs.seek(self.header.bytecode_index.offset)
        self.bytecode = self.fs.read(self.header.bytecode_index.count)
        self.bytecode_stream = FileStream(self.bytecode, 'm')

        # Fix function name when it save in pck header.
        for func_id in self.functions_id_offset:
            func_offset = self.functions_id_offset[func_id]
            if func_offset not in self.local_funcs:
                func_name = U'global_func_{}'.format(func_id)
                self.global_funcs_info[func_offset] = (func_id, func_name)
                self.global_func_names[func_id] = func_name

        # Optimize
        for i, entry_offset in enumerate(self.entrypoints):
            self.entrypoints_dict[entry_offset] = i
        for i, label_offset in enumerate(self.labels):
            if label_offset in self.labels_dict:
                self.labels_dict[label_offset].append(i)
            else:
                self.labels_dict[label_offset] = [i]

        self.fs.seek(0)
        return self

    def add_global_func(self, funcs_info, ref_funcs=None):
        # type: (Dict[int, Tuple[int, unicode]], Dict[int, unicode]) -> None

        for func_offset in funcs_info:
            func_id, func_name = funcs_info[func_offset]
            self.global_funcs_info[func_offset] = (func_id, func_name)
            self.global_func_names[func_id] = func_name

        if ref_funcs:
            self.global_ref_func_names = ref_funcs.copy()

        if funcs_info:
            self.has_global_function = True

    def add_global_var_names(self, types, names):
        # type: (List[Tuple[int, unicode, int]], List[unicode]) -> None
        self.global_var_types = [] + types
        self.global_var_name = [] + names

        # add static vars to global vars
        for var_type, name, length in self.static_vars:
            self.global_var_name.append(name)
            self.global_var_types.append((var_type, name, length))

    def read_static_vars(self):
        var_types = []
        local_vars = []

        var_types_count = self.header.static_var_types.count
        self.fs.seek(self.header.static_var_types.offset)
        for i in range(var_types_count):
            var_type = self.fs.read_u32()
            var_length = self.fs.read_u32()
            var_types.append((var_type, var_length))

        var_names = read_strings(self.fs, self.header.static_var_name_table,
                                 self.header.static_var_name_data)

        if len(var_types) != len(var_names):
            raise ValueError('Static variables count mismatch!')

        for i in range(var_types_count):
            var_type, var_length = var_types[i]
            local_vars.append((var_type, var_names[i], var_length))

        return local_vars

    def read_local_funcs(self):
        # type: () -> Dict[int, Tuple[int, unicode]]
        func_locations = []
        local_funcs = {}
        func_locations_count = self.header.local_func_location.count
        self.fs.seek(self.header.local_func_location.offset)
        for i in range(func_locations_count):
            offset = self.fs.read_u32()
            func_locations.append(offset)

        func_names = read_strings(self.fs, self.header.local_func_name_table,
                                  self.header.local_func_name_data)

        if len(func_locations) != len(func_names):
            raise ValueError('Local functions count mismatch!')

        for i in range(func_locations_count):
            offset = func_locations[i]
            local_funcs[offset] = (self.functions_offset_id[offset], func_names[i])

        return local_funcs

    def read_labels(self):
        self.fs.seek(self.header.labels.offset)

        labels = []
        for i in range(self.header.labels.count):
            labels.append(self.fs.read_u32())

        return labels
        pass

    def read_entrypoint(self):
        entrypoints = []
        self.fs.seek(self.header.entrypoints.offset)
        for i in range(self.header.entrypoints.count):
            entrypoints.append(self.fs.read_u32())

        return entrypoints

    def read_functions_id(self):
        self.fs.seek(self.header.function_locations.offset)
        functions_id = {}
        functions_offset = {}

        for i in range(self.header.function_locations.count):
            func_id = self.fs.read_u32()
            func_offset = self.fs.read_u32()
            if func_offset in functions_id:
                print '[WARNING] Duplicate function id to offset: {} - id = {}'.format(func_offset, func_id)

            functions_id[func_id] = func_offset
            functions_offset[func_offset] = func_id

        return functions_id, functions_offset

    def read_namae(self):
        self.fs.seek(self.header.namae.offset)

        return self.fs.read_list('{}I'.format(self.header.namae.count))

    def read_read_flags(self):
        self.fs.seek(self.header.read_flags.offset)

        return self.fs.read_list('{}I'.format(self.header.read_flags.count))

    def dump_strings(self, add_prep=True):
        # type: (bool) -> unicode
        lines = []
        for i, line in enumerate(self.strings):
            line = line.replace(U'\n', U'\\n').replace(U'\r', U'')
            if add_prep:
                lines.extend([
                    U'// <{:04d}> {}'.format(i, line),
                    U'<{:04d}> {}'.format(i, line),
                    U''
                ])
            else:
                lines.append(U'<{:04d}> {}'.format(i, line))

        return U'\r\n'.join(lines)

    def fix_strings(self):
        res = []
        for text in self.strings:
            res.append(text.replace(U'\\n', U'\n'))

        return res

    def to_file(self, ss_out_path):
        strings_tbl_block, strings_data_block = write_string_with_key(self.fix_strings(), SSScript.STRING_KEY)
        label_block = write_int_list(self.labels)
        entrypoints_block = write_int_list(self.entrypoints)

        fs_funcs_id_loc = FileStream(None, 'm')
        for func_id in sorted(self.functions_id_offset):
            func_offset = self.functions_id_offset[func_id]
            fs_funcs_id_loc.write_u32(func_id)
            fs_funcs_id_loc.write_u32(func_offset)

        funcs_id_location_block = fs_funcs_id_loc.get_values()

        fs_static_var_type = FileStream(None, 'm')
        vars_name = []
        for var_type, var_name, var_length in self.static_vars:
            fs_static_var_type.write_u32(var_type)
            fs_static_var_type.write_u32(var_length)
            vars_name.append(var_name)
        static_var_type_block = fs_static_var_type.get_values()
        static_var_name_tbl_block, static_var_name_data_block = write_string(vars_name)

        local_functions_offset = []
        local_functions_name = []
        for func_offset in sorted(self.local_funcs):
            func_id, func_name = self.local_funcs[func_offset]
            local_functions_offset.append(func_offset)
            local_functions_name.append(func_name)

        local_functions_location_block = write_int_list(local_functions_offset)
        local_functions_name_tbl_block, local_functions_name_data_block = write_string(local_functions_name)

        local_var_names_tbl_block, local_var_names_data_block = write_string(self.local_var_names)

        namae_block = write_int_list(self.namae)
        read_flags_block = write_int_list(self.read_flags)

        header_size = self.Header.SIZE
        f_header = FileStream(None, 'm')
        f_data = FileStream(None, 'm')
        f_header.write_u32(header_size)
        f_data.write(strings_tbl_block + strings_data_block)

        # h bytecode
        f_header.write_u32(header_size + f_data.tell())
        f_header.write_u32(len(self.bytecode))
        f_data.write(self.bytecode)

        # h strings
        f_header.write_u32(header_size)
        f_header.write_u32(len(self.strings))

        f_header.write_u32(header_size + len(strings_tbl_block))
        f_header.write_u32(len(self.strings))

        # h labels
        f_header.write_u32(header_size + f_data.tell())
        f_header.write_u32(len(self.labels))
        f_data.write(label_block)

        # h entrypoints
        f_header.write_u32(header_size + f_data.tell())
        f_header.write_u32(len(self.entrypoints))
        f_data.write(entrypoints_block)

        # h func id location
        f_header.write_u32(header_size + f_data.tell())
        f_header.write_u32(len(self.functions_id_offset))
        f_data.write(funcs_id_location_block)

        # h static vars type
        f_header.write_u32(header_size + f_data.tell())
        f_header.write_u32(len(self.static_vars))
        f_data.write(static_var_type_block)

        # static vars name
        f_header.write_u32(header_size + f_data.tell())
        f_header.write_u32(len(self.static_vars))
        f_data.write(static_var_name_tbl_block)

        f_header.write_u32(header_size + f_data.tell())
        f_header.write_u32(len(self.static_vars))
        f_data.write(static_var_name_data_block)

        # h local functions location
        f_header.write_u32(header_size + f_data.tell())
        f_header.write_u32(len(self.local_funcs))
        f_data.write(local_functions_location_block)

        # h local functions name
        f_header.write_u32(header_size + f_data.tell())
        f_header.write_u32(len(self.local_funcs))
        f_data.write(local_functions_name_tbl_block)

        f_header.write_u32(header_size + f_data.tell())
        f_header.write_u32(len(self.local_funcs))
        f_data.write(local_functions_name_data_block)

        # h local vars name
        f_header.write_u32(header_size + f_data.tell())
        f_header.write_u32(len(self.local_var_names))
        f_data.write(local_var_names_tbl_block)

        f_header.write_u32(header_size + f_data.tell())
        f_header.write_u32(len(self.local_var_names))
        f_data.write(local_var_names_data_block)

        # h namae
        f_header.write_u32(header_size + f_data.tell())
        f_header.write_u32(len(self.namae))
        if len(self.namae):
            f_data.write(namae_block)

        # h read flags
        f_header.write_u32(header_size + f_data.tell())
        f_header.write_u32(len(self.read_flags))
        if len(self.read_flags):
            f_data.write(read_flags_block)

        # write ss file
        open(ss_out_path, 'wb').write(f_header.get_values() + f_data.get_values())

        # write global data
        if self.global_funcs_info:
            lines = []
            for func_offset in sorted(self.global_funcs_info,
                                      key=lambda offs: self.global_funcs_info[offs][0]):
                func_id, func_name = self.global_funcs_info[func_offset]
                lines.append(U'{} {} {}'.format(func_id, func_name, func_offset))

            inc_path = U'{}.map'.format(ss_out_path)
            print inc_path
            open(inc_path, 'wb').write(U'\r\n'.join(lines).encode('utf8'))

        pass

    @classmethod
    def from_file(cls, ss_file_path):
        buff = open(ss_file_path, 'rb').read()
        return cls().read(buff)
