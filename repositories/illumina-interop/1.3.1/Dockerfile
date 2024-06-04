FROM continuumio/miniconda3:23.10.0-1

LABEL author="Alexis Lucattini" \
      description="Runs illumina-interop" \
      maintainer="alexis.lucattini@umccr.org"

ARG ILLUMINA_INTEROP_VERSION="1.3.1"
ARG PANDAS_VERSION="2.2.2"
ARG MATPLOTLIB_VERSION="3.9.0"
ARG SEABORN_VERSION="0.13.2"

COPY interop_imaging_plot.py /opt/conda/bin/interop_imaging_plot

RUN conda config --prepend channels conda-forge && \
    conda install -y -c bioconda illumina-interop=="${ILLUMINA_INTEROP_VERSION}" && \
    pip install --upgrade pip && \
    pip install \
        pandas=="${PANDAS_VERSION}" \
        matplotlib=="${MATPLOTLIB_VERSION}" \
        seaborn=="${SEABORN_VERSION}" && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.pyc' -delete && \
    /opt/conda/bin/conda clean --yes \
        --all \
        --force-pkgs-dirs && \
    chmod +x  /opt/conda/bin/interop_imaging_plot

# Reset entrypoint to null for cwl
ENTRYPOINT []

# Set cwd to multiqc
CMD []
