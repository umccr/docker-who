FROM debian:latest

ARG SAMTOOLS_URL="https://github.com/samtools/samtools/releases/download/1.17/samtools-1.17.tar.bz2"
ARG AWS_URL="https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"

# Updates
RUN apt update -y -q && \
  apt install -y -q \
    wget \
    curl \
    unzip \
    build-essential \
    libncurses5-dev \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev && \
  curl \
    --fail \
    --location \
    --show-error \
    --silent \
    --output "awscliv2.zip" \
    "${AWS_URL}" && \
  unzip -q "awscliv2.zip" && \
  ./aws/install && \
  rm -rf "awscliv2.zip" "aws/" && \
  wget --quiet "${SAMTOOLS_URL}" && \
  bunzip2 "samtools"*".bz2" && \
  tar -xf "samtools"*".tar" && \
  ( \
     cd "samtools"* && \
     ./configure && \
     make && \
     make install \
  )
  
ENTRYPOINT [ ]
CMD [ "bash" ]

