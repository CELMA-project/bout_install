# Building BOUT_dev
# docker build -f Dockerfile -t bout_dev:latest .

# Inspired by
# https://dev.to/faizanbashir/building-python-data-science-container-usingdocker-3f8p

# Use alpine as the base layer
FROM python:alpine

# Install dependencies
RUN apk add --no-cache \
    # Needed to clone BOUT-dev
    git \
    # Compiler base
    # https://wiki.alpinelinux.org/wiki/GCC
    build-base \
    # Needed by mpi (although build-base is installed)
    gfortran \
    # Needed by netcdf
    m4 \
    zlib-dev \
    # Needed by sundials
    cmake \
    # Needed for PETSc
    python2 \
    # Install pip dependencies
    && pip3 install --no-cache-dir bout-install \
    # Install BOUT-dev
    && bout_install -a \
    # Cleanup
    && apk del cmake python2 \
    && rm -rf /root/install /root/examples /var/cache/apk/*

# Set environment variables
ENV PATH="/root/local/bin:${PATH}"
ENV LD_LIBRARY_PATH="/root/local/lib:${LD_LIBRARY_PATH}"

ENTRYPOINT ["/bin/sh"]