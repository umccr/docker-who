# Alpine-pandas

## Version 1.2.2

### Usage

Used when manipulating small csv files often in CWL tools.    
Pandas documentation can be found [here](https://pandas.pydata.org/docs/).

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