#!/usr/bin/env bash
c++ -O0 -Wall -shared -std=c++17 -fPIC \
    -lmorfeusz2 \
    $(python3 -m pybind11 --includes) \
    -I ./src/pymorfeusz2/include \
    src/pymorfeusz2/pymorfeusz2.cpp \
    -o "_pymorfeusz2$(python3-config --extension-suffix)"
