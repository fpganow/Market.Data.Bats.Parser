-- VHDL wrapper for NiFpgaAG_bats_parser_ip
-- Generated by LabVIEW FPGA IP Export Utility
--
-- Ports:
-- reset      :  Reset port. Minimum assertion length: 8 base clock cycles.
--               Minimum de-assertion length: 40 base clock cycles.
-- enable_in  :  Enable in port. Minimum re-initialization length: 7 base clock cycles.
-- enable_out :  Enable out port.
-- enable_clr :  Enable clear port.
-- ctrlind_00_Ready_For_Debug : Top level control "Ready.For.Debug", sync to Clk40, bool
-- ctrlind_01_Debug_Valid : Top level indicator "Debug.Valid", sync to Clk40, bool
-- ctrlind_02_Debug_Element : Top level indicator "Debug.Element", sync to Clk40, u64
-- ctrlind_03_Ready_for_OrderBook_Command : Top level control "Ready.for.OrderBook.Command", sync to Clk40, bool
-- ctrlind_04_OrderBook_Command_Valid : Top level indicator "OrderBook.Command.Valid", sync to Clk40, bool
-- ctrlind_05_Nanoseconds_U64 : Top level indicator "Nanoseconds (U64)", sync to Clk40, u64
-- ctrlind_06_Seconds_U64 : Top level indicator "Seconds (U64)", sync to Clk40, u64
-- ctrlind_07_Remaining_Quantity_U32 : Top level indicator "Remaining Quantity (U32)", sync to Clk40, u32
-- ctrlind_08_Canceled_Quantity_U32 : Top level indicator "Canceled Quantity (U32)", sync to Clk40, u32
-- ctrlind_09_Executed_Quantity_U32 : Top level indicator "Executed Quantity (U32)", sync to Clk40, u32
-- ctrlind_10_Price_U64 : Top level indicator "Price (U64)", sync to Clk40, u64
-- ctrlind_11_Symbol_U64 : Top level indicator "Symbol (U64)", sync to Clk40, u64
-- ctrlind_12_Quantity_U32 : Top level indicator "Quantity (U32)", sync to Clk40, u32
-- ctrlind_13_Order_Id_U64 : Top level indicator "Order Id (U64)", sync to Clk40, u64
-- ctrlind_14_Side_U8 : Top level indicator "Side (U8)", sync to Clk40, u8
-- ctrlind_15_OrderBook_Command_Type : Top level indicator "OrderBook Command.Type", sync to Clk40, enum8
-- ctrlind_16_data_valid : Top level control "data.valid", sync to Clk40, bool
-- ctrlind_17_Byte_Enables : Top level control "Byte.Enables", sync to Clk40, array
-- ctrlind_18_Bytes : Top level control "Bytes", sync to Clk40, array
-- ctrlind_19_reset : Top level control "reset", sync to Clk40, bool
-- ctrlind_20_Ready_for_Udp_Input : Top level indicator "Ready.for.Udp.Input", sync to Clk40, bool
-- Clk40 : Clock "40 MHz Onboard Clock", nominal frequency 40.00 MHz, base clock

library ieee;
use ieee.std_logic_1164.all;

entity NiFpgaIPWrapper_bats_parser_ip is
		port (
			reset : in std_logic;
			enable_in : in std_logic;
			enable_out : out std_logic;
			enable_clr : in std_logic;
			ctrlind_00_Ready_For_Debug : in std_logic_vector(0 downto 0);
			ctrlind_01_Debug_Valid : out std_logic_vector(0 downto 0);
			ctrlind_02_Debug_Element : out std_logic_vector(63 downto 0);
			ctrlind_03_Ready_for_OrderBook_Command : in std_logic_vector(0 downto 0);
			ctrlind_04_OrderBook_Command_Valid : out std_logic_vector(0 downto 0);
			ctrlind_05_Nanoseconds_U64 : out std_logic_vector(63 downto 0);
			ctrlind_06_Seconds_U64 : out std_logic_vector(63 downto 0);
			ctrlind_07_Remaining_Quantity_U32 : out std_logic_vector(31 downto 0);
			ctrlind_08_Canceled_Quantity_U32 : out std_logic_vector(31 downto 0);
			ctrlind_09_Executed_Quantity_U32 : out std_logic_vector(31 downto 0);
			ctrlind_10_Price_U64 : out std_logic_vector(63 downto 0);
			ctrlind_11_Symbol_U64 : out std_logic_vector(63 downto 0);
			ctrlind_12_Quantity_U32 : out std_logic_vector(31 downto 0);
			ctrlind_13_Order_Id_U64 : out std_logic_vector(63 downto 0);
			ctrlind_14_Side_U8 : out std_logic_vector(7 downto 0);
			ctrlind_15_OrderBook_Command_Type : out std_logic_vector(7 downto 0);
			ctrlind_16_data_valid : in std_logic_vector(0 downto 0);
			ctrlind_17_Byte_Enables : in std_logic_vector(7 downto 0);
			ctrlind_18_Bytes : in std_logic_vector(63 downto 0);
			ctrlind_19_reset : in std_logic_vector(0 downto 0);
			ctrlind_20_Ready_for_Udp_Input : out std_logic_vector(0 downto 0);
			Clk40 : in std_logic
		);
end NiFpgaIPWrapper_bats_parser_ip;

architecture vhdl_labview of NiFpgaIPWrapper_bats_parser_ip is

	component NiFpgaAG_bats_parser_ip
		port (
			reset : in std_logic;
			enable_in : in std_logic;
			enable_out : out std_logic;
			enable_clr : in std_logic;
			ctrlind_00_Ready_For_Debug : in std_logic_vector(0 downto 0);
			ctrlind_01_Debug_Valid : out std_logic_vector(0 downto 0);
			ctrlind_02_Debug_Element : out std_logic_vector(63 downto 0);
			ctrlind_03_Ready_for_OrderBook_Command : in std_logic_vector(0 downto 0);
			ctrlind_04_OrderBook_Command_Valid : out std_logic_vector(0 downto 0);
			ctrlind_05_Nanoseconds_U64 : out std_logic_vector(63 downto 0);
			ctrlind_06_Seconds_U64 : out std_logic_vector(63 downto 0);
			ctrlind_07_Remaining_Quantity_U32 : out std_logic_vector(31 downto 0);
			ctrlind_08_Canceled_Quantity_U32 : out std_logic_vector(31 downto 0);
			ctrlind_09_Executed_Quantity_U32 : out std_logic_vector(31 downto 0);
			ctrlind_10_Price_U64 : out std_logic_vector(63 downto 0);
			ctrlind_11_Symbol_U64 : out std_logic_vector(63 downto 0);
			ctrlind_12_Quantity_U32 : out std_logic_vector(31 downto 0);
			ctrlind_13_Order_Id_U64 : out std_logic_vector(63 downto 0);
			ctrlind_14_Side_U8 : out std_logic_vector(7 downto 0);
			ctrlind_15_OrderBook_Command_Type : out std_logic_vector(7 downto 0);
			ctrlind_16_data_valid : in std_logic_vector(0 downto 0);
			ctrlind_17_Byte_Enables : in std_logic_vector(7 downto 0);
			ctrlind_18_Bytes : in std_logic_vector(63 downto 0);
			ctrlind_19_reset : in std_logic_vector(0 downto 0);
			ctrlind_20_Ready_for_Udp_Input : out std_logic_vector(0 downto 0);
			Clk40 : in std_logic;
			tDiagramEnableOut : in std_logic
		);
	end component;

begin
	MyLabVIEWIP : NiFpgaAG_bats_parser_ip
		port map(
			reset => reset,
			enable_in => enable_in,
			enable_out => enable_out,
			enable_clr => enable_clr,
			ctrlind_00_Ready_For_Debug => ctrlind_00_Ready_For_Debug,
			ctrlind_01_Debug_Valid => ctrlind_01_Debug_Valid,
			ctrlind_02_Debug_Element => ctrlind_02_Debug_Element,
			ctrlind_03_Ready_for_OrderBook_Command => ctrlind_03_Ready_for_OrderBook_Command,
			ctrlind_04_OrderBook_Command_Valid => ctrlind_04_OrderBook_Command_Valid,
			ctrlind_05_Nanoseconds_U64 => ctrlind_05_Nanoseconds_U64,
			ctrlind_06_Seconds_U64 => ctrlind_06_Seconds_U64,
			ctrlind_07_Remaining_Quantity_U32 => ctrlind_07_Remaining_Quantity_U32,
			ctrlind_08_Canceled_Quantity_U32 => ctrlind_08_Canceled_Quantity_U32,
			ctrlind_09_Executed_Quantity_U32 => ctrlind_09_Executed_Quantity_U32,
			ctrlind_10_Price_U64 => ctrlind_10_Price_U64,
			ctrlind_11_Symbol_U64 => ctrlind_11_Symbol_U64,
			ctrlind_12_Quantity_U32 => ctrlind_12_Quantity_U32,
			ctrlind_13_Order_Id_U64 => ctrlind_13_Order_Id_U64,
			ctrlind_14_Side_U8 => ctrlind_14_Side_U8,
			ctrlind_15_OrderBook_Command_Type => ctrlind_15_OrderBook_Command_Type,
			ctrlind_16_data_valid => ctrlind_16_data_valid,
			ctrlind_17_Byte_Enables => ctrlind_17_Byte_Enables,
			ctrlind_18_Bytes => ctrlind_18_Bytes,
			ctrlind_19_reset => ctrlind_19_reset,
			ctrlind_20_Ready_for_Udp_Input => ctrlind_20_Ready_for_Udp_Input,
			Clk40 => Clk40,
			tDiagramEnableOut => '1'
		);

end vhdl_labview;
