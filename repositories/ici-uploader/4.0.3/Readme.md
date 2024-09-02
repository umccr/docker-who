# Alpine-rsync

## Version 3.3.0

## Package link
[docker-who/alpine-rsync](https://github.com/umccr/docker-who/pkgs/container/alpine-rsync)

## Platforms
* linux/amd64
* linux/arm64

### Usage

```bash
docker pull ghcr.io/umccr/ici-uploader:4.0.3
```

### Description
Run the ici-uploader commandline tool without needing to worry about daemons, or even installing this thing!!

### Example
```bash
docker run --rm -it \
  --workdir "$PWD" \
  --volume "$PWD:$PWD" \
  ici-uploader:4.0.3 \
    ici-uploader help
```

Gives 

```
Usage: ici-uploader.jar [-hV] [--verbose] [--configFile=<configFile>] [COMMAND]
ICI Command-line Interface (Uploader) for analysis, and file operations
      --configFile, --config-file=<configFile>
                  [Optional] Path to the uploader configuration file. Defaults to ~/.illumina/ici-uploader/uploader-config.json.
  -h, --help      Show this help message and exit.
  -V, --version   Print version information and exit.
      --verbose   [Optional] Turn on INFO logging.
Commands:
  help                Displays help information about the specified command
  configure           Configure ici-uploader tool
  case-data           Set the metadata for the case via ici-uploader tool
  analyses, analysis  Upload analyses into Illumina Connected Insights (ICI)
  logs, ici-logs      Get ICI logs for Illumina Connected Insights (ICI)
  files               List or download files
```

## Configuration File

The only way to get this is to actually download the installer from the ICI site, this will provide you with the following keys

```json
[ {
  "domain" : null,
  "workgroup" : null,
  "url" : null,
  "apiKey" : null,
  "project" : null,
  "productKey" : null,
  "isCloud" : null,
  "isActive" : null
} ]
```