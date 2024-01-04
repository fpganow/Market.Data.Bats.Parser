`ifndef PYSV_PYSV
`define PYSV_PYSV
package pysv;
import "DPI-C" function chandle MyList_pysv_init();
import "DPI-C" function void MyList_append(input chandle self,
                                           input int value);
import "DPI-C" function void MyList_destroy(input chandle self);
import "DPI-C" function int MyList_get_idx(input chandle self,
                                           input int idx);
import "DPI-C" function int MyList_get_length(input chandle self);
import "DPI-C" function int get_time_(input int sec_since_midnight,
                                      input chandle out_list);
import "DPI-C" function void pysv_finalize();
class PySVObject;
chandle pysv_ptr;
endclass
typedef class MyList;
class MyList extends PySVObject;
  function new(input chandle ptr=null);
    if (ptr == null) begin
      pysv_ptr = MyList_pysv_init();
    end
    else begin
      pysv_ptr = ptr;
    end
  endfunction
  function void append(input int value);
    MyList_append(pysv_ptr, value);
  endfunction
  function void destroy();
    MyList_destroy(pysv_ptr);
  endfunction
  function int get_idx(input int idx);
    return MyList_get_idx(pysv_ptr, idx);
  endfunction
  function int get_length();
    return MyList_get_length(pysv_ptr);
  endfunction
endclass
function int get_time(input int sec_since_midnight,
                      input MyList out_list);
  return get_time_(sec_since_midnight, out_list.pysv_ptr);
endfunction
endpackage
`endif // PYSV_PYSV
