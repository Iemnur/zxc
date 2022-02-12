class MyCSV:
    def __init__(self, csv_chr=U','):
        self.rows = []
        self.csv_char = csv_chr
        pass

    def add_row(self, row):
        class CmdCell:
            def __init__(self):
                pass
            NONE = 0
            HAS_START_QUOTE = 1

        tmp_row = []
        for cell in row:
            cell_strip = cell.strip()
            # TODO optimize + fix more case

            if cell_strip.find(U'"') != -1:
                cell_r = cell.replace(U'"', U'""')
                cell = U'"{}"'.format(cell_r)
            elif cell.find(self.csv_char) != -1:
                cell = U'"{}"'.format(cell)
            elif cell.find(U'\n') != -1:
                cell = U'"{}"'.format(cell)

            tmp_row.append(cell)

        self.rows.append(tmp_row)

    def to_data(self):
        lines = []
        for row in self.rows:
            line = self.csv_char.join(row)
            lines.append(line)

        return U'\n'.join(lines)

    def to_file(self, path_out, enc='utf8'):
        import codecs
        codecs.open(path_out, 'wb', encoding=enc).write(self.to_data())

