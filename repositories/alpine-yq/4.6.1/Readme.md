# Alpine-yq

## Version 4.6.1

### Usage

Useful for querying yaml files in a 'jq' like syntax.      
yq docs can be found [here](https://github.com/mikefarah/yq)

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
MemTotal:        3977908 kB
```

#### CPUS
> grep -c ^processor /proc/cpuinfo

```bash
2
```