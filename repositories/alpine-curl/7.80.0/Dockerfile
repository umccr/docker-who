FROM docker.io/alpine:3.15

LABEL author="Alexis Lucattini" \
      description="Run curl v7.80" \
      maintainer="alexis.lucattini@umccr.org"

ARG TOOL_NAME="curl"
ARG TOOL_VERSION="7.80.0"
ARG FUZZY="true"
ARG ALPINE_MAIN_REPOSITORY="http://dl-cdn.alpinelinux.org/alpine/v3.15/main"

# User args
ARG USER="alpine_user"
ARG UID=1000
ARG GID=1000
ARG GROUP="alpine_group"

RUN apk update --quiet && \
    if [ "${FUZZY-}" = "true" ]; then \
      TOOL_VERSION="$(apk search --no-cache --repository "${ALPINE_MAIN_REPOSITORY}" \
                        "${TOOL_NAME}" | \
                      grep "^${TOOL_NAME}-${TOOL_VERSION}" | \
                      sed "s%^${TOOL_NAME}-%%")"; \
    fi; \
    apk add --no-cache --repository "${ALPINE_MAIN_REPOSITORY}" \
      "${TOOL_NAME}=${TOOL_VERSION}" \
      "bash"

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

USER "$USER"

CMD [ "${TOOL_NAME}" ]
