
all: glithcher.bin

# prog: icezero.bin icezprog
# 	./icezprog icezero.bin

# reset: icezprog
# 	./icezprog .

# icezprog: icezprog.c
# 	gcc -o icezprog -Wall -Os icezprog.c -lwiringPi -lrt -lstdc++

glithcher.blif: top.v pulse.v delay.v trigger.v uart_rx.v uart_tx.v uint32_receiver.v memdata.dat defines.vh
	yosys -p 'synth_ice40 -top top -blif glithcher.blif' top.v pulse.v delay.v trigger.v uart_rx.v uart_tx.v uint32_receiver.v

glithcher.json: top.v pulse.v delay.v trigger.v uart_rx.v uart_tx.v uint32_receiver.v memdata.dat defines.vh
	yosys -p 'synth_ice40 -top top -json glithcher.json' top.v pulse.v delay.v trigger.v uart_rx.v uart_tx.v uint32_receiver.v

glithcher.asc: glithcher.json glithcher.pcf
	nextpnr-ice40 --hx4k --package tq144 --pcf glithcher.pcf --asc glithcher.asc --json glithcher.json

glithcher.bin: glithcher.asc
	icetime -d hx4k -c 100 glithcher.asc
	icepack glithcher.asc glithcher.bin

memdata.dat: generate.py
	python3 generate.py

defines.vh: memdata.dat

testbench: testbench.v icezero.v
	iverilog -o testbench testbench.v icezero.v ../../icosoc/common/sim_sram.v $(shell yosys-config --datdir/ice40/cells_sim.v)

testbench.vcd: testbench
	./testbench

clean:
	rm -f testbench testbench.vcd
	rm -f glithcher.blif glithcher.json glithcher.asc glithcher.bin
	rm -f memdata.dat defines.vh

.PHONY: all prog reset clean

