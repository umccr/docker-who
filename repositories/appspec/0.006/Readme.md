# Alpine-yq

## Version 4.6.1

### Usage

For creating autocompletion scripts, more inspiration can be found [here](https://github.com/perlpunk/shell-completions)

### Build environment

#### OS RELEASE
> cat /etc/os-release

```bash
NAME="Ubuntu"
VERSION="20.04.2 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.2 LTS"
VERSION_ID="20.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=focal
UBUNTU_CODENAME=focal
```

#### Memory
> grep MemTotal /proc/meminfo

```bash
MemTotal:       13024996 kB
```

#### CPUS
> grep -c ^processor /proc/cpuinfo

```bash
4
```