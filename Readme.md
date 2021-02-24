<p align="center"><img src="docs/images/readme-main.png" alt="docker-who-logo" width="1014"></p>

# Dockerwho

A miscellaneous set of UMCCR dockerfiles that don't quite go anywhere else.    
This repo contains mostly containers used in our CWL pipelines.

## Contributing

### Folder structure

```text
repository-name
└── major.minor.patch
    ├── Dockerfile
    ├── Readme.md
    └── additional-file
```

where the docker image is tagged as `umccr/<repository-name>:major.minor.patch` (patch is optional).

### Docker tags / labels

Please lay out your LABEL attributes at the top of the Dockerfile with the following attributes

```dockerfile
LABEL author="your name" \
      description="A small description of the docker file" \
      maintainer="your@emailaddress.com"
```

### Readme

Complementing each Dockerfile should be a small Readme.md file.  

This should be a short document containing the following information.

1. Further resources:
  * Links to more online help for using this container.
  * Links to GitHub repositories that are used in this repo.
  * References to others when the dockerfile has been mostly inspired / derived from another source.

2. Build information:
  * The os-release of the host system where this container was built.
    * This can often be found at `/etc/os-release`.

### Latest tags :construction:

At the moment we're avoiding using `latest` tags as this can be dynamic.   
The end-goal is to have a GitHub actions that creates/bumps the latest tag to the appropriate version found in each repository.  



