#!/bin/bash
./configure --enable-ssl  --with-precision-digits=8 --with-thread=stdthread --with-precision=double --with-maxmsglen=32768 
#vi utests/Makefile: message_test$(EXEEXT): $(message_test_DEPENDENCIES) $(message_test_OBJECTS)
make -j4 install
