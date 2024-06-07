FROM docker.io/ubuntu:latest

LABEL author="Alexis Lucattini" \
      description="Build RClone" \
      maintainer="alexis.lucattini@umccr.org"

ARG RCLONE_VERSION="v1.66.0"
ARG TARGETPLATFORM

ADD rclone-config-maker.py /usr/local/bin/rclone-config-maker

RUN apt update -y -q && \
    apt install -y -q \
      wget \
      python3 \
      python3-tomli-w && \
    wget \
      --output-document "rclone-${RCLONE_VERSION}-linux-"${TARGETPLATFORM#linux/}".deb" \
      "https://downloads.rclone.org/${RCLONE_VERSION}/rclone-${RCLONE_VERSION}-linux-"${TARGETPLATFORM#linux/}".deb" && \
    dpkg -i "rclone-${RCLONE_VERSION}-linux-${TARGETPLATFORM#linux/}.deb" && \
    chmod +x /usr/local/bin/rclone-config-maker


ENTRYPOINT [ ]
CMD [ "/bin/bash" ]
