# Use alpine as the base layer
FROM python:alpine

# Install dependencies
RUN apk add --no-cache \
 # Needed to clone BOUT-dev
 git \
 # Compiler base
 # https://wiki.alpinelinux.org/wiki/GCC
 # FIXME: May be changed for a different compiler?
 build-base \
 # Needed by mpi (although build-base is installed)
 gfortran \
 # Needed by netcdf
 m4 \
 zlib-dev \
 # Needed by sundials
 cmake \
 # Needed for PETSc
 python2

# Install pip dependecies
RUN pip3 install --no-cache-dir bout-install

# Install BOUT-dev
# Note that we are removing the installation files from the layer
RUN bout_install -a && rm -rf /root/install /root/examples

# Set environment variables
ENV PATH="/root/local/bin:${PATH}"
ENV LD_LIBRARY_PATH="/root/local/lib:${LD_LIBRARY_PATH}"

ENTRYPOINT ["/bin/sh"]