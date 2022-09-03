import unicodedata
from base import *
from common.util import *


def insert_from_common_json(json_file, org_txt_file, path_out, encoding='utf-16'):
    org_text_dict = load_text_file(org_txt_file, encoding)
    json_rows = load_json(open(json_file, 'rb').read())

    text_dict = {}
    for row in json_rows['lines']:
        jp_id, _, _, jp_text, vn_text, _, _, vn_id = row
        vn_id = vn_id.strip().split(U':')[-1]
        jp_id = jp_id.strip()
        if len(jp_id) == 0:
            continue
        jp_id = int(jp_id)
        if len(vn_id) > 0:
            if jp_id not in org_text_dict:
                raise ValueError('Id not found: {}'.format(jp_id))

            vn_text = vn_text.replace(U'\n', U'\\n').replace(U'[AppendWin]', U'')
            # normalize
            vn_text = unicodedata.normalize('NFC', vn_text)

            # if jp_text.find(U'[AppendWin]') != -1:
            #     vn_text += U'\\n'
            text_dict[jp_id] = [jp_text, vn_text]

    lines_out = []
    for line_id in sorted(org_text_dict):
        text_arr = org_text_dict[line_id]
        in_trans_text = False
        if line_id in text_dict:
            in_trans_text = True
            text_arr = text_dict[line_id]
        trans_text = text_arr[0]
        line_id_tag = U'<{:04}>'.format(line_id)
        if in_trans_text and len(text_arr) > 1:
            prep_text = U'// {} {}'.format(line_id_tag, text_arr[0])
            trans_text = text_arr[1]
            lines_out.append(prep_text)
        lines_out.append(U'{} {}'.format(line_id_tag, trans_text))
        lines_out.append(U'')

    codecs.open(path_out, 'wb', encoding).write(U'\r\n'.join(lines_out))

    pass
