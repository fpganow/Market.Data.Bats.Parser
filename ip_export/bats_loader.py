import json
from pysv import (
    DataType,
    compile_lib,
    generate_sv_binding,
    sv
)
import sys
from typing import Any

import pitch

##############################################################################
# Custom type for transferring list elements back to SystemVerilog
##############################################################################
class MyList(object):
    @sv()
    def __init__(self):
        self._data = []

    @sv()
    def get_idx(self, idx):
        return self._data[idx]

    @sv()
    def set_idx(self, idx, value):
        if len(self._data) > idx:
            self._data[idx] = value

    @sv()
    def append(self, value):
        self._data.append(value)

    @sv(in_list=DataType.Object)
    def append_list(self, in_list):
        self._data.extend(in_list)

    @sv(in_list=DataType.Object)
    def prepend_list(self, in_list):
        self._data = in_list + self._data[:]

    @sv()
    def get_length(self):
        return len(self._data)

    @sv(no_x=DataType.Int,
            return_type=DataType.String)
    def to_str(self, no_x=False):
        if hasattr(self, '_data') is False:
            return '[]'
        elif self._data is None:
            return '[]'
        try:
            hdr = '0x'
            if no_x is True:
                hdr = ''
            res = '[' + ' '.join([ str.format('{}{:02X}', hdr, x) for x in self._data]) + ']'
        except Exception as ex:
            print(f'Exception in MyList.get_str(...): {ex}')
            sys.stdout.flush()
        return res


##############################################################################
# Wrappers around pitch module functions
##############################################################################
@sv(sec_since_midnight=DataType.Int,
    out_list=MyList,
    prepend=DataType.Bit,
    return_type=DataType.Int)
def get_time(sec_since_midnight: int, out_list: MyList, prepend: bool = False) -> int:
    try:
        parms = {
                "Time": sec_since_midnight
        }
        out_a = pitch.get_time(json.dumps(parms))
        if prepend is True:
            out_list.prepend_list(out_a)
        else:
            out_list.append_list(out_a)
        #out_list.from_bytearray(out_a)
    except Exception as ex:
        print(f'EXCEPTION in get_time(): {ex}')
        sys.stdout.flush()
        return 1
    return 0


@sv()
def get_seq_unit_hdr():
    pass

##############################################################################
# PYSV Related functions
##############################################################################
def compile():
    # compile the a shared_lib into build folder
    # lib_name='pysv'
    # release_build=False
    # clean_up_build=True
    # add_sys_path=False # Whether to add system path
    lib_path = compile_lib([MyList,
                            get_time,
                            get_seq_unit_hdr], cwd="build")

    # generate SV binding
    # pkg_name='pysv'
    # pretty_print=True
    #filename='out_sv_file.sv'
    generate_sv_binding([MyList,
                         get_time,
                         get_seq_unit_hdr], filename="pysv_pkg.sv")

if __name__ == "__main__":
    compile()
