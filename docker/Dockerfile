# Use ubuntu as the base layer
FROM ubuntu:18.04

# Install apt dependencies
RUN apt-get -yqq update
RUN apt-get -yqq upgrade
# Python dependencies (python2.7 is required for installing PETSc)
RUN apt-get -yqq install python2.7 python3 python3-pip
# Needed to make python2 a runnable command
RUN ln /usr/bin/python2.7 /usr/bin/python2
# Needed for bout-install dependencies
RUN apt-get -yqq install git
RUN apt-get -yqq install build-essential cmake gfortran m4 zlib1g-dev

# Install pip dependecies
RUN pip3 install bout-install

# Install BOUT-dev
RUN bout_install -a

# Set environment variables
ENV PATH="/root/local/bin:${PATH}"
ENV LD_LIBRARY_PATH="/root/local/lib:${LD_LIBRARY_PATH}"
