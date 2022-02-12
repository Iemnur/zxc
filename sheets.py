import sys

from shared.request import rq_get
from shared.common import *
from text.merger2 import unmerge_common_json_rows
from text.inserter import insert_from_common_json



def request_to_sheet(base_url, kk, api, params):
    # type: (str or unicode, str or unicode, str, List) -> Dict
    f, k = kk.split('|', 1)
    resp = rq_get(base_url, {'api': api, f: k, 'params': params})
    return resp


def get_sheets(base_url, kk):
    resp = request_to_sheet(base_url, kk, '2', ['commonJson'])
    if isinstance(resp, dict) and resp.get('status') == 1:
        sheets_name = resp.get('data')  # type: List
        print 'Get sheets name ok!'
        print sheets_name
        print '------------------'
        return sheets_name

    print 'Get sheets name error!'
    print resp
    print '------------------'
    return False


def get_sheet_data(sheet_name, base_url, kk):
    resp = request_to_sheet(base_url, kk, '3', [sheet_name])
    if isinstance(resp, dict) and resp.get('status') == 1:
        sheets_data = resp.get('data')  # type: List
        print 'Get {} data ok!'.format(sheet_name)
        print '------------------'
        return sheets_data

    print 'Get {} data error!'.format(sheet_name)
    print resp
    print '------------------'
    return False


def proc_data(base_url, kk, folder_org_txt):
    folder_data_out = 'data/sheet'
    make_dirs(folder_data_out)

    if base_url and kk:
        sheets_name = get_sheets(base_url, kk)
        if not sheets_name:
            raise ValueError

        for s_name in sheets_name:
            print s_name
            sheet_data = get_sheet_data(s_name, base_url, kk)
            if not sheet_data:
                raise ValueError
            # unmerge
            json_folder = '{}/json'.format(folder_data_out)
            print 'Unmerge data and save to folder: {}'.format(json_folder)

            make_dirs(json_folder)
            all_file_unmerged = unmerge_common_json_rows(sheet_data, json_folder)

            # json to txt
            txt_folder = '{}/txt'.format(folder_data_out)
            print 'Convert json to txt and save to folder: {}'.format(txt_folder)
            make_dirs(txt_folder)
            for json_filepath in all_file_unmerged:
                filename = get_filename(json_filepath, False)
                origin_txt_filepath = '{}/{}.strings.txt'.format(folder_org_txt, filename)
                txt_out_path = '{}/{}.strings.txt'.format(txt_folder, filename)

                print '[IN] {}\n[IN] {}\n[OUT] {}'.format(json_filepath, origin_txt_filepath, txt_out_path)
                insert_from_common_json(json_filepath, origin_txt_filepath, txt_out_path, 'utf8')
                print '+++++++++++++++++++++++'

            print '--------------------------------'


def main():
    base_url = None
    kk = None
    folder_org_txt = './'
    # folder_org_txt = 'data/rwp_jp_dis/resources'

    if len(sys.argv) > 3:
        base_url = sys.argv[1]
        kk = sys.argv[2]
        folder_org_txt = sys.argv[3]

    proc_data(base_url, kk, folder_org_txt)
    print 'Done!'
    pass


if __name__ == '__main__':
    main()
