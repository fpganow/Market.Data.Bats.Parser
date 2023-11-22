
module m();

import "DPI-C" pure function int myFunction (input int v[]);

int i;
int arr[4];
int dynArr[];

initial
begin
#1;
  arr = '{4, 5, 6, 7}';
  i = myFunction(arr);
  if( i == 6)
    $display("PASSED");
  else
    $display("FAILED");

  dynArr = new[6];
  dynArr = '{8, 9, 10, 11, 12, 13}';

  $finish();
end


endmodule
