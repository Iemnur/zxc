import sys
import argparse
import multiprocessing
import glob

from shared.common import *
from pack import PCK, GameExe
from script import Disassembler, Assembler


def read_key_file(key_path):
    """
    format: 16 bytes
        0x1A 0x2B ... or
        1A 2B ...

    :param key_path: str
    :return: list
    """

    line = open(key_path, 'rb').readline().replace(U',', U'')
    num_list = line.split(' ')
    if len(num_list) < 16:
        raise ValueError('Format of key incorrect!')

    ret = []
    for num in num_list:
        ret.append(int(num, 16))

    return ret


def parse_arg():
    parser = argparse.ArgumentParser(description='RWPlus tool')
    parser.add_argument('-v', '--version', action='version', version="1.0")

    parser.add_argument('-multi', help='Enable multi process for assembler.',
                        action='store_true', default=False)
    parser.add_argument('-key', help='Add key file.', metavar='key_path',
                        default=False)
    parser.add_argument('-res', help='Set resource path.', metavar='res_path',
                        default=False)

    parser.add_argument('-dis', nargs=3, type=str, metavar=('pck_path', 'folder_output', 'func_def_path'),
                        help='Disassembler script.')

    parser.add_argument('-asm', nargs=2, type=str, metavar=('asm_path', 'out_path'),
                        help='Assembler script.')

    parser.add_argument('-pack', nargs=argparse.PARSER, type=str, metavar='ss_folder, out_path, global_ini',
                        help='Repack PCK.')

    parser.add_argument('-decgexe', nargs=2, type=str, metavar=('dat_path', 'out_path'),
                        help='Decode Gameexe.dat')

    parser.add_argument('-encgexe', nargs=argparse.PARSER, type=str, metavar='ini_folder, out_path, compress_level',
                        help='Encode Gameexe.dat')

    args_ret = parser.parse_args()
    if len(sys.argv) <= 1:
        parser.print_help()

    return args_ret
    pass


def dis_proc(key16, resource_path, pck_path, out_folder, func_def_path):
    disams = Disassembler(pck_path, key16, func_def_path, resource_path)
    disams.disassembler_all_file(out_folder)
    pass


def assembler_task(argv_in):
    asm_in_path, ss_out_path = argv_in
    print asm_in_path
    asm = Assembler().from_file(asm_in_path)
    asm.to_file(ss_out_path)
    return 0


def asm_proc(multi_proc, in_path, out_path):

    def get_args():
        is_folder_input = is_folder(in_path)
        _args = []
        if is_folder_input:
            all_asm_file = glob.glob(U'{}/*.asm'.format(in_path))
            for file_path in all_asm_file:
                f_name = get_filename(file_path, False)
                out_file = U'{}/{}.ss'.format(out_path, f_name)
                _args.append((file_path.replace(U'\\', U'/'), out_file))
        else:
            _args.append((in_path, out_path))

        return _args

    args = get_args()

    if multi_proc:
        p = multiprocessing.Pool(multiprocessing.cpu_count())
        p.map(assembler_task, args)
    else:
        for argv in args:
            assembler_task(argv)
    pass


def repack_pck_proc(key16, ss_folder, out_path, global_ini_path=None):
    pck = PCK('w')
    pck.repack_data(ss_folder, out_path, global_ini_path, key16)
    pass


def decode_gexe_proc(key16, in_path, out_path):
    gexe = GameExe()
    gexe.decode_to_file(in_path, out_path, key16)
    pass


def encode_gexe_proc(key16, in_path, out_path, compress_level=0):
    if isinstance(compress_level, (str, unicode)):
        try:
            compress_level = int(compress_level)
        except:
            raise ValueError('compress_level invalid!!')

    gexe = GameExe()
    gexe.encode_to_file(in_path, out_path, key16, compress_level)
    pass


def main():
    # sys.argv.extend(['-dis', 'data/pck/steam/SceneEN.pck', 'data/script_dis', 'data/cfg/func.def'])
    # sys.argv.extend(['-multi', '-asm', 'data/script_dis', 'data/assembler'])
    # sys.argv.extend(['-pack', 'data/assembler', 'data/pck/test_repack.pck'])
    # sys.argv.extend(['-encgexe', 'data/assembler', 'data/pck/test_repack.pck'])

    args = parse_arg()
    key16 = None
    resource_path = None
    multi_proc = True

    if args.key:
        key16 = read_key_file(args.key)

    if args.res:
        resource_path = args.res

    if not args.multi:
        multi_proc = False

    if args.dis:
        argv = args.dis
        dis_proc(key16, resource_path, *argv)
    elif args.asm:
        argv = args.asm
        asm_proc(multi_proc, *argv)
    elif args.pack:
        argv = args.pack
        repack_pck_proc(key16, *argv)
    elif args.decgexe:
        argv = args.decgexe
        decode_gexe_proc(key16, *argv)
    elif args.encgexe:
        argv = args.encgexe
        encode_gexe_proc(key16, *argv)

    print 'Done!'
    pass


if __name__ == '__main__':
    main()
