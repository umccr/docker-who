FROM docker.io/alpine:3.13.2

LABEL author="Alexis Lucattini" \
      description="Run yq v4.23.1" \
      maintainer="alexis.lucattini@umccr.org"

ARG YQ_VERSION="4.23.1"

# User args
ARG USER="alpine_user"
ARG UID=1000
ARG GID=1000
ARG GROUP="alpine_group"
ARG TARGETPLATFORM
ARG BUILDPLATFORM

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

RUN wget --quiet \
        --output-document /usr/local/bin/yq \
	"https://github.com/mikefarah/yq/releases/download/v${YQ_VERSION}/yq_linux_${TARGETPLATFORM#linux/}" && \
    chmod +x /usr/local/bin/yq
   

USER "$USER"

CMD [ "yq" ]
