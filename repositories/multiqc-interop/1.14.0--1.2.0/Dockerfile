FROM ghcr.io/umccr/alpine-conda:22.11.1

LABEL author="Alexis Lucattini" \
      description="Run illumina-interop and then run multiqc" \
      maintainer="alexis.lucattini@umccr.org"

ARG MULTIQC_VERSION="1.14.0"
ARG ILLUMINA_INTEROP_VERSION="1.2.0"

RUN conda install --quiet --yes \
      pip && \
    pip install interop=="${ILLUMINA_INTEROP_VERSION}" && \
    pip install multiqc=="${MULTIQC_VERSION}" && \
    pip cache purge && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.pyc' -delete && \
    /opt/conda/bin/conda clean --yes \
        --all \
        --force-pkgs-dirs

# Reset entrypoint to null for cwl
ENTRYPOINT []

# Set cwd to multiqc
CMD [ "multiqc" ]
