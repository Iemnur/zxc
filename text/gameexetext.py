import re
from shared.common import *


def read_gameexe_ini(filepath):
    lines = open(filepath, 'rb').readlines()

    res_dict = {}
    for i, line in enumerate(lines):
        line = line.decode('utf8')
        if line.strip() == U'':
            continue

        k, v = line.split(U'=', 1)
        k = k.strip()
        if k not in res_dict:
            res_dict[k] = [(i, v)]
        else:
            res_dict[k].append((i, v))

    return res_dict


def ini_namae_dumper(lines_info, idx_start):
    str_pat = ur'\".+\"'
    idx = idx_start
    rows = []
    lines_format = []
    for line_number, value in lines_info:
        namae_key, namae_val, ex = value.split(U',', 2)
        namae_key_match = re.findall(str_pat, namae_key)
        namae_val_match = re.findall(str_pat, namae_val)
        if not namae_key_match or not namae_val_match:
            print 'Parse namae string error in line number: {}'.format(line_number)
            raise ValueError

        namae_key_format = re.sub(str_pat, U'"{{{}}}"'.format(idx), namae_key)
        idx += 1
        namae_val_format = re.sub(str_pat, U'"{{{}}}"'.format(idx), namae_val)
        idx += 1

        r_namae_k = namae_key_match[0][1:-1]
        r_namae_v = namae_val_match[0][1:-1]
        rows.append([line_number, U'#NAMAE!2,3|4', r_namae_k, r_namae_v, U''])
        lines_format.append((line_number, U'{},{},{}'.format(namae_key_format, namae_val_format, ex)))

    return idx, rows, lines_format


def dump_value_ini_to_common_json(ini_path, json_out_path):
    ini_dict = read_gameexe_ini(ini_path)
    dumpers = [(U'#NAMAE', ini_namae_dumper)]

    idx = 0
    rows = []  # 5 column: line_num, meta_info, val1, val2, trans
    for k, dumper in dumpers:
        idx, rr, lines_format = dumper(ini_dict.get(k), idx)
        ini_dict[k] = lines_format
        rows.extend(rr)

    json_obj = {
        'header': [[U'LINE', 75],
                   [U'KEY', 75],
                   [U'VAL1', 150],
                   [U'VAL2', 400],
                   [U'VN', 500]],
        'lines': rows,
        'ex_data': ini_dict
    }

    print json_out_path
    open(json_out_path, 'wb').write(dump_json(json_obj, 2, False).encode('utf8'))


def insert_value_ini_from_common_json(json_path, ini_out_path):
    json_obj = load_json_file(json_path, encoding='utf8')
    rows = json_obj['lines']
    ini_dict = json_obj['ex_data']
    lines_dict = {}

    trans_data = []
    for r in rows:
        if not U''.join(r[1:]):
            continue

        meta_info = r[1]
        cells_info = meta_info.split(U'!', 1)[1].split(U',')
        for info in cells_info:
            prio_arr = info.split(U'|')
            if len(prio_arr) > 1:
                trans_col = int(prio_arr[1])
                default_col = int(prio_arr[0])
                if r[trans_col]:
                    trans_data.append(r[trans_col])
                else:
                    trans_data.append(r[default_col])
            else:
                trans_data.append(r[int(info)])
    for k in ini_dict:
        k_lines = ini_dict.get(k)
        for line_num, line in k_lines:
            lines_dict[line_num] = U'{} ={}'.format(k, line.format(*trans_data))

    i = 0
    out = []
    for line_num in sorted(lines_dict):
        while line_num > i:
            out.append(U'')
            i += 1

        out.append(lines_dict.get(line_num).strip(U'\r\n'))
        i += 1

    print ini_out_path
    open(ini_out_path, 'wb').write(U'\r\n'.join(out).encode('utf8'))


def ini_namae_parse(line_number, value):
    str_pat = ur'\".+\"'

    namae_key, namae_val, ex = value.split(U',', 2)
    namae_key_match = re.findall(str_pat, namae_key)
    namae_val_match = re.findall(str_pat, namae_val)
    if not namae_key_match or not namae_val_match:
        print 'Parse namae string error in line number: {}'.format(line_number)
        raise ValueError

    namae_key_format = re.sub(str_pat, U'"{}"', namae_key)
    namae_val_format = re.sub(str_pat, U'"{}"', namae_val)

    r_namae_k = namae_key_match[0][1:-1]
    r_namae_v = namae_val_match[0][1:-1]
    values_out = [U'3,4|5', r_namae_k, r_namae_v, U'']
    value_format = U'{},{},{}'.format(namae_key_format, namae_val_format, ex)

    return values_out, value_format


def dump_value_ini_to_common_json2(ini_path, json_out_path, encoding='utf8'):
    lines = open(ini_path, 'rb').readlines()
    items_parser = {
        U'#NAMAE': ini_namae_parse
    }

    rows = []
    for i, line in enumerate(lines):
        line = line.decode(encoding).strip(U'\r\n')
        if line.strip() == U'':
            rows.append([U'!hidden_raw', line])
            continue

        k, v = line.split(U'=', 1)
        ks = k.strip()

        if ks in items_parser:
            values_out, value_format = items_parser[ks](i, v)
            row = [ks, U'{}={}'.format(k, value_format)]
            row.extend(values_out)
            rows.append(row)
        else:
            rows.append([U'!hidden_raw', line])

    json_obj = {
        'header': [[U'ID', 75],
                   [U'FORMAT', 130],
                   [U'META', 75],
                   [U'VAL1', 150],
                   [U'VAL2', 400],
                   [U'VN', 500]],
        'lines': rows,
    }

    print json_out_path
    open(json_out_path, 'wb').write(dump_json(json_obj, 2, False).encode('utf8'))


def insert_value_ini(rows):
    out = []

    for row in rows:
        if U'raw' in row[0].split(U'_'):
            out.append(row[1])
        else:
            format_line = row[1]
            meta_info = row[2]
            cells_info = meta_info.split(U',')
            values = []
            for info in cells_info:
                prio_arr = info.split(U'|')
                if len(prio_arr) > 1:
                    trans_col = int(prio_arr[1])
                    default_col = int(prio_arr[0])
                    if row[trans_col]:
                        values.append(row[trans_col])
                    else:
                        values.append(row[default_col])
                else:
                    if U''.join(row):
                        values.append(row[int(info)])

            out.append(format_line.format(*values))

    return out


def insert_value_ini_from_common_json2(json_path, ini_out_path):
    json_obj = load_json_file(json_path, encoding='utf8')
    rows = json_obj['lines']
    out = insert_value_ini(rows)

    print ini_out_path
    open(ini_out_path, 'wb').write(U'\r\n'.join(out).encode('utf8'))
