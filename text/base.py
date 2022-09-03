# coding=utf-8
import codecs

JSON_ID = 'ab1st'

ROUTES_DEFINE = {
    0: U'Unknown',
    1: U'Common',
    2: U'Kotori',
    3: U'Chihaya',
    4: U'Akane',
    5: U'Shizuru',
    6: U'Lucia',
    7: U'Moon',
    8: U'Terra',  # Ｔｅｒｒａ
    81: U'Oppai',
    90: U'Ending',

    100: U'System',
    101: U'System Popup',
    102: U'System Mappie',
    103: U'System Effect',
}


def get_route_id(filename):
    name = filename.lower().strip()
    if name.startswith('seen'):
        # seen0XYYY.txt
        if name[4:7] == '081':
            # Oppai
            return 81
        return int(name[4:6])
    elif name.startswith('ed_'):
        return 90
    elif name.startswith('sys10_mm02'):
        return 101
    elif name.startswith('sys40_mp50_'):
        return 102
    elif name.startswith('sys50_ef00'):
        return 103
    else:
        # Treat to System
        return 100


def get_route_name(filename):
    route_id = get_route_id(filename)
    return ROUTES_DEFINE[route_id]


def is_text_code(str_jp, str_en, str_vi):
    if len(str_jp) > 2 and (str_jp[0] == U'_' or str_jp[2] == U'_'):
        return True
    if str_jp.strip() == str_en.strip() == str_vi.strip():
        return True

    return False


def load_text_file(file_path, enc='utf-16'):
    lines = codecs.open(file_path, 'rb', encoding=enc).readlines()

    current_id = 0
    line_dict = {}
    for line in lines:
        line_strip = line.strip()
        if line_strip.startswith(U'//') or len(line_strip) == 0:
            continue
        elif line_strip[0] == U'<':
            token_start_pos = line.find(U'<')
            token_end_pos = line.find(U'>')
            if token_start_pos == -1 or token_end_pos == -1 or token_start_pos > token_end_pos:
                raise ValueError('token error')

            str_id = int(line[token_start_pos + 1:token_end_pos], 10)
            if str_id != current_id:
                raise ValueError('str diff')

            text_line = line[token_end_pos + 1:].rstrip(U'\r\n')
            if text_line[0] == U' ':
                text_line = text_line[1:]

            line_dict[str_id] = [text_line]
            current_id += 1
        elif line_strip[0] == U'{':
            # extra code line
            line_dict[current_id - 1].append(line.rstrip(U'\r\n'))
        else:
            raise ValueError(U'Unk in line: {}'.format(line))

    return line_dict


class DialogData:
    TALK = 1
    CHOICE = 2
    TITLE = 3
    POPUP = 4
    FURIGANA = 5
    UNK = 99

    def __init__(self, d_type=UNK, names=None, lines=None, ex=None):
        self.type = d_type
        self.names = names or []
        self.lines = lines or []
        self.ex = ex or {'map_name': {}, 'furigana': {}}

        pass

    def put_map_name(self, str_name_id, str_line_id):
        if str_name_id not in self.ex['map_name']:
            self.ex['map_name'][str_name_id] = None

        self.ex['map_name'][str_name_id] = str_line_id

    def put_furigana_id(self, str_line_id):
        self.ex['furigana'][str_line_id] = True

    def get_map_name(self):
        return self.ex['map_name']

    def get_furigana(self):
        return self.ex['furigana']

