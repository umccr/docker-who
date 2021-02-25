<p align="center"><img src="docs/images/readme-main.png" alt="docker-who-logo" width="1014"></p>

# Dockerwho <!-- omit in toc -->

- [Contributing](#contributing)
  - [Folder structure](#folder-structure)
  - [Docker tags / labels](#docker-tags--labels)
  - [Readme](#readme)
- [Auto-creation of Latest tags with GitHub actions](#auto-creation-of-latest-tags-with-github-actions)

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

## Auto-creation of Latest tags with GitHub actions 

The latest tag will be automatically created / updated on pushes to the 'main' branch.    
GitHub Actions will push the 'latest' tag based on the latest version in the repo on the following conditions:
  * The 'latest' tag does not exist for this repository. 
  * OR The 'latest' tag checksum does not match the latest version in the repo AND the latest version has a creation time
    AFTER the 'latest' tag creation time.  
    




