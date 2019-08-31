FROM jupyter/scipy-notebook:66c99628f4b8 

LABEL maintainer="Luca De Feo <https://defeo.lu/>"

USER root

# APT packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu \
    tzdata \
    gfortran \
    gcc \
    scilab \
    pari-gp \
    libpari-dev \
    sagemath \
    sagemath-jupyter \
    libgmp-dev \
    git \
    openssh-client \
    ssh \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER $NB_UID

# Conda packages
# Sage conflicts with the latest jupyterhub, thus we must relax the pinning
RUN conda install --quiet --yes \
    'r-base=3.4.1' \
    'r-irkernel=0.8*' \
    'r-plyr=1.8*' \
    'r-devtools=1.13*' \
    'r-tidyverse=1.1*' \
    'r-shiny=1.0*' \
    'r-rmarkdown=1.8*' \
    'r-forecast=8.2*' \
    'r-rsqlite=2.0*' \
    'r-reshape2=1.4*' \
    'r-nycflights13=0.2*' \
    'r-caret=6.0*' \
    'r-rcurl=1.95*' \
    'r-crayon=1.3*' \
    'r-randomforest=4.6*' \
    'r-htmltools=0.3*' \
    'r-sparklyr=0.7*' \
    'r-htmlwidgets=1.0*' \
    'r-hexbin=1.27*' \
    'jupyterhub' \
#    'sage=8.*' \
    'julia=1.0*' && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR

ENV CPATH=$CONDA_DIR/include

RUN pip install \
    pari_jupyter \
#    PySingular jupyter_kernel_singular \
    scilab-kernel && \
    fix-permissions $CONDA_DIR

USER $NB_UID

COPY ./keys/id_rsa.pub ./keys/id_rsa /home/$NB_USER/.ssh/

USER root

RUN echo "Host gitlab.mmcs.sfedu.ru\n\t\tStrictHostKeyChecking no\n" >> /home/$NB_USER/.ssh/config

USER $NB_UID

RUN cd /home/$NB_USER/work && git clone git@gitlab.mmcs.sfedu.ru:OPS_Group/OPS.git

# Fix SageMath kernel
USER root
RUN sed -i 's/"\/usr\/bin\/sage"/"env", "PATH=\/usr\/local\/sbin:\/usr\/local\/bin:\/usr\/sbin:\/usr\/bin:\/sbin:\/bin", "\/usr\/bin\/sage"/' /usr/share/jupyter/kernels/sagemath/kernel.json
USER $NB_UID

# Add conda env hook
COPY ./conda-activate.sh /usr/local/bin/before-notebook.d/

USER root

RUN jupyter labextension install @jupyterlab/git
RUN pip install --upgrade jupyterlab-git
RUN jupyter serverextension enable --py jupyterlab_git

USER $NB_UID

RUN /opt/conda/bin/conda create -n cling
RUN echo "source activate cling" > ~/.bashrc && \
    bash -c "source ~/.bashrc"
    #  conda init bash && \
    #  conda activate cling
    
RUN /opt/conda/bin/conda install xeus-cling -c conda-forge

RUN mkdir /opt/notebooks

#RUN mkdir /opt/conda/share/jupyter/kernels/cpp11 && \
#    cp /opt/conda/envs/cling/share/jupyter/kernels/xcpp11/* /opt/conda/share/jupyter/kernels/cpp11


user root

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    p7zip-full \
    qt5-default libqt5svg5-dev && \
    apt-get clean && \
    apt-get -y autoremove

RUN apt-get install -y cmake

RUN apt-get install -y libgtest-dev && \
    cd /usr/src/gtest/ && \
    cmake -DBUILD_SHARED_LIBS=ON && \
    make && \
    cp *.so /usr/lib

ADD . /home/jovyan/build

#RUN mkdir ~/Src && \
#    cd ~/Src && \
#    wget http://llvm.org/releases/5.0.0/llvm-5.0.0.src.tar.xz && \
#    wget http://llvm.org/releases/5.0.0/cfe-5.0.0.src.tar.xz  && \
#    tar -xvf llvm-5.0.0.src.tar.xz && \
#    tar -xvf cfe-5.0.0.src.tar.xz && \
#    mv -T cfe-5.0.0.src llvm-5.0.0.src/tools/clang && \
#    mkdir llvm-5.0.0.build && \
#    cd llvm-5.0.0.build && \
#    export CXXFLAGS="${CXXFLAGS} -fvisibility=hidden" && \
#    cmake -LAH -D CMAKE_BUILD_TYPE=Debug -D LLVM_REQUIRES_RTTI=1 -D LLVM_TARGETS_TO_BUILD="X86;" -D BUILD_SHARED_LIBS=0 -D LLVM_INCLUDE_TOOLS=0 -D LLVM_INCLUDE_EXAMPLES=0 -D LLVM_INCLUDE_TESTS=0 -D LLVM_INCLUDE_UTILS=0 -D LLVM_INCLUDE_DOCS=0 -D LLVM_ENABLE_TERMINFO=0 -D CMAKE_INSTALL_PREFIX=~/Lib/llvm-5.0.0.install ../llvm-5.0.0.src && \
#    make -j2  && \
#    make install

# /home/jovyan/work/OPS

user $NB_UID
	
RUN cd /home/$NB_USER/work/OPS && git fetch && git checkout issue26_clang5 && git pull

RUN mkdir /home/$NB_USER/work/ops-build

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


