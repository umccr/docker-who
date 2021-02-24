# Alpine-Conda

## Version 4.9.2

### Usage

Used mainly for building other alpine containers that rely on conda.  

Set environment variables `$EXTRA_CONDA_PACKAGES` or `$EXTRA_PIP_PACKAGES` at run-time in order to install 
more packages 'on-the-fly'.   

See [this article](https://jcristharif.com/conda-docker-tips.html) for reducing docker image sizes that use 
conda.

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



