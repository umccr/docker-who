FROM debian:latest

ARG TARGETPLATFORM
ARG ORA_MOUNT="/opt"

# Standard update and install wget
RUN apt update -yq && \
  apt install -yq && \
  mkdir -p "${ORA_MOUNT}"

# Copy over the main orad refdata and binary
# Data from "https://s3.amazonaws.com/webdata.illumina.com/downloads/software/dragen-decompression/orad.2.7.0.linux.tar.gz"
COPY orad.2.7.0.linux.tar.gz /tmp/orad.tar.gz

RUN tar \
    --directory "${ORA_MOUNT}" \
    --gzip \
    --extract \
    --file /tmp/orad.tar.gz \
    --strip-components=1 && \
  ( \
    cd /usr/local/bin && \
    ln -s "${ORA_MOUNT}/orad" orad \
  )

# We have an arm copy of the orad binary
# So we add that in here as well
COPY orad-arm64.tar.gz /tmp/orad-arm64.tar.gz

RUN if [[ "${TARGETPLATFORM#linux/}" == "arm64" ]]; then \
      tar -xzf /tmp/orad-arm64.tar.gz -C "${ORA_MOUNT}"; \
    fi && \
    rm /tmp/orad-arm64.tar.gz;

# Set the ora reference to the path ORA_MOUNT/oradata
ENV ORADATA_PATH="${ORA_MOUNT}/oradata/"

# Update the cmd to run orad
CMD [ "orad" ]
