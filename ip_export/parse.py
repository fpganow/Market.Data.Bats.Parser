#!/usr/bin/python3

from attrs import define
from enum import Enum
from pathlib import Path
import re
import sys


class Variable:
    class Direction(Enum):
        IN = 0
        OUT = 1
    class Type(Enum):
        SCALAR = 0
        VECTOR = 1
    class VectorType(Enum):
        ASCENDING = 0
        DESCENDING = 1


@define
class Entity:
    name: str = None
    port_name: str = None
    direction: Variable.Direction = None
    var_type: Variable.Type = None
    vector_type: Variable.VectorType = None
    vector_size: int = None

    def __str__(self):
        dir_str = "IN" if self.direction == Variable.Direction.IN else "OUT"
        type_str = "std_logic_vector" if self.var_type == Variable.Type.VECTOR else "std_logic"
        var_len = f', {self.vector_size}' if self.var_type == Variable.Type.VECTOR else ""
        return f'{self.port_name:40} -> {self.name:40}, {dir_str}, {type_str}{var_len}'

def get_connector_name(in_entity: Entity) -> str:

    if "ctrlind" in in_entity.port_name:

        ip_wire_name = 'out_ip_'
        if in_entity.direction == Variable.Direction.IN:
            ip_wire_name = 'in_ip_'

        #print(f'Parsing: {in_wire}')
        result = re.findall(r'ctrlind_(\d{2})_([a-zA-Z0-9_]+)', in_entity.port_name)
        #print(f'result: {result}')
        #var_idx = result[0][0]
        ip_wire_name += result[0][1]
        return f'{ip_wire_name}'.lower()

    # Non control/indicator ports, reset, enable_in, enable_clr, enable_out, Clk40...

    return in_entity.port_name.lower()


def main(argv):
    if len(argv) == 0:
        print(f'Usage: ./parse.py <filename>.v')
        return

    fin = argv[0]
    tab_stop = '    '
    print(f'{tab_stop}// AUTO_GENERATED_CODE_START: parse.py {argv}')
    print(f'{tab_stop}// Source file: {fin}')

    if not Path(fin).exists():
        print(f'File {fin} not found')
        sys.exit(1)

    vhd_src = Path(fin).read_text()

    target_entity = None
    entity_dict = {}

    reading = False
    for line in vhd_src.split('\n'):
        if line.startswith(f'entity'):
            target_entity = line.split(' ')[1]
            reading = True
        elif line.startswith(f'end {target_entity};'):
            break
        elif reading is True:
            trim_line = line.strip()
            # Ignore non-variable lines
            if trim_line.startswith('port (') or trim_line.startswith(');'):
                pass
            else:
                entity_obj = Entity()
                #print(f'Parsing variable info from:\n\t{trim_line}')
                # Variable Name
                port_name, port_type = trim_line.split(':')
                entity_obj.port_name = port_name.strip()

                # Variable Type
                if 'in ' in port_type:
                    entity_obj.direction = Variable.Direction.IN
                else:
                    entity_obj.direction = Variable.Direction.OUT

                # Variable Type
                if 'std_logic_vector' in port_type:
                    result = re.search('.*\((.*)\);', port_type)
                    first_bound, type_str, second_bound =  result.group(1).split(' ')

                    entity_obj.var_type = Variable.Type.VECTOR

                    if  'to' == type_str:
                        entity_obj.vector_type = Variable.VectorType.ASCENDING
                        entity_obj.vector_size = int(second_bound) - int(first_bound) + 1
                    elif 'downto' == type_str:
                        entity_obj.vector_type = Variable.VectorType.DESCENDING
                        entity_obj.vector_size = int(first_bound) - int(second_bound) + 1
                else:
                    entity_obj.var_type = Variable.Type.SCALAR
                entity_obj.name = get_connector_name(entity_obj)

                entity_dict[port_name] = entity_obj
                #print(f'{entity_obj}')

    # Generate code for instantiating this ip
    # First reg/wire declarations
    #  - reg for input
    #  - wire for output
    print(f'    // Variables for {target_entity}')
    for key, val in entity_dict.items():
        line_str = "    "
        if val.direction == Variable.Direction.IN:
            line_str += "reg    "
        elif val.direction == Variable.Direction.OUT:
            line_str += "wire   "
        if val.var_type == Variable.Type.VECTOR:
            line_str += f'[{val.vector_size-1:2}:0] '
        else:
            line_str += ' ' * 7
        line_str += f'   {val.name};'

        print(f'{line_str}')

    # Then UUT and wire it up
    print('')
    print(f'{tab_stop}{target_entity} UUT (')
    # key is port/signal name
    for idx, (key, val) in enumerate(entity_dict.items()):
        tail = ','
        if idx + 1 == len(entity_dict.items()):
            tail = ''
        print(f'{tab_stop*2}.{val.port_name}({val.name}){tail}')
    print(f'{tab_stop});')
    print(f'{tab_stop}// AUTO_GENERATED_CODE_END: parse.py')

if __name__ == "__main__":
    main(sys.argv[1:])
