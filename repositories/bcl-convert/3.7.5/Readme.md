# bcl-convert

## Version 3.7.5

### Usage

bcl-convert is used to convert Illumina basecall files (raw output) to fastq files (sequencing reads) split
by samples as per the samplesheet.  
More information on the bcl-convert algorithm and parameters can be found [here](https://sapac.support.illumina.com/sequencing/sequencing_software/bcl-convert.html)

### Build environment

#### OS RELEASE
> cat /etc/os-release

```bash
NAME="Amazon Linux"
VERSION="2"
ID="amzn"
ID_LIKE="centos rhel fedora"
VERSION_ID="2"
PRETTY_NAME="Amazon Linux 2"
ANSI_COLOR="0;33"
CPE_NAME="cpe:2.3:o:amazon:amazon_linux:2"
HOME_URL="https://amazonlinux.com/"
```

#### Memory
> grep MemTotal /proc/meminfo

```bash
MemTotal: 7950984 kB
```

#### CPUS
> grep -c ^processor /proc/cpuinfo

```bash
2
```