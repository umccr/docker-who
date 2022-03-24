FROM docker.io/continuumio/miniconda3:4.9.2-alpine

LABEL author="Alexis Lucattini" \
      description="Conda repo" \
      maintainer="alexis.lucattini@umccr.org"

# Tell Python not to recreate the bytecode files. Since this is a docker image,
# these will be recreated every time, writing them just uses unnecessary disk
# space.
ARG CONDA_VERSION=4.9.2
ENV PYTHONDONTWRITEBYTECODE=true
# Set environment path to this conda
ENV PATH=/opt/conda/bin:$PATH

# We do the following all in one block:
# - Create user and group anaconda
# - Install miniconda install dependencies
# - Download miniconda and check the md5sum
# - Install miniconda
# - Install tini
# - Remove all conda managed static libraries
# - Remove all conda managed *.pyc files
# - Cleanup conda files
# - Uninstall miniconda install dependencies
# Allow chown into opt so that the user can write/ create additional installations

RUN addgroup \
        -S anaconda && \
    adduser \
        -D \
        -G anaconda \
        anaconda

RUN echo ". /opt/conda/etc/profile.d/conda.sh" >> /home/anaconda/.profile && \
    echo "conda activate base" >> /home/anaconda/.profile && \
    /opt/conda/bin/conda install --yes --quiet \
        conda=="$CONDA_VERSION" && \
    echo "conda==$CONDA_VERSION" >> /opt/conda/conda-meta/pinned && \
    /opt/conda/bin/conda install --yes --quiet \
        --freeze-installed \
        tini && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.pyc' -delete && \
    /opt/conda/bin/conda clean --yes \
        --all \
        --force-pkgs-dirs && \
    chown -R anaconda:anaconda /opt/

COPY start.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/start.sh

USER anaconda

ENTRYPOINT ["/opt/conda/bin/tini", "-g", "--", "/usr/local/bin/start.sh"]

CMD ["sh", "--login", "-i"]
