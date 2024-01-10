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

class MyList:
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

    @sv()
    def get_length(self):
        return len(self._data)

    @sv()
    def from_bytearray(self, in_byte_array):
        self._data = in_byte_array


def test_get_time():
    from hamcrest import assert_that, equal_to
    # GIVEN
    time_in_s = 34_200
    my_list = MyList();
    my_list.append(100)

    # WHEN
    get_time(34200, my_list);

    # THEN
    assert_that(my_list.get_length(), equal_to(6))


@sv(sec_since_midnight=DataType.Int,
    out_list=MyList,
    return_type=DataType.Int)
def get_time(sec_since_midnight: int, out_list: MyList) -> int:
    print('-' * 80)
    print("[python] Generating Time message")
    print('-' * 20)
    print(f'out_list.get_idx(100): {out_list.get_idx(0)}')
    try:
        parms = {
                "Time": sec_since_midnight
        }
        out_a = pitch.get_time(json.dumps(parms))
        out_list.from_bytearray(out_a)
    except Exception as ex:
        print(f'EXCEPTION in get_time(): {ex}')
        sys.stdout.flush()
        return 1

    for i in range(out_list.get_length()):
        print(f'{out_list.get_idx(i)}')
    print('-' * 80)
    sys.stdout.flush()

    return 0

def compile():
    # compile the a shared_lib into build folder
    lib_path = compile_lib([MyList, get_time], cwd="build")

    # generate SV binding
    generate_sv_binding([MyList, get_time], filename="pysv_pkg.sv")

if __name__ == "__main__":
    compile()
