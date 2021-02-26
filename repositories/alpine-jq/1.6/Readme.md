# Alpine-JQ

## Version 1.6

### Usage

Useful when one MUST use jq 1.6 over jq 1.5

More jq documentation can be found [here](https://stedolan.github.io/jq/manual/)

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
> grep "MemTotal" /proc/meminfo

```bash
MemTotal: 7950984 kB
```

#### CPUS
> grep -c "^processor" /proc/cpuinfo

```bash
2
```



