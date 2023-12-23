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
    IS_WSL  := $(shell uname -a | grep -Pzo WSL)
    ifeq ($(IS_WSL),WSL)
        ARCH=wsl
    	VIVADO_DRIVE         :=  "F"
    	VIVADO_HOME          := "${VIVADO_DRIVE}:\\Xilinx\\Vivado\\${VIVADO_VER}"
    	VIVADO_BIN           := "${VIVADO_HOME}\\bin"
    	VIVADO_SETTINGS_64   := "${VIVADO_HOME}\\settings64.bat"

    	VIVADO_WIN  := C:\Xilinx\Vivado\2023.1\bin
 
    	XSC_BAT := "${VIVADO_HOME}\\bin\\xsc.bat"
    	XVHDL_BAT := "${VIVADO_HOME}\\bin\\xvhdl.bat"
    	XVLOG_BAT := "${VIVADO_HOME}\\bin\\xvlog.bat"
    	XELAB_BAT := "${VIVADO_HOME}\\bin\\xelab.bat"
    	XSIM_BAT := "${VIVADO_HOME}\\bin\\xsim.bat"

    else
        ifeq ($(UNAME_S),Linux)
            ARCH=linux
    		VIVADO_LIN_HOME      := "/tools/Xilinx/Vivado/${VIVADO_VER}/"
    		VIVADO_LIN_BIN       := "${VIVADO_LIN_HOME}/bin"
    		VIVADO_LIN_XSC       := "${VIVADO_LIN_BIN}/xsc"
    		VIVADO_LIN_XVHDL     := "${VIVADO_LIN_BIN}/xvhdl"
    		VIVADO_LIN_XVLOG     := "${VIVADO_LIN_BIN}/xvlog"
    		VIVADO_LIN_XELAB     := "${VIVADO_LIN_BIN}/xelab"
    		VIVADO_LIN_XSIM      := "${VIVADO_LIN_BIN}/xsim"
        endif
    endif
endif



help: info
	@echo
	@echo "Help"
	@echo "  - help_xsc"
	@echo "  - help_xsc"

info_win:
	@echo "Windows"

info_linux:
	@echo "Linux"

info: info_${ARCH}
	@echo "Detected architecture: ARCH=$(ARCH)"

xsc_help_win:
	powershell.exe ${XSC_BAT} --help
xsc_help_linux:
	${VIVADO_LIN_XSC} --help
xsc_help: xsc_help_${ARCH}

xvhdl_help_win:
	powershell.exe ${XVHDL_BAT} --help
xvhdl_help_linux:
	${VIVADO_LIN_XVHDL} --help
xvhdl_help: xvhdl_help_${ARCH}

xvlog_help_win:
	powershell.exe ${XVLOG_BAT} --help
xvlog_help_linux:
	${VIVADO_LIN_XVLOG} --help
xvlog_help: xvlog_help_${ARCH}

xelab_help_win:
	powershell.exe ${XELAB_BAT} --help
xelab_help_linux:
	${VIVADO_LIN_XELAB}  --help
xelab_help: xelab_help_${ARCH}

xsim_help_win:
	powershell.exe ${XELAB_BAT} --help
xsim_help_linux:
	${VIVADO_LIN_XELAB}  --help
xsim_help: xsim_help_${ARCH}


build:
	@echo -n ""
	@echo "Synthesizing Project"
	@echo "Running xvhdl.bat"
	@echo ""
	powershell.exe ${XVHDL_BAT}

clean:
	@echo "Cleaning"
	rm -rf xsim.dir
	rm -f xelab.*
	rm -f xsc.*
	rm -f xsim_*.*
	rm -f xsim.*
	rm -f xvhdl.*
	rm -f xvlog.*
	cd ip_export && rm -rf build
	cd ip_export && rm -f pysv_pkg.sv
	cd ip_export && rm -f *.pb
	cd ip_export && rm -f *.log
	cd ip_export && rm -f *.jou
	cd ip_export && rm -rf xsim.dir


#SRC_PATH 	  := $(shell echo "$(PWD)" | sed 's|^/mnt/||;s|/|\\|g')
.PHONY: dpi

#dpi: SRC_PATH 	  := $(shell echo "$(PWD)" | sed 's|^/mnt/||;s|/|\\|g')
#dpi: WIN_PATH 	  := $(shell echo "$(PWD)" | sed 's|^/mnt/||;s|/|\\|g')
ps_dpi:
	echo -n ""
	@echo "Synthesizing Project"
	@echo "Running xvhdl.bat"
	@echo "------"
	powershell.exe ${XSC_BAT} ./ip_export/dpi/simple_import/function.c -v
	powershell.exe ${XVLOG_BAT} -svlog ./ip_export/dpi/simple_import/file.sv
	powershell.exe ${XELAB_BAT} work.m -sv_lib dpi -R

win_dpi:
	${VIVADO_WIN}\xsc.bat .\ip_export\dpi\simple_import\function.c -v
	${VIVADO_WIN}\xvlog.bat -svlog .\ip_export\dpi\simple_import\file.sv
	${VIVADO_WIN}\xelab.bat work.m -sv_lib dpi -R

# Vivado 2023.2 has python3.8 embedded, so I'll use the same version.
export PYTHON=python3.8
lin_dpi:
	@echo "Building pysv python bindings"
	cd ip_export/tests && ${PYTHON} ./bats_loader.py
	cd ip_export/tests && ${VIVADO_LIN_XSC} ./dpi_to_py.c -v
	cd ip_export/tests && ${VIVADO_LIN_XVLOG} -sv -svlog ./parser_tb.sv
	cd ip_export/tests && ${VIVADO_LIN_XELAB} work.m -sv_lib dpi -sv_lib ./build/libpysv -R

install_deps:
	@echo "Installing pysv using PYTHON=${PYTHON}"
	powershell.exe ${PYTHON} -m pip install numpy

test_win: PYTHON=C:\\\\Users\\\\johns\\\\AppData\\\\Local\\\\Programs\\\\Python\\\\Python38\\\\python.exe
test_win:
	@echo "Building pysv-based test bench (Windows)"
	cd ip_export && ${PYTHON} ./bats_loader.py

test_wsl: PYTHON=C:\\Users\\johns\\AppData\\Local\\Programs\\Python\\Python38\\python.exe
test_wsl: install_deps
	@echo "Building pysv-based test bench (WSL)"
	@echo "PYTHON=${PYTHON}"
	cd ip_export && powershell.exe ${PYTHON} ./bats_loader.py
	#####powershell.exe ${XSC_BAT} ./ip_export/dpi/simple_import/function.c -v
	#####powershell.exe ${XVLOG_BAT} -svlog ./ip_export/dpi/simple_import/file.sv
	#####powershell.exe ${XELAB_BAT} work.m -sv_lib dpi -R
	#####cd ip_export/tests && powershell.exe ${XSC_BAT} ./dpi_to_py.c -v
	#####cd ip_export && powershell.exe ${XVLOG_BAT} -sv -svlog ./parser_tb.sv
	#cd ip_export && powershell.exe ${XVHDL_BAT} ./NiFpgaIPWrapper_bats_parser_ip.vhd
	#cd ip_export && powershell.exe ${XVLOG_BAT} -sv -svlog ./bats_parser_tb.sv
	#cd ip_export && powershell.exe ${XELAB_BAT} work.m -sv_lib ./build/libpysv -R

test_linux:
	@echo "Building pysv-based test bench (Linux)"
	@echo " - Creating Python bindings"
	@cd ip_export && ${PYTHON} ./bats_loader.py
	@echo
	@echo " - Compiling IP Wrapper"
	@cd ip_export && ${VIVADO_LIN_XVHDL} ./NiFpgaIPWrapper_bats_parser_ip.vhd
	@echo
	@echo " - Compiling SystemVerilog TestBench"
	cd ip_export && ${VIVADO_LIN_XVLOG} -sv -svlog ./bats_parser_tb.sv
	@echo
	@echo " - Elaborating"
	cd ip_export && ${VIVADO_LIN_XELAB} -debug all -top bats_parser_tb -sv_lib ./build/libpysv --snapshot bats_parser_tb
	@echo
	@echo " - Running Simulation"
	cd ip_export && ${VIVADO_LIN_XSIM} bats_parser_tb  -autoloadwcfg -runall

gui:
	@echo
	@echo " - Displaying waveform"
	@echo " xsim --gui ./ip_export/bats_parser_tb.wdb"

old_test_linux:
	#cd ip_export && ${PYTHON} ./bats_loader.py
	#cd ip_export && ${VIVADO_LIN_XVLOG} -sv -svlog ./bats_parser_tb.sv
	#cd ip_export && ${VIVADO_LIN_XELAB} work.m -sv_lib ./build/libpysv -R

test: test_${ARCH}
