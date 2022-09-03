from shared.common import *
import io
import script


class NodeData(object):
    def __init__(self, node_id, node_name, data):
        # type: (int, str or unicode, any) -> None
        self.id = node_id
        self.name = node_name  # type: unicode
        self.child_nodes = {}  # type: Dict[int, NodeData]
        self.data = data
        pass

    def add_child(self, node_id, node):
        # type: (int, NodeData) -> None
        if node_id in self.child_nodes:
            self.child_nodes[node_id].add_child(node_id, node)
        else:
            self.child_nodes[node_id] = node
        pass

    def find_child(self, path_to_child):
        # type: (List[int]) -> List[NodeData]
        res = []
        if len(path_to_child):
            node_id = path_to_child[0]
            if node_id in self.child_nodes:
                res.append(self.child_nodes[node_id])
                res.extend(self.child_nodes[node_id].find_child(path_to_child[1:]))

        return res

    def get_child(self, node_id):
        # type: (int) -> NodeData
        return self.child_nodes.get(node_id)


class FunctionDef:

    NODE_ELEMENT = U'element'
    NODE_PROP = U'prop'
    NODE_LIST = U'list'
    NODE_CMD = U'cmd'
    NODE_LIST_STAGE = U'list_stage_idx'
    NODE_STAGE_IDX = U'stage_idx'
    LIST_STAGE_SAME_TYPE = -1

    def __init__(self):
        self.nodes = NodeData(0, U'Root', U'R')
        self.line_idx = 0
        pass

    def _read_cmd(self, line, fs, parent_node):
        # type: (unicode, io.StringIO, NodeData) -> None

        if not line.endswith(U':'):
            raise ValueError('Missing ":" in line {}'.format(self.line_idx))

        _, cmd_id = line.split(U' ', 1)
        cmd_id = str_to_int(cmd_id[:-1])
        child_node = parent_node.get_child(cmd_id)
        if child_node is not None and child_node.id != self.NODE_CMD:
            raise ValueError('Duplicate id of cmd in line {}'.format(self.line_idx))

        overload_dict = {}
        while True:
            line = fs.readline()
            self.line_idx += 1
            if line == U'':
                print U'Expect "end" command in cmd node!. Line: {}'.format(self.line_idx)
                raise ValueError

            line = remove_dup_space(line.split(U'//')[0].strip())
            if line.startswith(U'end'):
                break

            if line.startswith(U'-'):
                _, option_id, return_type, func_name, args = line.split(U' ', 4)
                args = args.replace(U' ', U'')
                overload_dict[U'{}_{}'.format(option_id, args.lower())] = (option_id, return_type, func_name, args)
            elif line.startswith(U'*'):
                _, option_id, return_type, func_name, args = line.split(U' ', 4)
                args = args.replace(U' ', U'')
                overload_dict[U'*'.format(option_id, args.lower())] = (option_id, return_type, func_name, args)

        cmd_node = NodeData(cmd_id, self.NODE_CMD, (cmd_id, overload_dict))
        parent_node.add_child(cmd_id, cmd_node)

    def _read_list(self, line, fs, parent_node):
        # type: (unicode, io.StringIO, NodeData) -> None

        if not line.endswith(U':'):
            raise ValueError('Missing ":" in line {}'.format(self.line_idx))

        list_id = str_to_int(line.split(U' ', 1)[1][:-1])
        child_node = parent_node.get_child(list_id)
        if child_node is not None and child_node.id != self.NODE_LIST:
            raise ValueError('Duplicate id of list in line {}'.format(self.line_idx))

        list_node = NodeData(list_id, self.NODE_LIST, U'{}'.format(list_id))
        parent_node.add_child(list_id, list_node)
        idx_list_node = NodeData(0xFFFFFFFF, self.NODE_LIST_STAGE, U'{}'.format(0xFFFFFFFF))
        list_node.add_child(0xFFFFFFFF, idx_list_node)

        while True:
            line = fs.readline()
            self.line_idx += 1
            if line == U'':
                print U'Expect "end" command in list!. Line: {}'.format(self.line_idx)
                raise ValueError

            line = remove_dup_space(line.split(U'//')[0].strip())
            if line.startswith(U'end'):
                break

            if line:
                if line == U'*:':
                    idx = self.LIST_STAGE_SAME_TYPE
                elif not line.endswith(U':'):
                    raise ValueError('Missing ":" in line {}'.format(self.line_idx))
                else:
                    idx = str_to_int(line[:-1])

                idx_node = NodeData(idx, self.NODE_STAGE_IDX, U'{}'.format(idx))
                idx_list_node.add_child(idx, idx_node)

                while True:
                    line = fs.readline()
                    self.line_idx += 1

                    if line == U'':
                        print U'Expect "end" command in list!. Line: {}'.format(self.line_idx)
                        raise ValueError

                    line = remove_dup_space(line.split(U'//')[0].strip())
                    if line.startswith(U'end'):
                        break

                    if line.startswith(self.NODE_PROP):
                        self._read_prop(line, fs, idx_node)
                    elif line.startswith(self.NODE_LIST):
                        self._read_list(line, fs, idx_node)
                    elif line.startswith(self.NODE_CMD):
                        self._read_cmd(line, fs, idx_node)

                break

    def _read_prop(self, line, fs, parent_node):
        # type: (unicode, io.StringIO, NodeData) -> None

        if not line.endswith(U':'):
            raise ValueError('Missing ":" in line {}'.format(self.line_idx))

        prop_id = str_to_int(line.split(U' ', 1)[1][:-1])
        child_node = parent_node.get_child(prop_id)
        if child_node is not None and child_node.id != self.NODE_PROP:
            raise ValueError('Duplicate id of prop in line {}'.format(self.line_idx))

        prop_node = NodeData(prop_id, self.NODE_PROP, U'{}'.format(prop_id))
        parent_node.add_child(prop_id, prop_node)
        while True:
            line = fs.readline()
            self.line_idx += 1
            if line == U'':
                print U'Expect "end" command in prop!. Line: {}'.format(self.line_idx)
                raise ValueError

            line = remove_dup_space(line.split(U'//')[0].strip())
            if line.startswith(U'end'):
                break

            if line.startswith(self.NODE_PROP):
                self._read_prop(line, fs, prop_node)
            elif line.startswith(self.NODE_LIST):
                self._read_list(line, fs, prop_node)
            elif line.startswith(self.NODE_CMD):
                self._read_cmd(line, fs, prop_node)
        pass

    def _read_element(self, line, fs):
        # type: (unicode, io.StringIO) -> None

        if not line.endswith(U':'):
            raise ValueError('Missing ":" in line {}'.format(self.line_idx))

        element_id = str_to_int(line.split(U' ', 1)[1][:-1])
        element_node = NodeData(element_id, self.NODE_ELEMENT, U'{}'.format(element_id))
        child_node = self.nodes.get_child(element_id)
        if child_node is not None and child_node.id != self.NODE_ELEMENT:
            raise ValueError('Duplicate id of element in line {}'.format(self.line_idx))
        self.nodes.add_child(element_id, element_node)
        while True:
            line = fs.readline()
            self.line_idx += 1
            if line == U'':
                print U'Expect "end" command in element!. Line: {}'.format(self.line_idx)
                raise ValueError

            line = remove_dup_space(line.split(U'//')[0].strip())
            if line.startswith(U'end'):
                break

            if line.startswith(self.NODE_PROP):
                self._read_prop(line, fs, element_node)
            elif line.startswith(self.NODE_LIST):
                self._read_list(line, fs, element_node)
            elif line.startswith(self.NODE_CMD):
                self._read_cmd(line, fs, element_node)
        pass

    def load(self, file_path):
        fs = io.StringIO(open(file_path, 'rb').read().decode('utf8'))
        while True:
            line = fs.readline()
            self.line_idx += 1
            if line == U'':
                break

            line = remove_dup_space(line.split(U'//')[0].strip())

            if line.startswith(self.NODE_ELEMENT):
                self._read_element(line, fs)
            elif line.startswith(self.NODE_PROP):
                self._read_prop(line, fs, self.nodes)
            elif line.startswith(self.NODE_LIST):
                self._read_list(line, fs, self.nodes)
            elif line.startswith(self.NODE_CMD):
                self._read_cmd(line, fs, self.nodes)
            elif line:
                print U'Skip line {}: "{}"'.format(self.line_idx, line)

    def find_function(self, stack, func_option, args):
        # type: (script.StackInstructionVM, int, unicode) -> Optional[NodeData]
        top_inst = stack.get_value_in_frame()  # push int
        top_inst_value = top_inst.operands[0].value.value
        list_idx = []

        def get_result(funcs_node):
            # type: (NodeData) -> Optional[Tuple]
            funcs_id, overload_dict = funcs_node.data

            r = overload_dict.get(U'{}_{}'.format(func_option, args.replace(U' ', U'').lower()))
            if r is None:
                r = overload_dict.get(U'{}_(...)'.format(func_option))

            if r is None:
                r = overload_dict.get(U'*_{}'.format(args.replace(U' ', U'').lower()))

            if r is None:
                r = overload_dict.get(U'*')

            return r

        node = self.nodes.get_child(top_inst_value)
        if node is None:
            return None
        elif node.name.startswith(self.NODE_CMD):
            return get_result(node)

        idx = 1
        frame_size = stack.frame_size
        push_value = None
        while idx < frame_size:
            inst = stack.get_value_in_frame(idx)
            if inst.opcode == script.Opcode.PUSH:
                v = inst.operands[0].value  # type: script.Variable
                if v.var_type.value == script.VariableType.INT:
                    push_value = v.value

            if push_value is not None:
                parent_node = node
                node = node.get_child(push_value)
                if node is None:
                    m_node = parent_node.get_child(self.LIST_STAGE_SAME_TYPE)
                    if parent_node.name.startswith(self.NODE_LIST_STAGE) and m_node is not None:
                        node = m_node
                        list_idx.append(push_value)
                    else:
                        break

                if node.name.startswith(self.NODE_CMD):
                    n = get_result(node)
                    if n is None:
                        print U'not found: {}, {} - {}'.format(func_option, args, node.data)

                    if n and len(list_idx):
                        n = (n[0], n[1], n[2].format(*list_idx), n[3])
                    return n

                push_value = None
                idx += 1
            else:
                break

        return None
