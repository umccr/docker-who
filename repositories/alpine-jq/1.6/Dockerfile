FROM alpine:3.13.2

LABEL author="Alexis Lucattini" \
      description="Run JQ v1.6" \
      maintainer="alexis.lucattini@umccr.org"

ARG JQ_VERSION="1.6-r1"

# User args
ARG USER="alpine_user"
ARG UID=1000
ARG GID=1000
ARG GROUP="alpine_group"

RUN addgroup \
    --system \
    --gid "${GID}" \
    "${GROUP}" && \
    adduser \
    --system \
    --disabled-password \
    --ingroup "${GROUP}" \
    --uid "${UID}" \
    "$USER"

RUN apk add --no-cache \
    --repository http://dl-cdn.alpinelinux.org/alpine/v3.13/main jq=${JQ_VERSION}

USER "$USER"

CMD [ "jq" ]