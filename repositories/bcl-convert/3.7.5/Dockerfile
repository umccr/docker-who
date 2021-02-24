FROM centos:7

LABEL author="Alexis Lucattini" \
      description="Run bcl-convert 3.7.5 from a container" \
      maintainer="alexis.lucattini@umccr.org"

# This docker file was created with inspiration from
# https://gist.github.com/pansapiens/f66bdb59230004eba0d7fdec9e7eb5d8
# 
# You'll need to download bcl-convert.3.7.5.rpm from
# https://sapac.support.illumina.com/sequencing/sequencing_software/bcl-convert/downloads.html
# Yay clickwrap licenses !
#
# Building:
#
# docker build -t umccr/bcl-convert:latest-cwl -t umccr/bcl-convert:3.7.5-cwl
#
# Running:
#
# bcl-convert wants to be able to write to /var/logs/bcl-convert, so we bind a user writable directory for it
# mkdir logs
# singularity exec --bind logs:/var/log/bcl-convert bcl-convert.sif bcl-convert --help
# _or_
# singularity exec -wf bcl-convert.sif bcl-convert --help
#

# Add in RPM file
ADD bcl-convert.rpm /tmp/bcl-convert.rpm

# Install with groupinstall compiler tools
# -y -q for peace and quietness
RUN yum update -y -q && \
    yum groupinstall -y -q "Development Tools" && \
    yum update -y -q && \
    rpm -i /tmp/bcl-convert.rpm && \
    rm /tmp/bcl-convert.rpm && \
    yum clean all && \
    rm -rf /var/cache/yum

# This is so that bcl-convert can write a small little file to this folder
# When running with singularity use 
# --bind $(mktemp -d):/var/log/bcl-convert
# Docker should be able to handle with just this if --read-only=true is set
# as is done when running through cwltool locally
VOLUME /var/log/bcl-convert

# Set the entrypoint to null so that the Dockerfile
# is compatible with the cwl spec
ENTRYPOINT []
