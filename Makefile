
VIVADO_VER           := 2023.2

VIVADO_LIN_HOME      := "/tools/Xilinx/Vivado/${VIVADO_VER}/"
VIVADO_LIN_BIN       := "${VIVADO_LIN_HOME}/bin"
VIVADO_LIN_XSC       := "${VIVADO_LIN_BIN}/xsc"
VIVADO_LIN_XVHDL     := "${VIVADO_LIN_BIN}/xvhdl"
VIVADO_LIN_XVLOG     := "${VIVADO_LIN_BIN}/xvlog"
VIVADO_LIN_XELAB     := "${VIVADO_LIN_BIN}/xelab"
VIVADO_LIN_XSIM      := "${VIVADO_LIN_BIN}/xsim"

VIVADO_DRIVE         :=  "F"
VIVADO_HOME          := "${VIVADO_DRIVE}:\\Xilinx\\Vivado\\${VIVADO_VER}"
VIVADO_BIN           := "${VIVADO_HOME}\\bin"
VIVADO_SETTINGS_64   := "${VIVADO_HOME}\\settings64.bat"

VIVADO_WIN  := F:\Xilinx\Vivado\2023.1\bin

XSC_BAT := "${VIVADO_HOME}\\bin\\xsc.bat"
XVHDL_BAT := "${VIVADO_HOME}\\bin\\xvhdl.bat"
XVLOG_BAT := "${VIVADO_HOME}\\bin\\xvlog.bat"
XELAB_BAT := "${VIVADO_HOME}\\bin\\xelab.bat"
XSIM_BAT := "${VIVADO_HOME}\\bin\\xsim.bat"


# 1 - Synthesize
#  * NiFpgaIPWrapper_bats_parser_ip.vhd
#  * NiFpgaAG_bats_parser_ip.dcp
# 2 - Run Post-Simulation Synthesis
#@echo 'SRC_PATH=${SRC_PATH}'
#@echo 'XSC_BAT=${XSC_BAT}'
#@echo 'WIN_PATH=${WIN_PATH}'
#@echo '$$WIN_PATH: ${WIN_PATH}'
#@echo '$$XVHDL_BAT: ${XVHDL_BAT}'

xsc_help:
	powershell.exe ${XSC_BAT}

xvlog_help:
	powershell.exe ${XVLOG_BAT}

xelab_help:
	powershell.exe ${XELAB_BAT} 

build:
	@echo -n ""
	@echo "Synthesizing Project"
	@echo "Running xvhdl.bat"
	@echo ""
	powershell.exe ${XVHDL_BAT}

clean:
	rm -rf xsim.dir
	rm -f xelab.*
	rm -f xsc.*
	rm -f xsim_*.*
	rm -f xsim.*
	rm -f xvhdl.*
	rm -f xvlog.*

help_xsc:
	powershell.exe ${XSC_BAT}

help_xvlog:
	powershell.exe ${XVLOG_BAT}

help_xelab:
	powershell.exe ${XELAB_BAT}

help_xsim:
	powershell.exe ${XSIM_BAT} --help

SRC_PATH 	  := $(shell echo "$(PWD)" | sed 's|^/mnt/||;s|/|\\|g')
.PHONY: dpi

#dpi: SRC_PATH 	  := $(shell echo "$(PWD)" | sed 's|^/mnt/||;s|/|\\|g')
#dpi: WIN_PATH 	  := $(shell echo "$(PWD)" | sed 's|^/mnt/||;s|/|\\|g')
ps_dpi:
	echo -n ""
	@echo "Synthesizing Project"
	@echo "Running xvhdl.bat"
	@echo "------"
	powershell.exe ${XSC_BAT} ./ip_export/dpi/simple_import/function.c -v
	#powershell.exe ${XVLOG_BAT} -svlog ./ip_export/dpi/simple_import/file.sv
	#powershell.exe ${XELAB_BAT} work.m -sv_lib dpi -R


win_dpi:
	${VIVADO_WIN}\xsc.bat .\ip_export\dpi\simple_import\function.c -v
	${VIVADO_WIN}\xvlog.bat -svlog .\ip_export\dpi\simple_import\file.sv
	${VIVADO_WIN}\xelab.bat work.m -sv_lib dpi -R


lin_dpi:
	${VIVADO_LIN_XSC} ./ip_export/dpi/simple_import/function.c -v
	${VIVADO_LIN_XVLOG} -svlog ./ip_export/dpi/simple_import/file.sv
	${VIVADO_LIN_XELAB} work.m -sv_lib dpi -R
