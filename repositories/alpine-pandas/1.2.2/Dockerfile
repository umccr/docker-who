FROM umccr/alpine-conda:4.9.2

LABEL author="Alexis Lucattini" \
      description="Pandas in a tiny container" \
      maintainer="alexis.lucattini@umccr.org"

ARG XLRD_VERSION="1.2.0"
ARG PANDAS_VERSION="1.2.2"
ARG NO_MKL_VERSION="3.0"

# Install pandas
RUN conda install --yes \
        --freeze-installed \
        --channel anaconda \
        nomkl="${NO_MKL_VERSION}" \
        xlrd="${XLRD_VERSION}" \
        pandas="${PANDAS_VERSION}" && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.pyc' -delete && \
    /opt/conda/bin/conda clean --yes \
        --all \
        --force-pkgs-dirs

# Set entrypoint to null (for cwl usage)
ENTRYPOINT []

# Reset CMD to python
CMD ["/opt/conda/bin/python"]
