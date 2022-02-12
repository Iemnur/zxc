import codecs
import hashlib
import os
import glob
import struct
import json
from shutil import copyfile

# Common
# ----------------------------------------------------------- #
UTF_16_LE = 'utf-16-le'
UTF_16_BE = 'utf-16-be'
BOM_UTF16_LE = '\xff\xfe'
BOM_UTF16_BE = '\xfe\xff'

GBA_MEM_ROM_START = 0x8000000


# Unpack string byte to number
def to_u8(byte):
    result = struct.unpack('B', byte)[0]
    return result


def to_s8(byte):
    result = struct.unpack('b', byte)[0]
    return result


def to_u16_le(byte):
    result = struct.unpack('<H', byte)[0]  # Unsigned short LE
    return result


def to_s16_le(byte):
    result = struct.unpack('<h', byte)[0]  # Signed short LE
    return result


def to_u16_be(byte):
    result = struct.unpack('>H', byte)[0]  # BE
    return result


def to_s16_be(byte):
    result = struct.unpack('>h', byte)[0]  # BE
    return result


def to_u32_le(byte):
    result = struct.unpack('<I', byte)[0]  # LE
    return result


def to_s32_le(byte):
    result = struct.unpack('<i', byte)[0]  # LE
    return result


def to_u32_be(byte):
    result = struct.unpack('>I', byte)[0]  # BE
    return result


def to_s32_be(byte):
    result = struct.unpack('>i', byte)[0]  # BE
    return result


def to_float_le(number):
    result = struct.unpack('<f', number)[0]
    return result


def to_float_be(number):
    result = struct.unpack('>f', number)
    return result


def to_list_u32_le(byte, count):
    result = struct.unpack('<' + 'I' * count, byte)  # LE
    return result

def gba_to_u32_le(byte):
    value = to_u32_le(byte)
    if value < GBA_MEM_ROM_START:
        return 0
    return value - GBA_MEM_ROM_START


# Pack number to string byte
def to_str_u8(number):
    result = struct.pack('B', number)
    return result


def to_str_s8(number):
    result = struct.pack('b', number)
    return result


def to_str_u16_le(number):
    result = struct.pack('<H', number)
    return result


def to_str_s16_le(number):
    result = struct.pack('<h', number)
    return result


def to_str_u32_le(number):
    result = struct.pack('<I', number)
    return result


def to_str_s32_le(number):
    result = struct.pack('<i', number)
    return result


def to_str_u16_be(number):
    result = struct.pack('>H', number)
    return result


def to_str_s16_be(number):
    result = struct.pack('>h', number)
    return result


def to_str_u32_be(number):
    result = struct.pack('>I', number)
    return result


def to_str_s32_be(number):
    result = struct.pack('>i', number)
    return result


def to_sfloat_le(number):
    result = struct.pack('<f', number)
    return result


def to_sfloat_be(number):
    result = struct.pack('>f', number)
    return result


# Other
def text_unk_byte(byte):
    m_data = ""
    m_data += ("<$" + to_str_u8(byte) + ">").encode(UTF_16_LE)
    return m_data


def text_unk_2byte(byte):
    m_data = ""
    m_data += ("<$" + to_s16_le(byte) + ">").encode(UTF_16_LE)
    return m_data


def get_size(path):
    return os.path.getsize(path)


def get_folder_path(file_path):
    file_path = file_path.replace('\\', '/')
    folder_path = ''
    if file_path.find('/') != -1:
        folder_path = '/'.join(file_path.split('/')[:-1]) + '/'
    return folder_path


def is_ascii(character):
    return all(ord(c) <= 127 & ord(c) >= 32 for c in character)


def is_file(path):
    if not os.path.isfile(path):
        return False
    return True


def is_folder(path):
    if not os.path.isdir(path):
        return False
    return True


def new_folder(path):
    if not os.path.exists(path) and path.strip() != '':
        os.makedirs(path)


def list_files(folder):
    return os.listdir(folder)


def get_md5(data):
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()


def cp_file(s, d):
    copyfile(s, d)


def get_file_name(path, with_ext=False):
    if not isinstance(path, (str, unicode)):
        return path

    path = path.replace("\\", "/")
    name_with_ext = path.split("/")[-1]
    if with_ext:
        return name_with_ext

    name_without_ext = name_with_ext.split('.')[0]
    return name_without_ext


def get_file_ext(path):
    file_name = get_file_name(path, True)
    if len(file_name.split('.')) > 1:
        return file_name.split('.')[1]
    return ''

def find_file_v2(name, path):
    # check / end path
    if path[len(path) - 1] != '/':
        path += '/'

    list_file = glob.glob(path + name)
    return list_file


def find_file(name, path):
    # l_file = []
    for root, dirs, files in os.walk(path):
        for nfile in files:
            if nfile == name:
                # pdb.set_trace()
                return root + "\\" + name
                # l_file.append(root+"\\"+name)

    return ''


def list_all_file(path):
    l_file = []
    path = path.replace('/', '\\')
    for root, dirs, files in os.walk(path):
        for nfile in files:
            l_file.append(root + "\\" + nfile)

    return l_file


def list_all_file_with_ext(path, ext):
    l_file = []
    path = path.replace('/', '\\')
    for root, dirs, files in os.walk(path):
        for nfile in files:
            if nfile.split('.')[-1] == ext:
                l_file.append(root + "\\" + nfile)

    return l_file


# Split array
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def dump_json(obj, indent=None, is_ascii=True, obj_default=None, is_sort_keys=True):
    return json.dumps(obj, indent=indent, ensure_ascii=is_ascii, default=obj_default, sort_keys=is_sort_keys)


def load_json(data, encoding=None):
    return json.loads(data, encoding=encoding)


def hex_str_to_bin_str(hex_str):
    if not isinstance(hex_str, str):
        return hex_str
    hex_str = hex_str.replace('0x', '')
    return hex_str.decode('hex')


def load_bm_font_txt_conf(txt_path):
    try:
        fi_txt = codecs.open(txt_path, 'r', 'utf-8')
    except UnicodeError:
        raise UnicodeError('[ERROR]: Config file must save with UTF-8 encoding!')
    line = fi_txt.readline()

    bm_dict = {}
    while line != '':
        if line.strip() == '':
            line = fi_txt.readline()
            continue

        arr_line = line.split(None, 1)
        key_parent = arr_line[0]
        tk_eq_child_line = arr_line[1].split('=')
        arr_tk_child_clean = []
        for i in tk_eq_child_line:
            # Case: key="abc"
            arr_tk_quot = i.split("\"")
            if len(arr_tk_quot) > 1:
                str_val = ''.join(arr_tk_quot[:-1])
                next_key = arr_tk_quot[-1].strip()
                arr_tk_child_clean.append(str_val)
                arr_tk_child_clean.append(next_key)
            else:
                arr_tk_child_clean += i.split()

        # Load parent
        parent_arr = []
        if key_parent in bm_dict:
            parent_arr = bm_dict[key_parent]

        # Load child obj
        child_dict = {}
        next_is_key = True
        k = ''
        v = ''
        for i in arr_tk_child_clean:
            if next_is_key:
                k = i
                next_is_key = False
            else:
                v = i
                child_dict[k] = v
                next_is_key = True

        # Add child to parent array
        parent_arr.append(child_dict)
        # Add to result
        bm_dict[key_parent] = parent_arr
        # Next line
        line = fi_txt.readline()

    return bm_dict


def is_include_all(item_check, src):
    for c in item_check:
        if c not in src:
            return False
    return True


def is_shift_jis(num):
    if 0x81 <= num <= 0x9F or (0xE0 <= num <= 0xEF):
        return True
    return False
