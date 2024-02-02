FROM docker.io/ubuntu:latest

LABEL author="Alexis Lucattini" \
      description="Run basespace cli" \
      maintainer="alexis.lucattini@umccr.org"

ARG BASESPACE_CLI_VERSION="1.5.4"

ADD bs.${BASESPACE_CLI_VERSION}.bin /usr/bin/bs

RUN apt update -y -q && \
    apt install ca-certificates -y -q && \
    chmod +x /usr/bin/bs

ENTRYPOINT [ ]
CMD [ "bs" ]
