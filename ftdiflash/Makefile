CXX ?= clang++
CC ?= clang
LDLIBS = -lm -lstdc++
CFLAGS = -MD -O0 -ggdb -Wall -std=c99 -I/tmp/install/include
CXXFLAGS = -MD -O0 -ggdb -Wall -std=c++11 -I/tmp/install/include
PKG_CONFIG ?= pkg-config
DESTDIR ?=
PREFIX ?= /tmp/install
CHIPDB_SUBDIR ?= icebox
STATIC = 1

ifeq ($(MXE),1)
EXE = .exe
CXX = /usr/local/src/mxe/usr/bin/i686-w64-mingw32.static-gcc
CC = $(CXX)
PKG_CONFIG = /usr/local/src/mxe/usr/bin/i686-w64-mingw32.static-pkg-config
endif

ifneq ($(shell uname -s),Darwin)
  LDLIBS = -L/tmp/install/lib -lm
else
  LIBFTDI_NAME = $(shell $(PKG_CONFIG) --exists libftdi1 && echo ftdi1 || echo ftdi)
  LDLIBS = -L/usr/local/lib -l$(LIBFTDI_NAME) -lm
endif

ifeq ($(STATIC),1)
LDFLAGS += -static
# LDLIBS += $(shell for pkg in libftdi1 libftdi; do $(PKG_CONFIG) --silence-errors --static --libs $$pkg && exit; done; echo -lftdi; )
# CFLAGS += $(shell for pkg in libftdi1 libftdi; do $(PKG_CONFIG) --silence-errors --static --cflags $$pkg && exit; done; )
LDLIBS += -L/tmp/install/lib -lftdi1 -lusb-1.0 -pthread
CFLAGS += -I/tmp/install/include
else
# LDLIBS += $(shell for pkg in libftdi1 libftdi; do $(PKG_CONFIG) --silence-errors --libs $$pkg && exit; done; echo -lftdi; )
# CFLAGS += $(shell for pkg in libftdi1 libftdi; do $(PKG_CONFIG) --silence-errors --cflags $$pkg && exit; done; )
LDLIBS += -L/tmp/install/lib -lftdi1 -lusb-1.0 -pthread
CFLAGS += -I/tmp/install/include
endif

all: ftdiflash$(EXE)

ftdiflash$(EXE): ftdiflash.o
	$(CC) -o $@ $(LDFLAGS) $^ $(LDLIBS)

install: all
	mkdir -p $(DESTDIR)$(PREFIX)/bin
	cp ftdiflash $(DESTDIR)$(PREFIX)/bin/ftdiflash

uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/ftdiflash

clean:
	rm -f ftdiflash$(EXE)
	rm -f *.o *.d

-include *.d

.PHONY: all install uninstall clean
