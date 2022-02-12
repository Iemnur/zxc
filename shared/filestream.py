import struct
import io


class FileStream:
    def __init__(self, filepath, mode, little_endian=True):
        if mode == 'm':
            self.fs = io.BytesIO(filepath)
        else:
            self.fs = open(filepath, mode)
            self.filepath = filepath
        self.mode = mode
        self.endian = '<' if little_endian else '>'

    def __exit__(self, exc_type, exc_value, traceback):
        self.fs.close()

    def close(self):
        self.fs.close()

    def get_values(self):
        return self.read_at(0)

    def tell(self):
        return self.fs.tell()

    def tell_hex(self):
        return '0x%08X' % self.tell()

    def seek(self, pos, whence=0):
        self.fs.seek(pos, whence)

    def read(self, size=-1):
        return self.fs.read(size)

    def read_at(self, pos, size=-1):
        current = self.fs.tell()
        self.seek(pos)
        data = self.read(size)
        self.seek(current)
        return data

    def read_u8(self):
        return struct.unpack(self.endian + 'B', self.read(1))[0]

    def peek_u8(self):
        current = self.fs.tell()
        num = self.read_u8()
        self.seek(current)
        return num

    def read_u16(self):
        return struct.unpack(self.endian + 'H', self.read(2))[0]

    def read_u32(self):
        return struct.unpack(self.endian + 'I', self.read(4))[0]

    def read_s8(self):
        return struct.unpack(self.endian + 'b', self.read(1))[0]

    def read_s16(self):
        return struct.unpack(self.endian + 'h', self.read(2))[0]

    def read_s32(self):
        return struct.unpack(self.endian + 'i', self.read(4))[0]

    def read_float(self):
        return struct.unpack(self.endian + 'f', self.read(4))[0]

    def read_list(self, number_format):
        return struct.unpack(self.endian + number_format, self.read(struct.calcsize('={}'.format(number_format))))

    def read_line(self, size=-1):
        return self.fs.readline(size)

    def read_lines(self, size=-1):
        return self.fs.readlines(size)

    def read_hex(self, size=1, space=False):
        str_out = ''
        while size != 0:
            str_out += self.read(1).encode('hex') + ' ' if space else ''
            size -= 1

        return str_out

    def read_string(self):
        str_out = ''
        while True:
            byte = self.read_u8()
            if byte == 0:
                break
            else:
                str_out += chr(byte)

        return str_out

    def write(self, data):
        self.fs.write(data)

    def write_at(self, data, pos):
        current = self.tell()
        self.seek(pos)
        self.write(data)
        self.seek(current)

    def write_u8(self, num):
        self.write(struct.pack('B', num & 0xFF))

    def write_u8_at(self, num, pos):
        current = self.tell()
        self.seek(pos)
        self.write_u8(num)
        self.seek(current)

    def write_s8(self, num):
        self.write(struct.pack('b', num & 0xFF))

    def write_s8_at(self, num, pos):
        current = self.tell()
        self.seek(pos)
        self.write_s8(num)
        self.seek(current)

    def write_u16(self, num):
        self.write(struct.pack(self.endian + 'H', num & 0xFFFF))

    def write_u16_at(self, num, pos):
        current = self.tell()
        self.seek(pos)
        self.write_u16(num)
        self.seek(current)

    def write_s16(self, num):
        self.write(struct.pack(self.endian + 'h', num & 0xFFFF))

    def write_s16_at(self, num, pos):
        current = self.tell()
        self.seek(pos)
        self.write_s16(num)
        self.seek(current)

    def write_u32(self, num):
        self.write(struct.pack(self.endian + 'I', num & 0xFFFFFFFF))

    def write_u32_at(self, num, pos):
        current = self.tell()
        self.seek(pos)
        self.write_u32(num)
        self.seek(current)

    def write_s32(self, num):
        self.write(struct.pack(self.endian + 'i', num & 0xFFFFFFFF))

    def write_s32_at(self, num, pos):
        current = self.tell()
        self.seek(pos)
        self.write_s32(num)
        self.seek(current)

    def write_float(self, num):
        self.write(struct.pack(self.endian + 'f', num & 0xFFFFFFFF))

    def write_float_at(self, num, pos):
        current = self.tell()
        self.seek(pos)
        self.write_float(num)
        self.seek(current)

    def write_hex(self, str_hex):
        str_hex = str_hex.repalce(' ', '').decode('hex')
        self.write(str_hex)

    def write_hex_at(self, str_hex, pos):
        current = self.tell()
        self.seek(pos)
        self.write_hex(str_hex)
        self.seek(current)

    def write_list(self, number_format, number_list):
        self.write(struct.pack(self.endian + number_format, *number_list))

    def write_list_at(self, number_format, number_list, pos):
        current = self.tell()
        self.seek(pos)
        self.write_list(number_format, number_list)
        self.seek(current)
