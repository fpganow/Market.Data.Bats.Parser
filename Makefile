
VIVADO_VER           := 2023.1
VIVADO_HOME          := "C:\\Xilinx\\Vivado\\${VIVADO_VER}"
VIVADO_BIN           := "${VIVADO_HOME}\\bin"
VIVADO_SETTINGS_64   := "${VIVADO_HOME}\\settings64.bat"

XVHDL_BAT := "${VIVADO_HOME}\\bin\\xvhdl.bat"
XVLOG_BAT := "${VIVADO_HOME}\\bin\\xvlog.bat"
XELAB_BAT := "${VIVADO_HOME}\\bin\\xelab.bat"

WIN_PATH 	  := $(shell echo "$(PWD)" | sed 's|^/mnt/||;s|/|\\|g')
#@echo '$$WIN_PATH: ${WIN_PATH}'
#@echo '$$XVHDL_BAT: ${XVHDL_BAT}'

# 1 - Synthesize
#  * NiFpgaIPWrapper_bats_parser_ip.vhd
#  * NiFpgaAG_bats_parser_ip.dcp
# 2 - Run Post-Simulation Synthesis

build:
	@echo -n ""
	@echo "Synthesizing Project"
	@echo "Running xvhdl.bat"
	@echo ""
	powershell.exe ${XVHDL_BAT}
