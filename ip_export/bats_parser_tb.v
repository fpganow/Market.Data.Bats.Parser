`timescale 1ns / 1ps
//ip_bytes_18_in = 64'h0e0001010100000l;
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03/16/2021 09:23:26 PM
// Design Name: 
// Module Name: bats_parser_tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module bats_parser_tb;

    // 10ns = 100 MHz
    // 20ns = 50 MHz
    // 25ns = 40MHz
    // duration for each bit = 20 * timescale = 20 * 1 ns = 20 ns
    localparam period = 25;
    localparam duty_cycle = period / 2;

    reg clk;

    always
    begin
        clk = 1'b1;
        #duty_cycle;

        clk = 1'b0;
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
    // AUTO_GENERATED CODE: parse.py
    // Variables for NiFpgaIPWrapper_bats_parser_ip
    reg              ip_reset_in;
    reg              ip_enable_in_in;
    wire             ip_enable_out_out;
    reg              ip_enable_clr_in;
    reg    [ 0:0]    ip_ready_for_debug_00_in;
    wire   [ 0:0]    ip_debug_valid_01_out;
    wire   [63:0]    ip_debug_element_02_out;
    reg    [ 0:0]    ip_ready_for_orderbook_command_03_in;
    wire   [ 0:0]    ip_orderbook_command_valid_04_out;
    wire   [63:0]    ip_nanoseconds_u_05_out;
    wire   [63:0]    ip_seconds_u_06_out;
    wire   [31:0]    ip_remaining_quantity_u_07_out;
    wire   [31:0]    ip_canceled_quantity_u_08_out;
    wire   [31:0]    ip_executed_quantity_u_09_out;
    wire   [63:0]    ip_price_u_10_out;
    wire   [63:0]    ip_symbol_u_11_out;
    wire   [31:0]    ip_quantity_u_12_out;
    wire   [63:0]    ip_order_id_u_13_out;
    wire   [ 7:0]    ip_side_u_14_out;
    wire   [ 7:0]    ip_orderbook_command_type_15_out;
    reg    [ 0:0]    ip_data_valid_16_in;
    reg    [ 7:0]    ip_byte_enables_17_in;
    reg    [63:0]    ip_bytes_18_in;
    reg    [ 0:0]    ip_reset_19_in;
    wire   [ 0:0]    ip_ready_for_udp_input_20_out;
//    reg              ip_clk40_in;

    NiFpgaIPWrapper_bats_parser_ip UUT (
        .reset(ip_reset_in),
        .enable_in(ip_enable_in_in),
        .enable_out(ip_enable_out_out),
        .enable_clr(ip_enable_clr_in),
        .ctrlind_00_Ready_For_Debug(ip_ready_for_debug_00_in),
        .ctrlind_01_Debug_Valid(ip_debug_valid_01_out),
        .ctrlind_02_Debug_Element(ip_debug_element_02_out),
        .ctrlind_03_Ready_for_OrderBook_Command(ip_ready_for_orderbook_command_03_in),
        .ctrlind_04_OrderBook_Command_Valid(ip_orderbook_command_valid_04_out),
        .ctrlind_05_Nanoseconds_U64(ip_nanoseconds_u_05_out),
        .ctrlind_06_Seconds_U64(ip_seconds_u_06_out),
        .ctrlind_07_Remaining_Quantity_U32(ip_remaining_quantity_u_07_out),
        .ctrlind_08_Canceled_Quantity_U32(ip_canceled_quantity_u_08_out),
        .ctrlind_09_Executed_Quantity_U32(ip_executed_quantity_u_09_out),
        .ctrlind_10_Price_U64(ip_price_u_10_out),
        .ctrlind_11_Symbol_U64(ip_symbol_u_11_out),
        .ctrlind_12_Quantity_U32(ip_quantity_u_12_out),
        .ctrlind_13_Order_Id_U64(ip_order_id_u_13_out),
        .ctrlind_14_Side_U8(ip_side_u_14_out),
        .ctrlind_15_OrderBook_Command_Type(ip_orderbook_command_type_15_out),
        .ctrlind_16_data_valid(ip_data_valid_16_in),
        .ctrlind_17_Byte_Enables(ip_byte_enables_17_in),
        .ctrlind_18_Bytes(ip_bytes_18_in),
        .ctrlind_19_reset(ip_reset_19_in),
        .ctrlind_20_Ready_for_Udp_Input(ip_ready_for_udp_input_20_out),
        .Clk40(clk)
    );
    // AUTO_GENERATED CODE: parse.py

    integer fptr;
    integer scan_faults;

    initial
    begin
        // Set default control signal values
        ip_reset_in = 0;
        ip_enable_in_in = 0;
        ip_enable_clr_in = 0;
        // Set default values
        //   Ready.For.Orderbook.Command
        //   reset_in
        //   data_in
        //   data_valid
        ip_reset_19_in = 0;
        ip_ready_for_orderbook_command_03_in = 1;
        ip_ready_for_debug_00_in = 1;

        // Reset IP
        ip_reset_in = 1;
        #(period*50);

        ip_enable_in_in = 1;
        ip_reset_in = 0;
        #(period*40);

        // Enable IP
        ip_enable_in_in = 1;
        #(period*20);

        // LabVIEW/Code Reset
        ip_reset_19_in = 1;
        #(period);
        
        ip_reset_19_in = 0;
        #(period*5);

        // Most basic test - Sequenced Unit Header with Time
        ip_data_valid_16_in = 1;
        ip_byte_enables_17_in = 8'b11111111;        
        ip_bytes_18_in = 64'h000000020101000e;

        #(period*1);
        ip_data_valid_16_in = 1;
        ip_byte_enables_17_in = 8'b00111111;
        ip_bytes_18_in = 64'h00000006d2192006;

        #(period*1);
        ip_data_valid_16_in = 0;
        ip_byte_enables_17_in = 8'b00000000;
        ip_bytes_18_in = 64'h0000000000000000;

        wait (ip_orderbook_command_valid_04_out == 1);
//    reg    [63:0]    ip_bytes_18_in;
        // Sequenced Unit Header
        // Hdr Len  (2) - Including this header
        // Hdr Cnt  (1)
        // Hdr Unit (1)
        // Hdr Seq  (4)
        // 0E00  0101  0100 0000
        // Time -> 34,200 = 9:30 AM
        // 0620  9885  0000  0000


//        fptr = $fopen("raw.pitch.dat", "rb");
//        if(fptr == 0)
//        begin
//            $display("raw.pitch.dat was NULL");
//            $finish;
//        end
//        while (!$feof(fptr))
//        begin
//            scan_faults = $fread(bats_data, fptr);
//            data2_in = bats_data;
//            data_valid_in = 1'b1;
//            #period;           
//        end
//        $fclose(fptr); // Close file before finish

        $finish;
    end
endmodule
