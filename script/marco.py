import script
from shared.common import *


class ScriptMacros:
    def __init__(self):
        self._macros = {}             # type: Dict[unicode, ScriptMacros.Macro]
        self._macros_alias_name = {}  # type: Dict[unicode, unicode]
        pass

    class Macro:
        def __init__(self, name, argv, statements, alias_name=None):
            # type: (unicode, Dict[unicode, Tuple[int, any]], List[List[unicode]], Optional[unicode]) -> None
            self.name = name
            # argv_name: (argv_idx, value)
            self.argv = argv
            self.statements = statements
            self.alias_name = alias_name

        def get_value(self, argv_value):
            # type: (Dict[unicode, any]) -> List[unicode]
            res = []
            for statement in self.statements:
                inst = []
                for operand in statement:
                    if operand in argv_value:
                        inst.append(argv_value[operand])
                    else:
                        inst.append(operand)
                res.append(U' '.join(inst))

            return res

    def get_name_by_alias(self, alias_name):
        return self._macros_alias_name.get(alias_name)

    def load(self, filepath):
        fs = io.StringIO(open(filepath, 'rb').read().decode('utf8'))

        line_number = 0
        while True:
            line_number += 1
            line = fs.readline()
            if line == U'':
                break

            line = remove_dup_space(line.strip())

            if line.lower().startswith(U'macro') and line[-1] == U':':
                operands = line[:-1].split(U' ', 2)
                argv_name = U''
                if len(operands) == 3:
                    _, macro_name, argv_name = operands
                else:
                    _, macro_name = operands

                macro_alias = None
                alias_pos = macro_name.find(U'{')
                if alias_pos > 0:
                    if not macro_name.endswith(U'}'):
                        print U'Missing "}" in macro alias, line {}'.format(line_number)
                        raise ValueError

                    macro_alias = macro_name[alias_pos + 1:len(macro_name) - 1]
                    macro_name = macro_name[:alias_pos]

                if macro_alias:
                    self._macros_alias_name[macro_alias] = macro_name

                argv_name_list = [n.strip() for n in argv_name.split(U',')] if argv_name else []
                argv = {k: (i, None) for i, k in enumerate(argv_name_list)}

                statement = []
                while True:
                    line_number += 1
                    line = fs.readline()
                    if line == U'':
                        raise ValueError('"end macro" command not found! line: {}'.format(line_number))

                    line = remove_dup_space(line.strip())
                    if line.lower().startswith(U'end macro'):
                        break

                    operands = line.split(U' ')
                    statement.append(operands)

                macro = self.Macro(macro_name, argv, statement, macro_alias)
                self._macros[macro_name] = macro
            elif line:
                print 'Skip line: {}'.format(line_number)

    def execute(self, macro_name, argv_in, assembler_lines):
        # type: (unicode, List[unicode], Callable[List[unicode]]) -> script.Assembler

        if macro_name not in self._macros:
            print U'macro "{}" not found!'.format(macro_name)
            raise ValueError

        macro = self._macros[macro_name]
        argv_value = {}
        for argv_name in macro.argv:
            argv_idx, _ = macro.argv[argv_name]
            argv_value[argv_name] = argv_in[argv_idx]

        statements = macro.get_value(argv_value)

        return assembler_lines(statements)



