FROM continuumio/miniconda3:25.3.1-1

LABEL author="Alexis Lucattini" \
      description="Runs illumina-interop" \
      maintainer="alexis.lucattini@umccr.org"

# Arguments
ARG ILLUMINA_INTEROP_VERSION="1.5.0-0"
ARG PANDAS_VERSION="2.3.3"
ARG MATPLOTLIB_VERSION="3.10.7"
ARG SEABORN_VERSION="0.13.2"

# Installations
RUN \
    # Prepend conda forge to conda channel priority list  \
    conda config --prepend channels conda-forge && \
    # Install Illumina InterOp via the bioconda channel \
    conda install --yes \
      --channel bioconda \
      illumina-interop=="${ILLUMINA_INTEROP_VERSION}" && \
    # Upgrade pipe and then install pandas / matplotlib and seaborn via pip \
    pip install --upgrade pip && \
    pip install \
      pandas=="${PANDAS_VERSION}" \
      matplotlib=="${MATPLOTLIB_VERSION}" \
      seaborn=="${SEABORN_VERSION}" && \
    # Cleanup our conda installation \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.pyc' -delete && \
    /opt/conda/bin/conda clean --yes \
      --all \
      --force-pkgs-dirs

# Add our script
COPY interop_imaging_plot.py /opt/conda/bin/interop_imaging_plot

# Make our interop_imaging_plot executable
RUN chmod +x /opt/conda/bin/interop_imaging_plot

# Reset entrypoint to null for cwl
ENTRYPOINT []

# Set cwd to multiqc
CMD []
