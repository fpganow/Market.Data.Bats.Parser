`timescale 1ns / 1ps

`include "pysv_pkg.sv"
import pysv::*;

module parser_tb();

initial
begin
  MyList my_list;
  int i;

  #10;

  // Test out custom list first
  my_list = new();
  my_list.append(100);
  $display("my_list.get_idx(0) = %d", my_list.get_idx(0));

  // Now get the bytes array

  get_time(34200, my_list);

  // Validate results
  for (i=0; i<my_list.get_length(); i++)
  begin
      $display(" got [%d] = %d", i, my_list.get_idx(i));
  end
//*/
  $display("----------------------------------------------------------------");
  $display("  End of TEST BENCH  ");
  $display("----------------------------------------------------------------");

  pysv_finalize();

  $finish();
end

endmodule
