FROM umccr/alpine-conda:4.9.2

LABEL author="Alexis Lucattini" \
      description="Run illumina-interop and then run multiqc" \
      maintainer="alexis.lucattini@umccr.org"

ARG MULTIQC_VERSION="1.9"
ARG ILLUMINA_INTEROP_VERSION="1.1.21"

RUN conda install --quiet --yes \
        --channel bioconda \
        illumina-interop=="${ILLUMINA_INTEROP_VERSION}" && \
    conda install --quiet --yes \
        --channel anaconda \
        pip==21.0.1 && \
    pip install multiqc=="${MULTIQC_VERSION}" && \
    pip cache purge && \
    conda uninstall pip --yes && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.pyc' -delete && \
    /opt/conda/bin/conda clean --yes \
        --all \
        --force-pkgs-dirs \

# Reset entrypoint to null for cwl
ENTRYPOINT []

# Set cwd to multiqc
CMD [ "multiqc" ]
