FROM continuumio/miniconda3:23.10.0-1

LABEL author="Alexis Lucattini" \
      description="Runs illumina-interop" \
      maintainer="alexis.lucattini@umccr.org"

ARG ILLUMINA_INTEROP_VERSION="1.3.1"

RUN conda config --prepend channels conda-forge && \
    conda install -c bioconda illumina-interop=="${ILLUMINA_INTEROP_VERSION}" && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.pyc' -delete && \
    /opt/conda/bin/conda clean --yes \
        --all \
        --force-pkgs-dirs

# Reset entrypoint to null for cwl
ENTRYPOINT []

# Set cwd to multiqc
CMD []
