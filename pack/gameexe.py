from shared.common import *
from shared.compress import *
from keys import *


class GameExe:
    """
     00: unused, always = 0 ??
     04: use extra key: = 1 -> key 16 + key 256, 0 -> key 256
    """
    def __init__(self):
        self.id = None
        self.use_extra_key = None
        self.data_decode = None
        self.data_encode = None
        pass

    def decode(self, path, key16=None):
        fs = FileStream(path, 'rb')
        self.id = fs.read_u32()
        self.use_extra_key = fs.read_u32()

        str_buff_encrypted = fs.read()
        self.data_encode = str_buff_encrypted

        buff_decrypted = []
        for i, c in enumerate(str_buff_encrypted):
            n = ord(c)
            if self.use_extra_key:
                if key16 is None:
                    raise ValueError('Require key!')
                n = n ^ key16[i % 16]

            n = n ^ KEY_256_2[i % 256]

            buff_decrypted.append(chr(n))

        bfs = FileStream(''.join(buff_decrypted), 'm')

        compress_size, decompress_size = bfs.read_list('2I')
        if compress_size > len(str_buff_encrypted):
            raise ValueError('Key invalid!, key type: {}'.format('16 or 256' if self.use_extra_key else 256))

        data_decompressed = decompress_from_buff(bfs, decompress_size)
        if decompress_size != len(data_decompressed):
            raise ValueError('Decompress size incorrect!')

        self.data_decode = data_decompressed.decode('utf-16')

        return self.data_decode

    def encode(self, ini_path, key16=None, compress_level=0, encoding='utf8'):
        out = FileStream(None, 'm')
        out.write_u32(0)
        self.id = 0

        if key16:
            out.write_u32(1)
            self.use_extra_key = 1
        else:
            out.write_u32(0)
            self.use_extra_key = 0

        data_ini = open(ini_path, 'rb').read().decode(encoding).encode('utf-16-le')
        self.data_decode = data_ini
        data_buff = FileStream(None, 'm')
        data_compressed = None
        if compress_level == 0:
            data_compressed = lzss08_fake_compress(data_ini)
        else:
            # TODO: real compression
            raise NotImplemented

        data_buff.write_u32(len(data_compressed))
        data_buff.write_u32(len(data_ini))
        data_buff.write(data_compressed)

        for i, c in enumerate(data_buff.get_values()):
            n = ord(c)
            n = n ^ KEY_256_2[i % 256]
            if self.use_extra_key:
                n = n ^ key16[i % 16]

            out.write_u8(n)

        out.seek(8)
        self.data_encode = out.read()

        return out.get_values()

    @staticmethod
    def encode_to_file(ini_path, out_path, key16=None, compress_level=0, encoding='utf8'):
        exe = GameExe()
        enc = exe.encode(ini_path, key16, compress_level, encoding)
        open(out_path, 'wb').write(enc)

    @staticmethod
    def decode_to_file(gameexe_path, out_path, key16=None):
        gexe = GameExe()
        data = gexe.decode(gameexe_path, key16)
        open(out_path, 'wb').write(data.encode('utf8'))
