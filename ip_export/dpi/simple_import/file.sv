
module m();

import "DPI-C" function int myFunction(input int v[]);
//import "DPI-C" function int myFunction_2 (input int v[], output int v_out[]);

int i;
int arr[4];
//int dynArr[];
int v_out[];

initial
begin
#1;
  arr = {1, 2, 3, 4};
  v_out = new[3];
  i = myFunction(arr);
//  i = myFunction_2(arr, v_out);
  if( i == 6)
    $display("PASSED");
  else
    $display("FAILED, i=%d", i);

//  dynArr = new[6];
//  dynArr = {8, 9, 10, 11, 12, 13};

/*
  $display("v_out initialized");
  $display("v_out[0]=%d", v_out[0]);
  $display("v_out[1]=%d", v_out[1]);
  $display("v_out[2]=%d", v_out[2]);
*/

  $finish();
end

endmodule
