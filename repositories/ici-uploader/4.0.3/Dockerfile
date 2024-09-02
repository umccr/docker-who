FROM alpine:3

# ARGS
# Target platform (linux/amd64, linux/arm64)
ARG TARGETPLATFORM

# For the ici-uploader
ARG ICI_HOME="/usr/local/share/ici-uploader"
# User args (we run from a non-root user)
ARG USER="ici_user"
ARG UID=1000
ARG GID=1000
ARG GROUP="ici_user"

# ENV
ENV ICI_HOME="${ICI_HOME}"

# RUN
# Install Java
RUN apk update && \
  apk add \
    openjdk11 \
    tar \
    bash && \
  mkdir -p "${ICI_HOME}"

# Add and extract tarball
ADD "ici-uploader.${TARGETPLATFORM#linux/}.tar.gz" "${ICI_HOME%ici-uploader}"
ADD "ici-uploader.sh" "/usr/local/bin/ici-uploader"

# Change permissions
RUN ls "${ICI_HOME}" && chmod a+r "${ICI_HOME}/" && \
    chmod a+x "${ICI_HOME}/ici-uploader" && \
    chmod a+x "/usr/local/bin/ici-uploader"

# Add a non-root user
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

# Change ownership
USER "$USER"

# Add a softlink from the user home to the ici-uploader
RUN mkdir -p "/home/${USER}/.illumina/" && \
    ln -s "${ICI_HOME}" "/home/${USER}/.illumina/ici-uploader"

CMD [ "ici-uploader" ]
