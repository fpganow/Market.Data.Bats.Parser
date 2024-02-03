SHELL := /bin/bash

VIVADO_VER           := 2023.2

ifeq ($(OS),Windows_NT)
    ARCH=win
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
else
    UNAME_S := $(shell uname -s)
    ARCH=linux
    VIVADO_LIN_HOME      := "/tools/Xilinx/Vivado/${VIVADO_VER}/"
    VIVADO_LIN_BIN       := "${VIVADO_LIN_HOME}/bin"
    VIVADO_LIN_XSC       := "${VIVADO_LIN_BIN}/xsc"
    VIVADO_LIN_XVHDL     := "${VIVADO_LIN_BIN}/xvhdl"
    VIVADO_LIN_XVLOG     := "${VIVADO_LIN_BIN}/xvlog"
    VIVADO_LIN_XELAB     := "${VIVADO_LIN_BIN}/xelab"
    VIVADO_LIN_XSIM      := "${VIVADO_LIN_BIN}/xsim"
endif


help: info
	@echo
	@echo "Help"
	@echo "  - clean"
	@echo "  - info"
	@echo "  - compile"
	@echo "  - elaborate"
	@echo "  - simulate"
	@echo "  - waveform"


clean:
	@echo "Cleaning"
	rm -f *.log *.jou
	rm -f xelab.*
	rm -f xsc.*
	rm -f xvhdl.*
	rm -f xvlog.*
	cd ip_export && rm -rf build
	cd ip_export && rm -f pysv_pkg.sv
	cd ip_export && rm -f *.pb
	cd ip_export && rm -f *.log
	cd ip_export && rm -f *.jou
	cd ip_export && rm -f *.wdb
	cd ip_export && rm -rf xsim.dir
	cd ip_export && rm -rf __pycache__
	cd ip_export/sim && rm -f *.log *.pb *.jou
	cd ip_export/sim && rm -rf xsim.dir

#XILINX_HLS=/tools/Xilinx/Vitis_HLS/2023.2
#XILINX_VIVADO=/tools/Xilinx/Vivado/2023.2
SRC_XIL=source /tools/Xilinx/Vivado/2023.2/settings64.sh
info:
	@echo "Detected architecture: ${ARCH}"
	@echo " - SHEL = ${SHELL}"
	${SRC_XIL} && printenv

# Generate synthesized version manually
# Then script it out
export PYTHON=python3.11
py_codegen:
	@echo "  - Creating Python Bindings"
	@echo "    Using Python=${PYTHON}"
	cd ip_export && ${PYTHON} ./bats_loader.py

compile: py_codegen
	@echo "  - Compiling"
	${SRC_XIL} && cd ip_export/sim && ./compile.sh

elaborate: compile
	@echo "  - Elaborating"
	${SRC_XIL} && cd ip_export/sim && ./elaborate.sh

simulate: elaborate
	@echo "  - Simulating"
	${SRC_XIL} && cd ip_export/sim && ./simulate.sh

waveform:
	@echo
	@echo " - Displaying waveform"
	@echo " xsim --gui ./ip_export/bats_parser_tb_func_synth.wdb"
	${SRC_XIL} && cd ip_export/sim && \
		xsim --gui ./bats_parser_tb_func_synth.wdb \
		--view ./bats_parser_tb_func_synth.wcfg

wave: waveform

# breaks with pysv==0.3.0
install_py_deps_linux:
	${PYTHON} -m pip install pysv==0.2.0

install_deps: install_deps_${ARCH}
	@echo "Installed pysv using PYTHON=${PYTHON}"

# Old manually created compile elaborate simulate commands created without .prj files
	#@echo
	#@echo " - Compiling IP Wrapper (Open Checkpoint and synthesize)"
	#cd ip_export && ${VIVADO_LIN_BIN}/xvhdl ./NiFpgaIPWrapper_bats_parser_ip.vhd
	#@echo " - Compiling Synthesized IP Wrapper"
	#cd ip_export && ${VIVADO_LIN_BIN}/xvlog --incr --relax ./bats_parser_tb_func_synth.v
	#@echo
	#@echo " - Compiling SystemVerilog TestBench"
	#cd ip_export && ${VIVADO_LIN_BIN}/xvlog -sv -svlog ./bats_parser_tb.sv
	#@echo
	#@echo " - Elaborating"
	#cd ip_export && ${VIVADO_LIN_BIN}/xelab --incr -debug all --relax --mt 8 \
#				-L xil_defaultlib -L unisims_ver -L secureip \
#				xil_defaultlib.glbl \
#				-top bats_parser_tb -sv_lib ./build/libpysv --snapshot bats_parser_tb
#					--snapshot bats_parser_tb_func_synth
	#@echo
	#@echo " - Running Simulation"
	#cd ip_export && ${VIVADO_LIN_XSIM} bats_parser_tb  -tclbatch xsim_cfg.tcl
#	cd ip_export && ${VIVADO_LIN_XSIM} --gui bats_parser_tb.wdb
#
#test_win: PYTHON=C:\\\\Users\\\\johns\\\\AppData\\\\Local\\\\Programs\\\\Python\\\\Python38\\\\python.exe
#test_win:
#	@echo "Building pysv-based test bench (Windows)"
#	cd ip_export && ${PYTHON} ./bats_loader.py
#
#test: test_${ARCH}
