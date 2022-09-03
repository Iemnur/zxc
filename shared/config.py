from common import *


class MyIniConfig(object):

    SECTION_TAG = U'@'
    FIELD_TAG = U'#'
    LIST_NAME_BEGIN_TAG = U'['
    LIST_NAME_END_TAG = U']'
    END_TAG = U'[END]'

    def __init__(self):
        self._sections = {}
        self.section_write = None
        pass

    def _read_field(self, line):
        # type: (unicode) -> (unicode, unicode)
        key_name, value = line.split(U'=', 1)
        key_name = key_name[1:]  # remove '#' tag

        return key_name, value
        pass

    def _read_list(self, fi):
        # type: (io.StringIO) -> list
        res = []
        while True:
            line = fi.readline()
            if line == U'':
                break

            line = line.strip()
            if line.upper() == self.END_TAG:
                break

            res.append(line)

        return res

    def _read_section(self, fi, section_name):
        # type: (io.StringIO, unicode) -> None

        section = {}

        while True:
            pos = fi.tell()
            line = fi.readline()
            if line == U'':
                break
            line = line.split(U'//', 1)[0].strip()

            if line.startswith(self.FIELD_TAG):
                key_name, value = self._read_field(line)
                section[key_name] = value
            elif line.startswith(self.LIST_NAME_BEGIN_TAG) and line.endswith(self.LIST_NAME_END_TAG):
                key_name = line[1:-1]
                value = self._read_list(fi)
                section[key_name] = value
            elif line.startswith(self.SECTION_TAG):
                fi.seek(pos)
                break

        self._sections[section_name] = section

    def read(self, ini_path):
        # type: (str or unicode) -> MyIniConfig

        fi = io.StringIO(open(ini_path, 'rb').read().decode('utf8'))
        while True:
            line = fi.readline()
            if line == U'':
                break

            line = line.split(U'//', 1)[0].strip().upper()

            if line[0] == U'@':
                section_name = line[1:]
                if section_name not in self._sections:
                    self._sections[section_name] = {}
                self._read_section(fi, section_name)

        return self

    def get_data(self, section_name, key):
        section = self._sections.get(section_name)
        if section:
            return section.get(key)

        return None

    def set_section_write(self, section_type):
        self.section_write = section_type

    def _write(self, section_name, key_name, value):

        if section_name not in self._sections:
            self._sections[section_name] = {}

        self._sections[section_name][key_name] = value
        pass

    def write_data(self, key_name, value):

        if self.section_write is None:
            print 'Need set section for writer!'
            raise ValueError

        self._write(self.section_write, key_name, value)
        pass

    def get_ini_data(self):
        fo = io.StringIO()

        def write_data(dict_section):
            for key_name in sorted(dict_section,
                                   key=lambda kn: 2 if isinstance(dict_section[kn], (list, tuple)) else 1):
                value = dict_section[key_name]
                if isinstance(value, (list, tuple)):
                    fo.write(U'[{}]\r\n'.format(key_name))
                    for item in value:
                        fo.write(U'{}\r\n'.format(item))
                    fo.write(U'{}\r\n'.format(self.END_TAG))
                else:
                    fo.write(U'#{}={}\r\n'.format(key_name, value))

        for section_name in sorted(self._sections):
            section = self._sections[section_name]
            if section:
                fo.write(U'@{}\r\n'.format(section_name))
                write_data(section)
                fo.write(U'\r\n')

        return fo.getvalue()

    def to_file(self, file_path):
        fo = open(file_path, 'wb')
        fo.write(self.get_ini_data().encode('utf8'))
        fo.close()
        pass


class SSIniConfig(MyIniConfig):

    SECTION_LOCAL = U'LOCAL'
    SECTION_GLOBAL = U'GLOBAL'
    FIELD_LABEL_COUNT = U'LABEL_COUNT'
    FIELD_ENTRY_COUNT = U'ENTRY_COUNT'
    LIST_LOCAL_FUNC = U'LOCAL_FUNC'
    LIST_STATIC_VARS = U'STATIC_VARS'
    LIST_LOCAL_VAR_NAMES = U'LOCAL_VAR_NAMES'
    LIST_GLOBAL_FUNCTION = U'GLOBAL_FUNC'

    def __init__(self):
        super(SSIniConfig, self).__init__()
        self._sections[self.SECTION_LOCAL] = {}
        self._sections[self.SECTION_GLOBAL] = {}
        pass

    @property
    def _local(self):
        return self._sections[self.SECTION_LOCAL]

    @property
    def _global(self):
        return self._sections[self.SECTION_GLOBAL]

    @property
    def label_count(self):
        value = self._local.get(self.FIELD_LABEL_COUNT)
        return int(value) if value else None

    @property
    def entry_count(self):
        value = self._local.get(self.FIELD_ENTRY_COUNT)
        return int(value) if value else None

    @property
    def local_function(self):
        res = {}

        list_value = self._local.get(self.LIST_LOCAL_FUNC)
        if list_value:
            for func in list_value:
                func_idx, func_name = func.split(U' ', 1)
                func_idx = int(func_idx)
                res[func_name] = func_idx

        return res

    @property
    def static_vars(self):
        res = []

        list_value = self._local.get(self.LIST_STATIC_VARS)
        if list_value:
            for var_info in list_value:
                var_type, var_name, var_length = var_info.split(U' ', 2)

                var_type = int(var_type)
                var_length = int(var_length)

                res.append((var_type, var_name, var_length))

        return res

    @property
    def local_var_names(self):
        return self._local.get(self.LIST_LOCAL_VAR_NAMES) or []

    @property
    def global_func(self):
        res = {}

        list_value = self._global.get(self.LIST_GLOBAL_FUNCTION)
        if list_value:
            for func in list_value:
                func_idx, func_name = func.split(U' ', 1)
                func_idx = int(func_idx)
                res[func_name] = func_idx

        return res


class PCKIniConfig(MyIniConfig):

    SECTION_GLOBAL = U'GLOBAL'
    FIELD_XOR_LEVEL = U'XOR_LEVEL'
    FIELD_ENCRYPT_FLAG = U'ENCRYPT_FLAG'
    LIST_VARIABLE = U'VARIABLES'
    LIST_FUNCTION = U'FUNCTIONS'
    LIST_SCENE_NAME = U'SCENE_NAMES'

    def __init__(self):
        super(PCKIniConfig, self).__init__()
        self._sections[self.SECTION_GLOBAL] = {}
        self.section_write = self.SECTION_GLOBAL
        pass

    @property
    def _global(self):
        return self._sections[self.SECTION_GLOBAL]

    @property
    def xor_level(self):
        value = self._global.get(self.FIELD_XOR_LEVEL)
        return int(value)

    @property
    def encrypt_flag(self):
        value = self._global.get(self.FIELD_ENCRYPT_FLAG)
        return int(value)

    @property
    def variables(self):
        # type: () -> Tuple[List[Tuple[int, unicode, int]], List[unicode]]
        list_value = self._global.get(self.LIST_VARIABLE)
        var_types = []
        var_names = []

        for item in list_value:
            var_type, var_name, var_length = item.split(U' ', 2)
            var_type = int(var_type)
            var_length = int(var_length)
            var_types.append((var_type, VariableType.get_type_name(var_type), var_length))
            var_names.append(var_name)

        return var_types, var_names

    @property
    def functions(self):
        # type: () -> Dict[int, Dict[int, Tuple[int, unicode]]]
        list_value = self._global.get(self.LIST_FUNCTION)
        res = {}

        i = 0
        while i < len(list_value):
            item = list_value[i]
            if item.strip():
                sce_name, func_count = item.split(U' ', 1)
                sce_name = sce_name.strip()
                ss_idx = self.scene_names.index(sce_name)
                func_count = int(func_count)
                funcs_info = {}
                while func_count:
                    i += 1
                    item = remove_dup_space(list_value[i])
                    func_id, func_name, func_offset = item.split(U' ', 2)
                    func_id = int(func_id)
                    func_offset = int(func_offset)
                    funcs_info[func_offset] = (func_id, func_name)
                    func_count -= 1
                    pass

                res[ss_idx] = funcs_info

            i += 1

        return res

    @property
    def scene_names(self):
        # type: () -> List[unicode]
        res = []
        values = self._global.get(self.LIST_SCENE_NAME)
        if values:
            for name in values:
                res.append(name.strip())
        return res
