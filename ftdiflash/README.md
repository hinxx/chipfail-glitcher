# ftdiflash
simple SPI flash programmer for use with FTDI USB devices

See the guide here: https://learn.adafruit.com/programming-spi-flash-prom-with-an-ft232h-breakout/overview

This is a modified version of the iceprog tool from the excellent Icestorm FPGA toolchain by Clifford Wolf
https://github.com/cliffordwolf/icestorm


## using latest libusb and libftdi

Get the sources and compile to allow static build of ftdiflash utility.

### libusb

wget https://github.com/libusb/libusb/releases/download/v1.0.26/libusb-1.0.26.tar.bz2
tar xf libusb-1.0.26.tar.bz2
cd libusb-1.0.26
./configure --disable-udev --prefix=/tmp/install
make
make install
cd ..

### libftdi

wget https://www.intra2net.com/en/developer/libftdi/download/libftdi1-1.5.tar.bz2
tar xf libftdi1-1.5.tar.bz2
cd libftdi1-1.5
mkdir build
cd build
cmake -DCMAKE_PREFIX_PATH=/tmp/install -DCMAKE_INSTALL_PREFIX=/tmp/install ..
make
make install

### ftdiflash

make

./ftdiflash

ftdiflash -- simple programming tool for programming SPI flash with an FTDI


Usage: ./ftdiflash [options] <filename>

    -d <device-string>
        use the specified USB device:

            d:<devicenode>                (e.g. d:002/005)
            i:<vendor>:<product>          (e.g. i:0x0403:0x6010)
            i:<vendor>:<product>:<index>  (e.g. i:0x0403:0x6010:0)
            s:<vendor>:<product>:<serial-string>

    -I [ABCD]
        connect to the specified interface on the FTDI chip

    -r
        read first 256 kB from flash and write to file

    -R <size_in_bytes>
        read the specified number of bytes from flash
        (append 'k' to the argument for size in kilobytes, or
        'M' for size in megabytes)

    -o <offset_in_bytes>
        start address for read/write (instead of zero)
        (append 'k' to the argument for size in kilobytes, or
        'M' for size in megabytes)

    -c
        do not write flash, only verify (check)

    -b
        bulk erase entire flash before writing

    -n
        do not erase flash before writing

    -t
        just read the flash ID sequence

    -v
        verbose output

Without -b or -n, ftdiflash will erase aligned chunks of 64kB in write mode.
This means that some data after the written data (or even before when -o is
used) may be erased as well.
