import io
import os
import struct
import codecs
import json
from types import *
from filestream import FileStream
from typing import List, Tuple, Dict, Optional, Callable


def path_exists(path):
    return os.path.exists(path)


def make_dirs(path):
    if not path_exists(path):
        os.makedirs(path)


def is_folder(path):
    return os.path.isdir(path)
    pass


def is_file(path):
    return os.path.isfile(path)
    pass


def get_filename(path, has_ext=True):
    res = os.path.basename(path)
    if not has_ext:
        res = res.split('.', 1)[0]
    return res


def get_cwd():
    return os.getcwd()


def full_path(relative_path):
    return os.path.abspath(relative_path)


def str_to_int(value):
    # type: (unicode) -> int
    v = value.lower()
    if v.startswith(U'0x'):
        return int(v, 16)
    elif v[-1] == U'h':
        return int(v[:-1], 16)
    elif v[-1] == U'd':
        return int(v[:-1], 10)
    else:
        return int(v, 0)


def read_strings(fs, idx_table, data_table):
    # type: (FileStream, HeaderPair, HeaderPair) -> list

    res = []
    if idx_table.count != data_table.count:
        raise ValueError('Index and string data length mismatch.')

    fs.seek(idx_table.offset)
    str_idx_info = []
    for i in range(idx_table.count):
        str_idx_info.append(HeaderPair.load(fs))

    for i in range(data_table.count):
        str_offset = data_table.offset + (str_idx_info[i].offset * 2)
        str_size = str_idx_info[i].count
        fs.seek(str_offset)

        str_value = fs.read(str_size * 2)
        res.append(str_value.decode('utf-16-le'))

    return res


def read_string_with_key(fs, idx_table, data_table, key):
    # type: (FileStream, HeaderPair, HeaderPair, int) -> list

    res = []
    if idx_table.count != data_table.count:
        raise ValueError('Index and string data length mismatch!')

    fs.seek(idx_table.offset)
    str_idx_info = []
    for i in range(idx_table.count):
        str_idx_info.append(HeaderPair.load(fs))

    for i in range(data_table.count):
        str_offset = data_table.offset + (str_idx_info[i].offset * 2)
        str_size = str_idx_info[i].count
        fs.seek(str_offset)

        chr_dec_list = []
        for j in range(str_size):
            n = fs.read_u16() ^ (i * key)
            chr_dec_list.append(struct.pack('<H', n & 0xFFFF).decode('utf-16-le'))

        res.append(U''.join(chr_dec_list))

    return res


def write_string(strings):
    # type: (List[unicode]) -> (str, str)
    encoded_data = []
    f_table = FileStream(None, 'm')
    offset = 0
    for i, text in enumerate(strings):
        f_table.write_u32(offset)                 # offset
        f_table.write_u32(len(text))              # size
        encoded_data.append(text.encode('utf-16-le'))
        offset += len(text)

    return f_table.get_values(), ''.join(encoded_data)


def write_string_with_key(strings, key):
    # type: (List[unicode], int) -> (str, str)
    encoded_data = []
    offset = 0
    f_table = FileStream(None, 'm')
    f_data = FileStream(None, 'm')
    for i, text in enumerate(strings):
        f_table.write_u32(offset)                 # offset
        f_table.write_u32(len(text))              # size
        for c in text:
            enc_c = struct.unpack('<H', c.encode('utf-16-le'))[0] ^ (i * key)
            encoded_data.append(enc_c & 0xFFFF)
        offset += len(text)

    f_data.write_list('H' * len(encoded_data), encoded_data)
    return f_table.get_values(), f_data.get_values()


def write_int_list(int_list):
    # type: (List[int]) -> str
    fs = FileStream(None, 'm')
    for v in int_list:
        fs.write_u32(v)

    return fs.get_values()


def remove_dup_space(str_in):
    res = []
    prev_is_space = False
    for c in str_in:
        if c == U' ':
            if prev_is_space is False:
                res.append(c)
                prev_is_space = True
        else:
            res.append(c)
            prev_is_space = False

    return U''.join(res)


def load_json(str_data, encoding=None):
    return json.loads(str_data, encoding=encoding)


def load_json_file(json_file, encoding=None):
    data = open(json_file, 'rb').read()
    return load_json(data, encoding)


def dump_json(obj, indent=None, is_ascii=True, obj_default=None, is_sort_keys=True):
    return json.dumps(obj, indent=indent, ensure_ascii=is_ascii, default=obj_default, sort_keys=is_sort_keys)