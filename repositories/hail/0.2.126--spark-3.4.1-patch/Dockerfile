FROM databricksruntime/python:13.3-LTS

ARG HAIL_COMMIT_ID="5b718e1"  # https://github.com/hail-is/hail/commit/5b718e1d3e1d72fad15cc57801601a6e35df41dd
ARG SCALA_VERSION="2.12.0"
ARG SPARK_VERSION="3.4.1"
ARG BREEZE_VERSION="2.1.0"

RUN apt update -y && \
    apt-get install -yq \
      openjdk-8-jre-headless \
      g++ \
      python3 \
      python3-pip \
      libopenblas-base \
      liblapack3 \
      git \
      rsync \
      liblz4-dev 

COPY 0001-spark-to-3.4.1.patch /root/0001-spark-to-3.4.1.patch 

RUN \
    git clone "https://github.com/hail-is/hail.git" && \
    ( \
      cd hail && \
      git checkout "${HAIL_COMMIT_ID}" && \
      git apply /root/0001-spark-to-3.4.1.patch && \
      ( \
        cd hail/ && \
        . /databricks/python3/bin/activate && \
        make install \
          HAIL_COMPILE_NATIVES=1 \
          SCALA_VERSION="${SCALA_VERSION}" \
          SPARK_VERSION="${SPARK_VERSION}"\ && \
        pip install markupsafe==2.0.1 \
      ) \
    ) && \
    rm -rf hail && \
    rm /root/0001-spark-to-3.4.1.patch

