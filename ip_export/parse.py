#!/usr/bin/python3

from attrs import define
from enum import Enum
from pathlib import Path
import re
import sys


def get_trimmed_name(in_wire: str) -> str:
    if "ctrlind" in in_wire:
        # TODO: Include direction in name and variable index,
        # TODO: Make lowercase

        #print(f'Parsing: {in_wire}')
        result = re.findall(r'ctrlind_(\d{2})_(\D+)', in_wire)
        #print(f'result: {result}')
        var_idx = result[0][0]
        var_name = result[0][1]
        return f'{var_name}_{var_idx}'.lower()
    return in_wire.lower()


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
    direction: Variable.Direction = None
    var_type: Variable.Type = None
    vector_type: Variable.VectorType = None
    vector_size: int = None

    def __str__(self):
        dir_str = "IN" if self.direction == Variable.Direction.IN else "OUT"
        type_str = "std_logic_vector" if self.var_type == Variable.Type.VECTOR else "std_logic"
        var_len = f', {self.vector_size}' if self.var_type == Variable.Type.VECTOR else ""
        return f'{self.name}, {dir_str}, {type_str}{var_len}'



def main(argv):
    if len(argv) == 0:
        print(f'Usage: ./parse.py <filename>.v')
        return

    fin = argv[0]
    print(f'Opening Source File: {fin}')

    #fin = "NiFpgaIPWrapper_bats_parser_ip.vhd"
    if not Path(fin).exists():
        print(f'File {fin} not found')
        sys.exit(1)

#    target_entity = 'NiFpgaIPWrapper_bats_parser_ip'

    vhd_src = Path(fin).read_text()
    #print(f'vhd_src: {vhd_src}')

    target_entity = None
    entity_dict = {}

    entity_src = ""
    reading = False
    for line in vhd_src.split('\n'):
        if line.startswith(f'entity'):
            #entity_obj.name = line.split(' ')[1]
            target_entity = line.split(' ')[1]
            #print(f'TARGET: {target_entity}')
            entity_src += f'{line}\n'
            reading = True
        elif line.startswith(f'end {target_entity};'):
            entity_src += f'{line}\n'
            break
        elif reading is True:
            trim_line = line.strip()
            if trim_line.startswith('port (') or trim_line.startswith(');'):
                #print(f'port line: {trim_line}')
                pass
            else:
                entity_obj = Entity()
                #print(f'Parsing variable info from:\n\t{trim_line}')
                # Variable Name
                var_name_tmp, var_type_tmp = trim_line.split(':')
                entity_obj.name = var_name_tmp.strip()

                # Variable Type
                if 'in ' in var_type_tmp:
                    entity_obj.direction = Variable.Direction.IN
                else:
                    entity_obj.direction = Variable.Direction.OUT

                # Variable Type
                if 'std_logic_vector' in var_type_tmp:
                    result = re.search('.*\((.*)\);', var_type_tmp)
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
                ip_wire_name = get_trimmed_name(entity_obj.name)
                if entity_obj.direction == Variable.Direction.IN:
                    ip_wire_name += '_in'
                else:
                    ip_wire_name += '_out'
                entity_dict[ip_wire_name] = entity_obj
            entity_src += f'{line}\n'


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
        line_str += f'   ip_{key};'

        print(f'{line_str}')

    # Then UUT and wire it up
    tab_stop = '    '
    print('')
    print(f'{tab_stop}{target_entity} UUT (')
    for idx, (key, val) in enumerate(entity_dict.items()):
        tail = ','
        if idx + 1 == len(entity_dict.items()):
            tail = ''
        print(f'{tab_stop*2}.{val.name}(ip_{key}){tail}')
    print(f'{tab_stop});')


if __name__ == "__main__":
    main(sys.argv[1:])
