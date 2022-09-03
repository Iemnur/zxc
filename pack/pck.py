from shared.common import *
from shared.compress import *
from shared.config import PCKIniConfig
from ss import SSScript
from keys import *


class PCK:
    HEADER_SIZE = 0x5C
    MODE_READ = 'r'
    MODE_WRITE = 'w'
    DEFAULT_GLOBAL_INI_FILE = U'pck.global.ini'

    class Header:
        def __init__(self, fs):
            # type: (FileStream) -> None

            self.header_size = fs.read_u32()
            if self.header_size != PCK.HEADER_SIZE:
                raise ValueError('Incorrect pck format!')

            self.global_var_types = HeaderPair.load(fs)
            self.global_var_name_table = HeaderPair.load(fs)
            self.global_var_name_data = HeaderPair.load(fs)

            self.global_func_location = HeaderPair.load(fs)
            self.global_func_name_table = HeaderPair.load(fs)
            self.global_func_name_data = HeaderPair.load(fs)

            self.scene_name_table = HeaderPair.load(fs)
            self.scene_name_data = HeaderPair.load(fs)

            self.scene_data_table = HeaderPair.load(fs)
            self.scene_data = HeaderPair.load(fs)

            self.xor_level = fs.read_u32()
            self.encrypt_flag = fs.read_s32()

            pass

    def __init__(self, mode):
        # type: (str) -> None

        self.mode = mode
        self.fs = None                        # type: Optional[FileStream]
        self.key16 = None                     # type: Optional[List[int]]
        self.xor_level = 0
        self.encrypt_flag = 0

        self.header = None                    # type: Optional[PCK.Header]

        self.global_var_types = None          # type: Optional[List[Tuple[int, unicode, int]]]
        self.global_var_name = []             # type: List[unicode]

        self.global_func_locations = []       # type: List[Tuple[int, int]]
        self.global_func_names = []           # type: List[unicode]

        # ss_id: {func_offset: (func_id, func_name)}
        self.global_func_info = {}            # type: Dict[int, Dict[int, Tuple[int, unicode]]]

        self.scene_names = []                 # type: List[unicode]
        self.scene_data_table = None          # type: Optional[List[HeaderPair]]

        self.ini = PCKIniConfig()

        pass

    def read(self, file_path, key16=None):
        # type: (str or unicode, List[int]) -> PCK

        if self.mode != self.MODE_READ:
            print "Can't read data when mode={}".format(self.mode)
            raise ValueError

        self.fs = FileStream(file_path, 'rb')
        self.key16 = key16

        self.header = self.Header(self.fs)

        self.xor_level = self.header.xor_level
        self.encrypt_flag = self.header.encrypt_flag

        var_types, var_names = self.read_global_vars()
        self.global_var_types = var_types
        self.global_var_name = var_names

        func_locations, func_names, func_info = self.read_global_funcs()
        self.global_func_locations = func_locations
        self.global_func_names = func_names

        # ss_id: {func_offset: (func_id, func_name)}
        self.global_func_info = func_info  # type: Dict[int, Dict[int, Tuple[int, unicode]]]

        scene_names, scene_data_table = self.read_scene_info()
        self.scene_names = scene_names
        self.scene_data_table = scene_data_table

        return self

    def read_global_vars(self):
        var_types = []
        fs = self.fs
        fs.seek(self.header.global_var_types.offset)
        for i in range(self.header.global_var_types.count):
            var_type, var_length = fs.read_list('2I')
            var_types.append((var_type, VariableType.get_type_name(var_type), var_length))

        var_names = read_strings(fs, self.header.global_var_name_table, self.header.global_var_name_data)
        if len(var_types) != len(var_names):
            raise ValueError('Global variables count mismatch!')

        return var_types, var_names

    def read_global_funcs(self):
        func_locations = []
        fs = self.fs
        fs.seek(self.header.global_func_location.offset)
        for i in range(self.header.global_func_location.count):
            file_index, offset = fs.read_list('2I')
            func_locations.append((file_index, offset))

        func_names = read_strings(fs, self.header.global_func_name_table, self.header.global_func_name_data)
        if len(func_locations) != len(func_names):
            raise ValueError('Global functions count mismatch!')

        func_info = {}
        for func_id, (file_index, offset) in enumerate(func_locations):
            if file_index in func_info:
                func_info[file_index][offset] = (func_id, func_names[func_id])
            else:
                func_info[file_index] = {offset: (func_id, func_names[func_id])}

        return func_locations, func_names, func_info
        pass

    def read_scene_info(self):
        fs = self.fs
        scene_names = read_strings(fs, self.header.scene_name_table, self.header.scene_name_data)
        scene_data_table = []
        fs.seek(self.header.scene_data_table.offset)
        for i in range(self.header.scene_data_table.count):
            scene_data_table.append(HeaderPair.load(fs))

        if len(scene_names) != len(scene_data_table):
            raise ValueError('Scene names and data length mismatch!')

        return scene_names, scene_data_table
        pass

    def get_ss_data(self, ss_idx):
        fs = self.fs
        if ss_idx > len(self.scene_names) - 1:
            raise ValueError('Out of range index ss file!')

        ss_info = self.scene_data_table[ss_idx]
        fs.seek(self.header.scene_data.offset + ss_info.offset)
        str_buff = fs.read(ss_info.count)

        if self.encrypt_flag < 1:
            return str_buff

        buff = []
        for i, c in enumerate(str_buff):
            n = ord(c)
            if self.xor_level:
                if self.key16 is None:
                    raise ValueError('Require key!')
                n = n ^ self.key16[i % 16]

            buff.append(n)

        str_buff = []
        for i, n in enumerate(buff):
            nn = n ^ KEY_256[i % 256]
            str_buff.append(chr(nn))

        str_buff = ''.join(str_buff)

        bfs = FileStream(str_buff, 'm')

        compress_size, decompress_size = bfs.read_list('2I')
        if compress_size != ss_info.count:
            raise ValueError('Expected {} bytes, got {}!'.format(ss_info.count, compress_size))

        data_decompressed = decompress_from_buff(bfs, decompress_size)
        if decompress_size != len(data_decompressed):
            raise ValueError('Decompress size incorrect!')

        return data_decompressed

    def get_ss_info(self, ss_idx):
        ss_data = self.get_ss_data(ss_idx)
        return SSScript().read(ss_data)

    def extract_idx(self, idx_ss_file, out_folder):
        data = self.get_ss_data(idx_ss_file)
        ss_name = self.scene_names[idx_ss_file]
        path_out = '{}/{}.ss'.format(out_folder, ss_name)
        print path_out
        open(path_out, 'wb').write(data)

    def extract_all(self, out_folder):
        for i in range(len(self.scene_names)):
            self.extract_idx(i, out_folder)

    def dump_info(self, ini_out_path):
        ini = PCKIniConfig()
        ini.write_data(ini.FIELD_XOR_LEVEL, self.header.xor_level)
        ini.write_data(ini.FIELD_ENCRYPT_FLAG, self.header.encrypt_flag)
        ini.write_data(ini.LIST_SCENE_NAME, self.scene_names)

        vars_convert = []
        for i, var_name in enumerate(self.global_var_name):
            var_type, _, var_length = self.global_var_types[i]
            vars_convert.append(U'{} {} {}'.format(var_type, var_name, var_length))

        ini.write_data(ini.LIST_VARIABLE, vars_convert)

        funcs_convert = []
        for ss_id in sorted(self.global_func_info):
            ss_name = self.scene_names[ss_id]
            funcs = self.global_func_info[ss_id]
            funcs_convert.append(U'{} {}'.format(ss_name, len(funcs)))
            for func_offset in sorted(funcs, key=lambda offs: funcs[offs][0]):
                func_id, func_name = funcs[func_offset]
                funcs_convert.append(U'{} {} {}'.format(func_id, func_name, func_offset))

        ini.write_data(ini.LIST_FUNCTION, funcs_convert)

        open(ini_out_path, 'wb').write(ini.get_ini_data().encode('utf8'))
        pass

    def __update_ss_func_map(self, ss_folder):
        for ss_id in self.global_func_info:
            map_path = U'{}/{}.ss.map'.format(ss_folder, self.scene_names[ss_id])
            if path_exists(map_path):
                lines = io.StringIO(open(map_path, 'rb').read().decode('utf8')).readlines()
                func_info = self.global_func_info[ss_id]

                for line in lines:
                    line = remove_dup_space(line.strip())
                    if line:
                        func_id, func_name, func_offset = line.split(U' ', 2)
                        func_id = int(func_id)
                        func_offset = int(func_offset)
                        func_info[func_offset] = (func_id, func_name)

    def __update_state(self):
        func_names_dict = {}
        func_location_dict = {}

        for ss_id in self.global_func_info:
            func_info = self.global_func_info[ss_id]
            for func_offset in func_info:
                func_id, func_name = func_info[func_offset]
                func_names_dict[func_id] = func_name
                func_location_dict[func_id] = (ss_id, func_offset)

        i = 0
        for func_id in sorted(func_location_dict):
            if i != func_id:
                print 'Function id mismatched!'
                raise ValueError

            self.global_func_locations.append(func_location_dict[func_id])
            self.global_func_names.append(func_names_dict[func_id])
            i += 1
        pass

    def __load_ini_config(self, ini_path):
        self.ini.read(ini_path)

        self.xor_level = self.ini.xor_level
        self.encrypt_flag = self.ini.encrypt_flag
        self.scene_names = self.ini.scene_names
        self.global_var_types, self.global_var_name = self.ini.variables
        self.global_func_info = self.ini.functions
        pass

    def __encrypt_data(self, data):
        # TODO: xor and compress data here
        raise NotImplemented()
        pass

    def repack_data(self, ss_folder, pck_out, global_ini_path=None, key16=None):
        if self.mode != self.MODE_WRITE:
            print "Can't repack data when mode={}".format(self.mode)
            raise ValueError

        if not global_ini_path:
            global_ini_path = U'{}/{}'.format(ss_folder, self.DEFAULT_GLOBAL_INI_FILE)

        self.key16 = key16
        self.__load_ini_config(global_ini_path)
        self.__update_ss_func_map(ss_folder)
        self.__update_state()

        # vars_type
        fs_vars_type = FileStream(None, 'm')
        for var_type, var_name, var_length in self.global_var_types:
            fs_vars_type.write_u32(var_type)
            fs_vars_type.write_u32(var_length)

        vars_type_block = fs_vars_type.get_values()
        vars_name_table_block, vars_name_data_block = write_string(self.global_var_name)

        # function
        fs_func_locations = FileStream(None, 'm')
        for ss_id, func_offset in self.global_func_locations:
            fs_func_locations.write_u32(ss_id)
            fs_func_locations.write_u32(func_offset)
            pass

        func_locations_block = fs_func_locations.get_values()
        func_names_table_block, func_names_data_block = write_string(self.global_func_names)

        # scene name
        scene_names_table_block, scene_names_data_block = write_string(self.scene_names)

        # pck
        f_head = FileStream(None, 'm')
        f_data = FileStream(None, 'm')

        header_size = PCK.HEADER_SIZE
        f_head.write_u32(header_size)

        # vars type
        f_head.write_u32(header_size)
        f_head.write_u32(len(self.global_var_types))
        f_data.write(vars_type_block)

        # vars name
        f_head.write_u32(header_size + f_data.tell())
        f_head.write_u32(len(self.global_var_name))
        f_data.write(vars_name_table_block)

        f_head.write_u32(header_size + f_data.tell())
        f_head.write_u32(len(self.global_var_name))
        f_data.write(vars_name_data_block)

        # function locations
        f_head.write_u32(header_size + f_data.tell())
        f_head.write_u32(len(self.global_func_locations))
        f_data.write(func_locations_block)

        # function names
        f_head.write_u32(header_size + f_data.tell())
        f_head.write_u32(len(self.global_func_names))
        f_data.write(func_names_table_block)

        f_head.write_u32(header_size + f_data.tell())
        f_head.write_u32(len(self.global_func_names))
        f_data.write(func_names_data_block)

        # scene names
        f_head.write_u32(header_size + f_data.tell())
        f_head.write_u32(len(self.scene_names))
        f_data.write(scene_names_table_block)

        f_head.write_u32(header_size + f_data.tell())
        f_head.write_u32(len(self.scene_names))
        f_data.write(scene_names_data_block)

        # scene data
        f_ss_table = FileStream(None, 'm')
        f_ss_data = FileStream(None, 'm')

        for scene_name in self.scene_names:
            ss_path = U'{}/{}.ss'.format(ss_folder, scene_name)
            print ss_path

            ss_data = open(ss_path, 'rb').read()
            if self.encrypt_flag > 0:
                ss_data = self.__encrypt_data(ss_data)

            f_ss_table.write_u32(f_ss_data.tell())
            f_ss_table.write_u32(len(ss_data))
            f_ss_data.write(ss_data)

        all_ss_data_table_block = f_ss_table.get_values()
        all_ss_data_data_block = f_ss_data.get_values()

        # scene data table
        f_head.write_u32(header_size + f_data.tell())
        f_head.write_u32(len(self.scene_names))
        f_data.write(all_ss_data_table_block)

        # scene data
        f_head.write_u32(header_size + f_data.tell())
        f_head.write_u32(len(self.scene_names))
        f_data.write(all_ss_data_data_block)

        # xor level
        f_head.write_u32(self.xor_level)

        # encrypt flags
        f_head.write_s32(self.encrypt_flag)

        # write pck
        print pck_out
        open(pck_out, 'wb').write(f_head.get_values() + f_data.get_values())
        pass
