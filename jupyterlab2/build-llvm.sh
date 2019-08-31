#!/bin/bash
mkdir ~/Src && \
    cd ~/Src && \
    wget http://llvm.org/releases/5.0.0/llvm-5.0.0.src.tar.xz && \
    wget http://llvm.org/releases/5.0.0/cfe-5.0.0.src.tar.xz  && \
    tar -xvf llvm-5.0.0.src.tar.xz && \
    tar -xvf cfe-5.0.0.src.tar.xz && \
    mv -T cfe-5.0.0.src llvm-5.0.0.src/tools/clang && \
    mkdir llvm-5.0.0.build && \
    cd llvm-5.0.0.build && \
    export CXXFLAGS="${CXXFLAGS} -fvisibility=hidden" && \
    cmake -LAH -D CMAKE_BUILD_TYPE=Debug -D LLVM_REQUIRES_RTTI=1 -D LLVM_TARGETS_TO_BUILD="X86;" -D BUILD_SHARED_LIBS=0 -D LLVM_INCLUDE_EXAMPLES=0 -D LLVM_INCLUDE_TESTS=0 -D LLVM_INCLUDE_UTILS=0 -D LLVM_INCLUDE_DOCS=0 -D LLVM_ENABLE_TERMINFO=0 -D CMAKE_INSTALL_PREFIX=~/Lib/llvm-5.0.0.install ../llvm-5.0.0.src && \
    make -j2  && \
    make install

#RUN cd /home/$NB_USER/work/ops-build && \
#    cmake \
#    -D CMAKE_BUILD_TYPE=Debug \
#    -D OPS_LLVM_DIR=/home/$NB_USER/Lib/llvm-5.0.0.install \
#    -D BUILD_SHARED_LIBS=1 ../OPS && \
#    make

#RUN cd /home/$NB_USER/work/OPS && git pull && \
#    cd /home/$NB_USER/work/ops-build && \
#    cmake \
#    -D  CMAKE_BUILD_TYPE=Debug \
#    -D OPS_LLVM_DIR=/home/$NB_USER/Lib/llvm-5.0.0.install \
#    -D BUILD_SHARED_LIBS=1 ../OPS && \
#    make


