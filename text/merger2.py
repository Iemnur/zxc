import glob

from base import *
from shared.common import *


def merge_from_common_json(json_folder, folder_out, max_lines=20000):
    all_asm_file = glob.glob(U'{}/*.json'.format(json_folder))

    dict_json_files = {}
    header = None

    print 'Pre data...'
    for f_path in all_asm_file:
        json_rows = load_json_file(f_path)
        f_name = get_filename(f_path, False)
        if not header:
            header = json_rows['header']

        dict_json_files[f_name.lower()] = json_rows['lines']

    dict_file_routes_id = {}
    for filename in dict_json_files:
        route_id = get_route_id(filename)
        if route_id not in dict_file_routes_id:
            dict_file_routes_id[route_id] = [filename.lower()]
        else:
            dict_file_routes_id[route_id].append(filename.lower())

    print 'Start merge'
    overview_col_start = 2
    for route_id in sorted(dict_file_routes_id):
        all_filename_in_route = dict_file_routes_id[route_id]

        split_container = []
        lines = []
        route_name = ROUTES_DEFINE[route_id]
        toc = []
        for filename in sorted(all_filename_in_route):
            head_row = [U''] * len(header)
            head_row[0] = U'!hidden_file_{}'.format(filename)
            lines.append(head_row)

            idx_start = len(lines)
            lines_data = dict_json_files[filename]
            if U''.join(lines_data[-1]) == U'':
                lines_data.pop()

            lines.extend(lines_data)
            idx_end = len(lines)

            toc.append({
                'filename': filename.upper(),
                'range': [idx_start, idx_end - idx_start]
            })

            if idx_end >= max_lines:
                split_container.append(
                    (toc, lines)
                )
                lines = []
                toc = []

        if len(lines):
            split_container.append(
                (toc, lines)
            )

        if len(split_container) == 1:
            toc, lines = split_container[0]
            file_out = '{}/{}'.format(folder_out, route_name)
            json_obj = {
                'header': header,
                'overview': {
                    'direction': 'h',
                    'container_name': route_name,
                    'col_pos': overview_col_start,
                    'src_trans_col': 3,
                    'name': 'Overview',
                    'count': [3, 4],
                    'toc': toc
                },
                'lines': lines
            }
            overview_col_start += 3

            print file_out
            open(file_out, 'wb').write(dump_json(json_obj, indent=2, is_ascii=False).encode('utf8'))
        else:
            for i, (toc, lines) in enumerate(split_container):
                filename = '{}_p{}'.format(route_name, i)
                file_out = '{}/{}'.format(folder_out, filename)
                json_obj = {
                    'header': header,
                    'overview': {
                        'direction': 'h',
                        'container_name': filename,
                        'col_pos': overview_col_start,
                        'src_trans_col': 3,
                        'name': 'Overview',
                        'count': [3, 4],
                        'toc': toc
                    },
                    'lines': lines
                }

                print file_out
                open(file_out, 'wb').write(dump_json(json_obj, indent=2, is_ascii=False).encode('utf8'))

            overview_col_start += 3
    pass


def unmerge_common_json_rows(rows, out_folder):
    lines = []
    filename = None
    all_file_unmerged = []
    for row in rows:
        if row[0].strip().startswith(U'!hidden_file_'):
            if len(lines) and filename:
                path_out = U'{}/{}.json'.format(out_folder, filename)
                print path_out
                open(path_out, 'wb').write(dump_json({'lines': lines, }, indent=2, is_ascii=False).encode('utf8'))
                all_file_unmerged.append(path_out)

            lines = []
            filename = row[0].strip().split(U'!hidden_file_', 1)[-1]
        else:
            lines.append(row)

    if len(lines) and filename:
        path_out = U'{}/{}.json'.format(out_folder, filename)
        print path_out
        open(path_out, 'wb').write(dump_json({'lines': lines, }, indent=2, is_ascii=False).encode('utf8'))
        all_file_unmerged.append(path_out)

    return all_file_unmerged
