FROM docker.io/centos:centos7

LABEL author="Alexis Lucattini" \
      description="Run appspec" \
      maintainer="alexis.lucattini@umccr.org"

ARG APPSPEC_VERSION="0.006"

# User args
ARG USER="centos_user"
ARG UID=1000
ARG GID=1000
ARG GROUP="centos_group"

# Update yum cache
# Install required packages
# Run cpanm
RUN yum update -y && \
    yum install -y -q \
      openssl-devel \
      wget \
      yum-utils \
      gcc && \
    yum install -y -q \
      perl-devel \
      perl-CPAN \
      perl-App-cpanminus \
      perl-Test-Simple \
      perl-ExtUtils-MakeMaker \
      perl-JSON && \
    yum install -y -q \
      python3 && \
    cpanm --quiet "List::Util" && \
    cpanm --quiet "List::MoreUtils" && \
    cpanm --quiet "App::AppSpec@${APPSPEC_VERSION}" && \
    yum clean all && \
    rm -rf /var/cache/yum && \
    rm -rf /root/.cpanm

# Create group/user
RUN groupadd \
        --system \
        --gid "$GID" \
        "$GROUP" && \
    useradd \
        --system \
        --gid "$GID" \
        --no-create-home \
        --uid "$UID" \
        "$USER"

# Set user
USER "$USER"

CMD [ "appspec" ]
