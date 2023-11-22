
VIVADO_VER           := 2023.1
VIVADO_HOME          := "C:\\Xilinx\\Vivado\\${VIVADO_VER}"
VIVADO_BIN           := "${VIVADO_HOME}\\bin"
VIVADO_SETTINGS_64   := "${VIVADO_HOME}\\settings64.bat"

XSC_BAT := "${VIVADO_HOME}\\bin\\xsc.bat"
XVHDL_BAT := "${VIVADO_HOME}\\bin\\xvhdl.bat"
XVLOG_BAT := "${VIVADO_HOME}\\bin\\xvlog.bat"
XELAB_BAT := "${VIVADO_HOME}\\bin\\xelab.bat"

WIN_PATH 	  := $(shell echo "$(PWD)" | sed 's|^/mnt/||;s|/|\\|g')

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

SRC_PATH 	  := $(shell echo "$(PWD)" | sed 's|^/mnt/||;s|/|\\|g')
dpi:
	@echo -n ""
	@echo "Synthesizing Project"
	@echo "Running xvhdl.bat"
	@echo ""

	@echo 'SRC_PATH=${SRC_PATH}'
	@echo 'XSC_BAT=${XSC_BAT}'
	@echo 'WIN_PATH=${WIN_PATH}'
	@echo '$$WIN_PATH: ${WIN_PATH}'
	@echo '$$XVHDL_BAT: ${XVHDL_BAT}'

	powershell.exe ${XSC_BAT} ./ip_export/dpi/simple_import/function.c
	powershell.exe ${XVLOG_BAT} -svlog ./ip_export/dpi/simple_import/file.sv
	powershell.exe ${XELAB_BAT} work.m -sv_lib dpi -R

