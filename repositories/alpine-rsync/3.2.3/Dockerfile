FROM docker.io/alpine:3.13.2

LABEL author="Alexis Lucattini" \
      description="Run rsync 3.2.3" \
      maintainer="alexis.lucattini@umccr.org"

ARG TOOL_NAME="rsync"
ARG TOOL_VERSION="3.2.3"
ARG FUZZY="true"
ARG ALPINE_MAIN_REPOSITORY="http://dl-cdn.alpinelinux.org/alpine/v3.13/main"

# User args
ARG USER="alpine_user"
ARG UID=1000
ARG GID=1000
ARG GROUP="alpine_group"

RUN apk update --quiet && \
    if [[ "${FUZZY-}" == "true" ]]; then \
      TOOL_VERSION="$(apk search --no-cache --repository "${ALPINE_MAIN_REPOSITORY}" \
                        "${TOOL_NAME}" | \
                      grep "^${TOOL_NAME}-${TOOL_VERSION}" | \
                      sed "s%^${TOOL_NAME}-%%")"; \
    fi; \
    apk add --no-cache --repository "${ALPINE_MAIN_REPOSITORY}" \
      "${TOOL_NAME}=${TOOL_VERSION}"

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
