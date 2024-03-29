`timescale 1ns / 1ps

`include "pysv_pkg.sv"
import pysv::*;

//////////////////////////////////////////////////////////////////////////////////
// 
// Create Date: 03/16/2021 09:23:26 PM
// Module Name: bats_parser_tb
// Description: 
// 
// 
//////////////////////////////////////////////////////////////////////////////////

module bats_parser_tb();

    // 10ns = 100 MHz
    // 20ns = 50 MHz
    // 25ns = 40MHz
    // duration for each bit = 20 * timescale = 20 * 1 ns = 20 ns
    localparam period = 25;
    localparam duty_cycle = period / 2;

    reg clk40;

    always
    begin
        clk40 = 1'b1;
        #duty_cycle;

        clk40 = 1'b0;
        #duty_cycle;
    end

    // Variables for NiFpgaIPWrapper_bats_parser_ip
    // reset: asynchronous reset (active high)
    // enable_in: Must be synchronous to base clock.  Assert to
    //            start running the IP, must remain asserted
    //            when the IP is running.  Deassert when resetting
    //            the IP.
    // enable_out: Ignore this for free running IP. Otherwise it is
    //             asserted when the IP has stopped.
    // enable_clr: Assert for one cycle to prepare IP for a single shot.
    // AUTO_GENERATED_CODE_START: parse.py ['./NiFpgaIPWrapper_bats_parser_ip.vhd']
    // Source file: ./NiFpgaIPWrapper_bats_parser_ip.vhd
    // Variables for NiFpgaIPWrapper_bats_parser_ip
    reg              reset;
    reg              enable_in;
    wire             enable_out;
    reg              enable_clr;
    // Control
    reg    [ 0:0]    in_ip_reset;
    reg    [63:0]    in_ip_bytes;
    wire   [ 0:0]    out_ip_ready_for_udp_input;
    wire   [63:0]    out_ip_bytes_echo;
    wire   [ 7:0]    out_ip_bytes_valid;
    // Debug
    reg    [ 0:0]    in_ip_ready_for_debug;
    wire   [ 0:0]    out_ip_debug_valid;
    wire   [63:0]    out_ip_debug_element;
    reg    [ 7:0]    in_ip_byte_enables;
    reg    [ 0:0]    in_ip_data_valid;
    // OrderBook.Command
    reg    [ 0:0]    in_ip_ready_for_orderbook_command;
    wire   [ 0:0]    out_ip_orderbook_command_valid;

    wire   [ 7:0]    out_ip_orderbook_command_type;
    wire   [ 7:0]    out_ip_side_u8;
    wire   [63:0]    out_ip_order_id_u64;
    wire   [31:0]    out_ip_quantity_u32;
    wire   [63:0]    out_ip_symbol_u64;
    wire   [63:0]    out_ip_price_u64;
    wire   [31:0]    out_ip_executed_quantity_u32;
    wire   [31:0]    out_ip_canceled_quantity_u32;
    wire   [31:0]    out_ip_remaining_quantity_u32;
    wire   [63:0]    out_ip_seconds_u64;
    wire   [63:0]    out_ip_nanoseconds_u64;
    wire   [ 0:0]    out_ip_add;
    wire   [ 0:0]    out_ip_edit;
    wire   [ 0:0]    out_ip_remove;
    wire   [31:0]    out_ip_seq_no;

    NiFpgaIPWrapper_bats_parser_ip UUT (
        .reset(reset),
        .enable_in(enable_in),
        .enable_out(enable_out),
        .enable_clr(enable_clr),
        // Debug
        .ctrlind_00_Ready_For_Debug(in_ip_ready_for_debug),
        .ctrlind_01_Debug_Valid(out_ip_debug_valid),
        .ctrlind_02_Debug_Element(out_ip_debug_element),
        // Control
        .ctrlind_03_Ready_for_OrderBook_Command(in_ip_ready_for_orderbook_command),
        // OrderBook.Command
        .ctrlind_04_OrderBook_Command_Valid(out_ip_orderbook_command_valid),
        .ctrlind_05_seq_no(out_ip_seq_no),
        .ctrlind_06_Remove(out_ip_remove),
        .ctrlind_07_Edit(out_ip_edit),
        .ctrlind_08_Add(out_ip_add),
        .ctrlind_09_Nanoseconds_U64(out_ip_nanoseconds_u64),
        .ctrlind_10_Seconds_U64(out_ip_seconds_u64),
        .ctrlind_11_Remaining_Quantity_U32(out_ip_remaining_quantity_u32),
        .ctrlind_12_Canceled_Quantity_U32(out_ip_canceled_quantity_u32),
        .ctrlind_13_Executed_Quantity_U32(out_ip_executed_quantity_u32),
        .ctrlind_14_Price_U64(out_ip_price_u64),
        .ctrlind_15_Symbol_U64(out_ip_symbol_u64),
        .ctrlind_16_Quantity_U32(out_ip_quantity_u32),
        .ctrlind_17_Order_Id_U64(out_ip_order_id_u64),
        .ctrlind_18_Side_U8(out_ip_side_u8),
        .ctrlind_19_OrderBook_Command_Type(out_ip_orderbook_command_type),
        .ctrlind_20_reset(in_ip_reset),
        .ctrlind_21_Bytes(in_ip_bytes),
        .ctrlind_22_Byte_Enables(in_ip_byte_enables),
        .ctrlind_23_data_valid(in_ip_data_valid),
        .ctrlind_24_Ready_for_Udp_Input(out_ip_ready_for_udp_input),
        .ctrlind_25_Bytes_echo(out_ip_bytes_echo),
        .ctrlind_26_Bytes_Valid(out_ip_bytes_valid),
        .Clk40(clk40)
    );
    // AUTO_GENERATED_CODE_END: parse.py

    initial
    begin
        MyList my_list;
        int ret;
        longint i_word;
        int i;
        // Set default control signal values
        reset = 0;
        enable_in = 0;
        enable_clr = 0;
        // Set default values
        //   Ready.For.Orderbook.Command
        //   reset_in
        //   data_in
        //   data_valid
        reset = 0;
        in_ip_reset = 0;
        in_ip_ready_for_orderbook_command = 1;
        in_ip_ready_for_debug = 1;
        in_ip_data_valid = 0;
        in_ip_byte_enables = 8'h0;
        in_ip_bytes = 64'h00000000;

        // Reset IP
        reset = 1;
        #(period*50);
        $display("Reset IP");

        enable_in = 1;
        reset = 0;
        #(period*40);

        // Enable IP
        enable_in = 1;
        #(period*20);

        // LabVIEW/Code Reset
        in_ip_reset = 1;
        #(period);

        in_ip_reset = 0;
        #(period*5);

        $display("+=================================================================================+");
        $display("|  Hard-coded Sequenced Unit Header                                               |");
        $display("+---------------------------------------------------------------------------------+");
        $display("  Test #1 - Send hard-coded Sequenced Unit Header");
        $display("    - 1st WORD");
        in_ip_data_valid = 1;
        in_ip_byte_enables = 8'b11111111;
        in_ip_bytes = 64'h0e00010102000000;
        $display("    - 2nd WORD");
        #(period*1);
        in_ip_data_valid = 1;
        in_ip_byte_enables = 8'b11111100;
        in_ip_bytes = 64'h062020d206000000;
        $display("    - Clear data_valid");
        #(period*1);
        in_ip_data_valid = 0;
        in_ip_byte_enables = 8'b00000000;
        in_ip_bytes = 64'h0000000000000000;

        $display("    + Assert result");
        #(period*1);
        wait (out_ip_orderbook_command_valid == 1);
        $display("    - out_ip_orderbook_command_valid: %d",
                        out_ip_orderbook_command_valid);
        $display("    - out_ip_seconds_u64: %d (0x%x)",
                        out_ip_seconds_u64,
                        out_ip_seconds_u64);
        $display("    - out_ip_orderbook_command_type: %d",
                        out_ip_orderbook_command_type);

        $display("+=================================================================================+");
        $display("|  Testing PYSV                                                                   |");
        $display("+---------------------------------------------------------------------------------+");

        // Test #1 - Create Custom List via PYSV
        $display("  Test #1 - Create List via PYSV");
        my_list = new();
        my_list.append(100);
        my_list.append(200);
        my_list.append(300);
        my_list.append(400);
        $display("  -  Length = %0d", my_list.get_length());
        assert (my_list.get_length() == 4);
        $display("  -  Bytes = %s", my_list.to_str(0));
        assert (my_list.to_str(0) == "[0x64 0xC8 0x12C 0x190]") else $error("Assertion failed %s", my_list.to_str(0));
        assert (my_list.get_idx(0) == 100);
        assert (my_list.get_idx(1) == 200);
        assert (my_list.get_idx(2) == 300);
        assert (my_list.get_idx(3) == 400);
        $display("  *  Passed");

        // Test #2 - Create List, Append and Prepend to it
        $display("+---------------------------------------------------------------------------------+");
        $display("  Test #2 - Create List, Append and Prepend to it");
        my_list = new();
        $display("  - Generating and appending 1st Time message");
        ret = get_time(34200, my_list, 0);
        $display("  - Length = %0d", my_list.get_length());
        assert (my_list.get_length() == 6);
        assert (my_list.to_str(0) == "[0x06 0x20 0x98 0x85 0x00 0x00]") else $error("Assertion failed %s", my_list.to_str(0));
        $display("  - Generating and prepending 2nd Time message");
        ret = get_time(34201, my_list, 1);
        assert (my_list.to_str(0) == "[0x06 0x20 0x99 0x85 0x00 0x00 0x06 0x20 0x98 0x85 0x00 0x00]") else 
            $error("Assertion failed %s", my_list.to_str(0));
        $display("  *  Passed");

        // Test #3 - Create Time Message and prepend appropriate Seq Unit Header
        $display("+---------------------------------------------------------------------------------+");
        $display("  Test #3 - Create Time Message and prepend appropriate Seq Unit Header");
        $display("  -  Time = 35,199");
        my_list = new();
        ret = get_time(35199, my_list, 0);
        assert (my_list.get_length() == 6);
        assert (my_list.to_str(0) == "[0x06 0x20 0x7F 0x89 0x00 0x00]") else
            $error("Invalid bytes for Time message: %s", my_list.to_str(0));

        ret = get_seq_unit_hdr(1, 1, my_list);
        assert (ret == 0) else $display("Bad exit code");
        assert (my_list.get_length() == 14) else 
            $error("Bad length, was %d", my_list.get_length());
        assert (my_list.to_str(0) == "[0x0E 0x00 0x02 0x01 0x01 0x00 0x00 0x00 0x06 0x20 0x7F 0x89 0x00 0x00]") else 
            $error("Invalid bytes for Sequenced Unit Header, %s", my_list.to_str(0));
        // TODO: How can systemverilog know if a previous assertion failed and make this 'passed' mean something?
            // -? External library such as VUnit? https://vunit.github.io/user_guide.html
        $display("  *  Passed");

        // Test #4 - Use SeqUnitHdr with single Time Message, pass through BATS.Parser IP
        $display("+---------------------------------------------------------------------------------+");
        $display("  Test #4 - Create SeqUnitHdr with single Time Message, pass through BATS.Parser IP");
        my_list = new();
        ret = get_time(32199, my_list, 0);
        ret = get_seq_unit_hdr(1, 1, my_list);
        assert (ret == 0);
        $display("  -  Return value = %0d", ret);
        assert (my_list.get_length() == 14);
        $display("  -  Length = %0d", my_list.get_length());

        i_word = my_list.get_word(0);
        $display("  -  i_word[0] = 0x%0x", i_word);

        in_ip_data_valid = 1;
        in_ip_byte_enables = 8'b11111111;        
        in_ip_bytes = i_word;

        #(period*1);
        i_word = my_list.get_word(1);
        in_ip_data_valid = 1;
        in_ip_byte_enables = 8'b11111100;
        in_ip_bytes = i_word;

        #(period*1);
        in_ip_data_valid = 0;
        in_ip_byte_enables = 8'b00000000;
        in_ip_bytes = 64'h0000000000000000;

        $display("  - Sent 2nd Test time message");
        $display("    Results:");
        wait (out_ip_orderbook_command_valid == 1);
        $display("    - out_ip_orderbook_command_valid: %d",
                        out_ip_orderbook_command_valid);
        assert (out_ip_seconds_u64 == 32199);
        $display("    - out_ip_seconds_u64: %d (0x%x)",
                        out_ip_seconds_u64,
                        out_ip_seconds_u64);
        assert (out_ip_orderbook_command_type == 0);
        $display("    - out_ip_orderbook_command_type: %d",
                        out_ip_orderbook_command_type);

        pysv_finalize();
        $display("+---------------------------------------------------------------------------------+");
        $display("|  Finished Testing PYSV                                                          |");
        $display("+---------------------------------------------------------------------------------+");
// */

        $display("----------------------------------------------------------------");
        $display("  End of TEST BENCH  ");
        $display("----------------------------------------------------------------");

/*
        wait (out_ip_orderbook_command_valid == 1);
        assert (out_ip_seconds_u64 == 64'h000000000006d219);
*/

        $finish;
    end
endmodule
