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
    // AUTO_GENERATED_CODE_START: parse.py ['./NiFpgaIPWrapper_bats_parser_ip.vhd']
    // Source file: ./NiFpgaIPWrapper_bats_parser_ip.vhd
    // Variables for NiFpgaIPWrapper_bats_parser_ip
    reg              reset;
    reg              enable_in;
    wire             enable_out;
    reg              enable_clr;
    reg    [ 0:0]    in_ip_ready_for_debug;
    wire   [ 0:0]    out_ip_debug_valid;
    wire   [63:0]    out_ip_debug_element;
    reg    [ 0:0]    in_ip_ready_for_orderbook_command;
    wire   [ 0:0]    out_ip_orderbook_command_valid;
    wire   [63:0]    out_ip_nanoseconds_u64;
    wire   [63:0]    out_ip_seconds_u64;
    wire   [31:0]    out_ip_remaining_quantity_u32;
    wire   [31:0]    out_ip_canceled_quantity_u32;
    wire   [31:0]    out_ip_executed_quantity_u32;
    wire   [63:0]    out_ip_price_u64;
    wire   [63:0]    out_ip_symbol_u64;
    wire   [31:0]    out_ip_quantity_u32;
    wire   [63:0]    out_ip_order_id_u64;
    wire   [ 7:0]    out_ip_side_u8;
    wire   [ 7:0]    out_ip_orderbook_command_type;
    reg    [ 0:0]    in_ip_reset;
    reg    [63:0]    in_ip_bytes;
    reg    [ 7:0]    in_ip_byte_enables;
    reg    [ 0:0]    in_ip_data_valid;
    wire   [ 0:0]    out_ip_ready_for_udp_input;
    wire   [63:0]    out_ip_bytes_echo;
    wire   [ 7:0]    out_ip_bytes_valid;
    reg              clk40;

    NiFpgaIPWrapper_bats_parser_ip UUT (
        .reset(reset),
        .enable_in(enable_in),
        .enable_out(enable_out),
        .enable_clr(enable_clr),
        .ctrlind_00_Ready_For_Debug(in_ip_ready_for_debug),
        .ctrlind_01_Debug_Valid(out_ip_debug_valid),
        .ctrlind_02_Debug_Element(out_ip_debug_element),
        .ctrlind_03_Ready_for_OrderBook_Command(in_ip_ready_for_orderbook_command),
        .ctrlind_04_OrderBook_Command_Valid(out_ip_orderbook_command_valid),
        .ctrlind_05_Nanoseconds_U64(out_ip_nanoseconds_u64),
        .ctrlind_06_Seconds_U64(out_ip_seconds_u64),
        .ctrlind_07_Remaining_Quantity_U32(out_ip_remaining_quantity_u32),
        .ctrlind_08_Canceled_Quantity_U32(out_ip_canceled_quantity_u32),
        .ctrlind_09_Executed_Quantity_U32(out_ip_executed_quantity_u32),
        .ctrlind_10_Price_U64(out_ip_price_u64),
        .ctrlind_11_Symbol_U64(out_ip_symbol_u64),
        .ctrlind_12_Quantity_U32(out_ip_quantity_u32),
        .ctrlind_13_Order_Id_U64(out_ip_order_id_u64),
        .ctrlind_14_Side_U8(out_ip_side_u8),
        .ctrlind_15_OrderBook_Command_Type(out_ip_orderbook_command_type),
        .ctrlind_16_reset(in_ip_reset),
        .ctrlind_17_Bytes(in_ip_bytes),
        .ctrlind_18_Byte_Enables(in_ip_byte_enables),
        .ctrlind_19_data_valid(in_ip_data_valid),
        .ctrlind_20_Ready_for_Udp_Input(out_ip_ready_for_udp_input),
        .ctrlind_21_Bytes_echo(out_ip_bytes_echo),
        .ctrlind_22_Bytes_Valid(out_ip_bytes_valid),
        .Clk40(clk40)
    );
    // AUTO_GENERATED_CODE_END: parse.py

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
        ip_data_valid_16_in = 0;
        ip_byte_enables_17_in = 8'h0;
        ip_bytes_18_in = 64'h00000000;

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
        //ip_bytes_18_in = 64'h00 00 00 02 01 01 00 0e;
        //ip_bytes_18_in = 64'h0e00010102000000;

        #(period*1);
        ip_data_valid_16_in = 1;
        ip_byte_enables_17_in = 8'b00111111;
        ip_bytes_18_in = 64'h00000006d2192006;
        //ip_bytes_18_in = 64'h00 00 00 06 d2 19 20 06;
        //ip_byte_enables_17_in = 8'b11111100;
        //ip_bytes_18_in = 64'h062019d206000000;

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
