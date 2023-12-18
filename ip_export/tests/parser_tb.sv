`include "pysv_pkg.sv"


import pysv::*;

module m();

import "DPI-C" function int dpi_function(input int v[], output int v_out[]);

int i;
int arr[4];
int dynArr[];
int v_out[];
int out_bytes;
string my_str = "Hello_STRING";

initial
begin
  MyList foo;

  #1;

  arr = {1, 2, 3, 4};
  v_out = new[3];
  v_out = {1, 2, 3};
  i = dpi_function(arr, v_out);
  if( i == 6)
    $display("PASSED");
  else
    $display("FAILED, i=%d", i);

  foo = new();
  foo.append(100);
  $display("foo.get_idx(0) = %d", foo.get_idx(0));
  get_time("Hello", foo);

  for (i=0; i< foo.get_length(); i++)
  begin
      $display(" got [%d] = %d", i, foo.get_idx(i));
  end
  //$display("foo.get_idx(12) = %d", foo.get_idx(12));
  $display("----------------------------------------------------------------");
  $display("  End of TEST BENCH  ");
  $display("----------------------------------------------------------------");
//  get_time2("BATS_TIME", 100, 99.75);

//  $display("get_time=%d", i);
//  dynArr = new[6];
//  dynArr = {8, 9, 10, 11, 12, 13};

/*
  $display("v_out initialized");
  $display("v_out[0]=%d", v_out[0]);
  $display("v_out[1]=%d", v_out[1]);
  $display("v_out[2]=%d", v_out[2]);
*/
//  bw.destroy();


  pysv_finalize();
  $finish();
end

endmodule
