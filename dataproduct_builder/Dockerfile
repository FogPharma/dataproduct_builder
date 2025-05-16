FROM continuumio/miniconda3
RUN apt-get update 
RUN apt-get install -y build-essential curl libbz2-dev libffi-dev liblzma-dev   libncursesw5-dev  libreadline-dev  libsqlite3-dev libssl-dev  libxml2-dev libxmlsec1-dev  llvm  make  tk-dev   wget  xz-utils zlib1g-dev unixodbc  unixodbc-dev
RUN mkdir /root/.pip
COPY pip.conf /root/.pip/pip.conf
COPY environment.yml /tmp/environment.yml
RUN conda update -n base -c defaults conda -y
RUN conda install -n base -c conda-forge mamba -y
RUN mamba env update --name base --file /tmp/environment.yml --prune
RUN mamba install -c conda-forge git -y