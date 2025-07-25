FROM debian:latest

ARG TARGETPLATFORM
ARG ORAD_URL="https://s3.amazonaws.com/webdata.illumina.com/downloads/software/dragen-decompression/orad.2.7.0.linux.tar.gz"

RUN apt update -yq && \
  apt install -yq \
    wget && \
  mkdir -p /opt/ && \
  wget --quiet \
    --output-document /dev/stdout \
    "${ORAD_URL}" | \
  tar \
    --directory /opt/ \
    --gzip \
    --extract \
    --file - \
    --strip-components=1 && \
  ( \
    cd /usr/local/bin && \
    ln -s /opt/orad orad \
  )

COPY orad-arm64.tar.gz /tmp/orad-arm64.tar.gz

RUN if [[ TARGETPLATFORM == "linux/arm64" ]]; then \
      tar -xzf /tmp/orad-arm64.tar.gz -C /opt/; \
    fi && \
    rm /tmp/orad-arm64.tar.gz;

CMD [ "orad" ]
