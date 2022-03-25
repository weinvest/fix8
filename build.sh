#!/bin/bash
./configure --enable-ssl --with-thread=stdthread  --with-precision-digits=8 --with-maxmsglen=32768 --disable-f8test --disable-gtest
#vi utests/Makefile: message_test$(EXEEXT): $(message_test_DEPENDENCIES) $(message_test_OBJECTS)
make -j4 install
