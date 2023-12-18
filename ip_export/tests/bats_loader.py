import json
from pysv import (
    DataType,
    compile_lib,
    generate_sv_binding,
    sv
)
import sys
import numpy
from typing import Any

import pitch

class MyList:
    @sv()
    def __init__(self):
        self._data = []

    @sv()
    def get_idx(self, idx):
        return self._data[idx]

    @sv
    def set_idx(self, idx, value):
        if len(self._data) > idx:
            self._data[idx] = value

    @sv()
    def append(self, value):
        self._data.append(value)

    @sv()
    def get_length(self):
        return len(self._data)

    def from_bytearray(self, in_byte_array):
        self._data = in_byte_array

@sv(in_str=DataType.String,
    in_obj=MyList,
    return_type=DataType.Int)
def get_time(in_Time: str, in_obj) -> int:
    print('-' * 80)
    print("[python] Generating Time message")
    print('-' * 20)
    #print(f'in_obj.get_idx(100): {in_obj.get_idx(0)}')
    try:
        parms = {
                "Time": 12_000
        }
        out_a = pitch.get_time(json.dumps(parms))
    #my_b_arr = bytearray([100, 110, 120])
        in_obj.from_bytearray(out_a)
    except Exception as ex:
        print(f'EXCEPTION: {ex}')
        sys.stdout.flush()
        return 1

    for i in range(in_obj.get_length()):
        print(f'{in_obj.get_idx(i)}')
    print('-' * 80)
    sys.stdout.flush()

    return 0

@sv(in_str=DataType.String,
    in_int=DataType.Int,
    in_flt=DataType.Float,
    return_type=DataType.Int)
def get_time2(in_str: str,
             in_int: int,
             in_flt: float) -> int:
    print('-' * 80)
    print("Generating Time message")
    print('-' * 80)
    print('Input parameters:')
    print(f'   - in_str = {in_str}')
    print(f'   - in_int = {in_int}')
    print(f'   - in_flt = {in_flt}')
    print('-' * 80)
    sys.stdout.flush()
    return 12

#    print(f'   - in_obj = {in_obj}')
#    print(f'   - in_arr_int = {in_arr_int}')
#    out_bytes = numpy.array([1, 2, 3, 4])
#    bw = ByteWrapper(100)
#    return in_obj.get_idx(25)

# compile the a shared_lib into build folder
lib_path = compile_lib([MyList, get_time, get_time2], cwd="build")
# generate SV binding
generate_sv_binding([MyList, get_time, get_time2], filename="pysv_pkg.sv")
