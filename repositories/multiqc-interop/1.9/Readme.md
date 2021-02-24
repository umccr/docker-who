# multiqc-interop

## Version 1.9

### Usage

multiqc-interop uses the [multiqc](https://multiqc.info/) package to generate quality control information of an
illumina sequencing run.  One must first run the interop commands `interop_index-summary` and `interop_summary`
and parse the outputs of these as positional parameters to the multiqc-interop command.  
You can read more on interop data [here](https://illumina.github.io/interop/index.html)

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