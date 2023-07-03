
all: icezero.bin

prog: icezero.bin icezprog
	./icezprog icezero.bin

reset: icezprog
	./icezprog .

icezprog: icezprog.c
	gcc -o icezprog -Wall -Os icezprog.c -lwiringPi -lrt -lstdc++

icezero.blif: top.v pulse.v delay.v trigger.v uart_rx.v uart_tx.v uint32_receiver.v memdata.dat defines.vh
	yosys -p 'synth_ice40 -top top -blif icezero.blif' top.v pulse.v delay.v trigger.v uart_rx.v uart_tx.v uint32_receiver.v

icezero.json: top.v pulse.v delay.v trigger.v uart_rx.v uart_tx.v uint32_receiver.v memdata.dat defines.vh
	yosys -p 'synth_ice40 -top top -json icezero.json' top.v pulse.v delay.v trigger.v uart_rx.v uart_tx.v uint32_receiver.v

#icezero.asc: icezero.blif icezero.pcf
icezero.asc: icezero.json icezero.pcf
	nextpnr-ice40 --hx8k --package tq144:4k --pcf icezero.pcf --asc icezero.asc --json icezero.json

icezero.bin: icezero.asc
#	icetime -d hx8k -c 25 icezero.asc
	icetime -d hx8k -c 100 icezero.asc
	icepack icezero.asc icezero.bin

# SUCCESS!!
# ...
# // Timing estimate: 9.03 ns (110.76 MHz)
# // Checking 40.00 ns (25.00 MHz) clock constraint: PASSED.
# icepack icezero.asc icezero.bin

memdata.dat: generate.py
	python3 generate.py

defines.vh: memdata.dat

testbench: testbench.v icezero.v
	iverilog -o testbench testbench.v icezero.v ../../icosoc/common/sim_sram.v $(shell yosys-config --datdir/ice40/cells_sim.v)

testbench.vcd: testbench
	./testbench

clean:
	rm -f testbench testbench.vcd
	rm -f icezero.blif icezero.json icezero.asc icezero.bin
	rm -f memdata.dat defines.vh

.PHONY: all prog reset clean

