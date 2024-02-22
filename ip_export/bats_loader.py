import json
import math
from pysv import (
    DataType,
    compile_lib,
    generate_sv_binding,
    sv
)
import sys
from typing import Any, List

import cboe_pitch

#TODO: Implement the following functions
#  [x]  get_seq_unit_hdr
#  [x]  get_time
#  [] get_add_order_long
#  [] get_add_order_short
#  [] get_add_order_expanded
#  [] get_order_executed
#  [] get_order_executed_at_price_size
#  [] get_reduce_size_long
#  [] get_reduce_size_short
#  [] get_modify_order_long
#  [] get_modify_order_short
#  [] get_delete_order
#  [] get_trade_long
#  [] get_trade_short
#  [] get_trade_expanded


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
    def replace_list(self, in_py_list):
        self._data = in_py_list

    @sv()
    def get_length(self):
        return len(self._data)

    @sv()
    def get_num_words(self):
        return ((len(self._data) // 8) + (len(self._data) % 8 > 0))

    @sv()
    def is_aligned(self):
        return (len(self._data) % 8 == 0)

    @sv(index=DataType.Int,
        return_type=DataType.ULongInt)
    def get_word(self, index):
        final_word = 0
        try:
            data_to_copy = self._data.copy()

            start_idx = index * 8
            stop_idx = start_idx + 8
            if start_idx + 8 > len(data_to_copy):
                stop_idx = len(data_to_copy)

            for i in range(start_idx, stop_idx):
                final_word = (final_word << 8) | data_to_copy[i]

            num_zeros = 8 - (stop_idx - start_idx)
            # Add padding
            for i in range(num_zeros):
                final_word = (final_word << 8) | 0

        except Exception as EX:
            print(f'Exception in MyList.get_word(..): {ex}')
            sys.stdout.flush()

        return final_word

    @sv(index=DataType.Int,
        return_type=DataType.UInt)
    def get_byte_enables(self, index):
        start_idx = index * 8
        stop_idx = start_idx + 8
        if start_idx + 8 > len(self._data):
            stop_idx = len(self._data)

        num_zeros = 8 - (stop_idx - start_idx)
        print(f'num_zeroes: {num_zeros}')
        casted = (0xff << num_zeros) & 0xf
        print(f'casted: {hex(casted)} - {bin(casted)}')
        return (0xff << num_zeros) & 0xff

    @sv()
    def from_array(self, in_list):
        self._data = in_list

    @sv(return_type=DataType.Int)
    def to_array(self) -> int:
        return self._data

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
def post_process(out_list: MyList) -> None:
    pass


#  - AddOrder
@sv(sec_since_midnight=DataType.Int,
    out_list=MyList,
    prepend=DataType.Bit,
    return_type=DataType.Int)
def get_time(sec_since_midnight: int,
             out_list: MyList,
             prepend: bool = False) -> int:
    try:
        parms = {
                "Time": sec_since_midnight
        }
        out_a = cboe_pitch.get_time(json.dumps(parms))
        if prepend is True:
            out_list.prepend_list(out_a)
        else:
            out_list.append_list(out_a)
    except Exception as ex:
        print(f'EXCEPTION in cboe_pitch.get_time(): {ex}')
        sys.stdout.flush()
        return 1
    return 0


@sv(time_offset=DataType.Int,
    order_id=DataType.String,
    side_indicator=DataType.String,
    quantity=DataType.Int,
    symbol=DataType.String,
    price=DataType,
    out_list=MyList,
    prepend=DataType.Bit,
    return_type=DataType.Int)
def get_add_order_long(time_offset: int,
                       order_id: str,
                       side_indicator: str,
                       quantity: int,
                       symbol: str,
                       price: float,
                       out_list: MyList,
                       prepend: bool = False) -> int:
    try:
        parms = {
            "Time Offset": time_offset,
            "Order Id": order_id,
            "Side Indicator": side_indicator,
            "Quantity": quantity,
            "Symbol": symbol,
            "Price": price,
        }
        out_a = cboe_pitch.get_add_order_long(json.dumps(parms))
        if prepend is True:
            out_list.prepend_list(out_a)
        else:
            out_list.append_list(out_a)
    except Exception as ex:
        print(f'EXCEPTION in cboe_pitch.get_add_order_long(): {ex}')
        sys.stdout.flush()
        return 1
    return 0


@sv(time_offset=DataType.Int,
    order_id=DataType.String,
    side_indicator=DataType.String,
    quantity=DataType.Int,
    symbol=DataType.String,
    price=DataType,
    out_list=MyList,
    prepend=DataType.Bit,
    return_type=DataType.Int)
def get_add_order_short(time_offset: int,
                       order_id: str,
                       side_indicator: str,
                       quantity: int,
                       symbol: str,
                       price: float,
                       out_list: MyList,
                       prepend: bool = False) -> int:
    try:
        parms = {
            "Time Offset": time_offset,
            "Order Id": order_id,
            "Side Indicator": side_indicator,
            "Quantity": quantity,
            "Symbol": symbol,
            "Price": price,
        }
        out_a = cboe_pitch.get_add_order_short(json.dumps(parms))
        if prepend is True:
            out_list.prepend_list(out_a)
        else:
            out_list.append_list(out_a)
    except Exception as ex:
        print(f'EXCEPTION in cboe_pitch.get_add_order_short(): {ex}')
        sys.stdout.flush()
        return 1
    return 0


@sv(time_offset=DataType.Int,
    order_id=DataType.String,
    side_indicator=DataType.String,
    quantity=DataType.Int,
    symbol=DataType.String,
    price=DataType,
    out_list=MyList,
    prepend=DataType.Bit,
    return_type=DataType.Int)
def get_add_order_expanded(time_offset: int,
                       order_id: str,
                       side_indicator: str,
                       quantity: int,
                       symbol: str,
                       price: float,
                       out_list: MyList,
                       prepend: bool = False) -> int:
    try:
        parms = {
            "Time Offset": time_offset,
            "Order Id": order_id,
            "Side Indicator": side_indicator,
            "Quantity": quantity,
            "Symbol": symbol,
            "Price": price,
        }
        out_a = cboe_pitch.get_add_order_expanded(json.dumps(parms))
        if prepend is True:
            out_list.prepend_list(out_a)
        else:
            out_list.append_list(out_a)
    except Exception as ex:
        print(f'EXCEPTION in cboe_pitch.get_add_order_expanded(): {ex}')
        sys.stdout.flush()
        return 1
    return 0

@sv(hdr_seq=DataType.Int,
    hdr_count=DataType.Int,
    msgs_array=MyList,
    return_type=DataType.Int)
def get_seq_unit_hdr(hdr_seq: int, hdr_count: int, msgs_array: MyList) -> bool:
    """
    Will call cboe_pitch.get_seq_unit_hdr with a parameters dictionary (JSON)
    and with a list representing the raw bytes of all messages to be included
    in the Sequenced Unit Header.  Parameters should have the following format:
        hdr_seq
        hdr_count
        msgs_array
    """
    try:
        parms = {
            "HdrSeq": hdr_seq,
            "HdrCount": hdr_count
        }

        # copy msgs_array to temp_array
        temp_array = msgs_array._data
        seq_unit_hdr_arr = cboe_pitch.get_seq_unit_hdr(json.dumps(parms),
                                        msgs_array=temp_array)
        msgs_array.replace_list(seq_unit_hdr_arr)
    except Exception as ex:
        print(f'EXCEPTION in cboe_pitch.get_seq_unit_hdr(): {ex}')
        sys.stdout.flush()
        return 1

    return 0


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
