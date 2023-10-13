FROM continuumio/anaconda3:2023.09-0

LABEL author="Alexis Lucattini" \
      description="Run illumina-interop and then run multiqc" \
      maintainer="alexis.lucattini@umccr.org"

ARG MULTIQC_VERSION="1.14.0"
ARG ILLUMINA_INTEROP_VERSION="1.2.0"

RUN conda config --prepend channels conda-forge && \
    conda install -c bioconda multiqc=="${MULTIQC_VERSION}" && \
    conda install -c bioconda illumina-interop=="${ILLUMINA_INTEROP_VERSION}" && \ 
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.pyc' -delete && \
    /opt/conda/bin/conda clean --yes \
        --all \
        --force-pkgs-dirs

# Reset entrypoint to null for cwl
ENTRYPOINT []

# Set cwd to multiqc
CMD [ "multiqc" ]
