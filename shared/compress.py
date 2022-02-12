from filestream import FileStream


# lzss08_decode
def decompress_from_buff(fs, out_size):
    # type: (FileStream, int) -> str
    buff_out = []
    while len(buff_out) < out_size:
        flag = fs.read_u8()
        for i in range(8):
            if len(buff_out) >= out_size:
                break
            if flag & (1 << i):
                buff_out.append(chr(fs.read_u8()))
            else:
                n = fs.read_u16()
                count = (n & 0x0F) + 2
                offset = n >> 4

                for j in range(count):
                    value = buff_out[-offset]
                    buff_out.append(value)

    return ''.join(buff_out)
