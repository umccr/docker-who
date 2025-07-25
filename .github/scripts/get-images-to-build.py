#!/usr/bin/env python3

"""
Get images to build and output the following to stdout

echo "::set-output name=images_to_build::['a','b','c']"
echo "::set-output name=image_versions_to_build::['a','b','c']"
"""

# Imports
import json
import subprocess
from os import environ
from datetime import datetime, timezone
from typing import List, Optional, Dict
from pathlib import Path
import logging
import sys
import re

# Globals
REPOSITORY_PATH = Path("repositories")
REPO_NAME = environ["REPO_NAME"]
DOCKER_REGISTRY_PREFIX = "docker://ghcr.io"

# Set logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s',
                              '%m-%d-%Y %H:%M:%S')
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setFormatter(formatter)
logger.addHandler(stderr_handler)


## Folder functions
def get_folder_list() -> List[Path]:
    """
    Get folder list
    :return:
    """
    folder_list = []
    for image_dir in REPOSITORY_PATH.glob("*/*"):
        if not image_dir.is_dir():
            continue
        if not (image_dir / "Dockerfile").is_file():
            continue
        folder_list.append(Path(REPOSITORY_PATH) / image_dir.relative_to(REPOSITORY_PATH))

    logger.info(f"Got {len(folder_list)} image paths to asses through")
    return folder_list


def get_folder_modified_time(folder_path: Path) -> Optional[datetime]:
    """
    Get folder modification time through git
    :param folder_path
    :return:
    """
    # Get the last date a file changed in this path in epoch time
    get_date_proc = subprocess.run(["git", "log", "-1", "--format=%aI", "--", f"{folder_path}/"],
                                   capture_output=True)

    # Check all g
    if not get_date_proc.returncode == 0:
        logger.error(f"Could not get date from command \"{' ,'.join(get_date_proc.args)}\"")
        logger.error(f"Stderr was: {get_date_proc.stderr.decode()}")
        return None

    folder_modification_time = datetime.fromisoformat(get_date_proc.stdout.decode().strip())

    logger.info(f"Folder path modification time for {folder_path} was {folder_modification_time}")
    return datetime.fromtimestamp(folder_modification_time.timestamp(), tz=timezone.utc)


## Docker functions

# Pull the skopeo image from quay.io
def pull_skopeo_image() -> None:
    docker_pull_proc = subprocess.run(["docker", "pull", "quay.io/skopeo/stable"],
                                      capture_output=True)

    if not docker_pull_proc.returncode == 0:
        logger.error(f"Could not pull skopeop image with command \"{', '.join(docker_pull_proc.args)}\"")
        logger.error(f"Stderr was: {docker_pull_proc.stderr.decode()}")

    logger.info("Pulled down the skopeo image")


# Check docker exists first
def docker_exists(repo_name: str, image_name: str) -> Optional[bool]:
    # Test the list-tags command, a non zero exit code means the docker image likely doesn't exist
    list_docker_tags_proc = subprocess.run(["docker", "run", "--rm", "quay.io/skopeo/stable",
                                            "list-tags", f"{DOCKER_REGISTRY_PREFIX}/{repo_name}/{image_name}"],
                                           capture_output=True)

    if list_docker_tags_proc.returncode == 0:
        logger.info(f"Was able to list tags, image \"{DOCKER_REGISTRY_PREFIX}/{repo_name}/{image_name}\" exists")
        return True
    elif list_docker_tags_proc.returncode == 1:
        logger.info(f"Got exit code 1 for \"{', '.join(list_docker_tags_proc.args)}\". "
                    f"This means that the image does not exist on ghrc.io")
        return False
    else:
        logger.error(f"Unknown error when trying to determine if image exists. "
                     f"Got exit code {list_docker_tags_proc.returncode} for \"{', '.join(list_docker_tags_proc.args)}\". "
                     f"Stderr was: {list_docker_tags_proc.stderr.decode()} ")
        return None


def get_docker_tags_from_image(repo_name: str, image_name: str) -> Optional[List]:
    # Test the list-tags command, a non zero exit code means the docker image likely doesn't exist
    list_docker_tags_proc = subprocess.run(["docker", "run", "--rm", "quay.io/skopeo/stable",
                                            "list-tags", f"{DOCKER_REGISTRY_PREFIX}/{repo_name}/{image_name}"],
                                           capture_output=True)

    if not list_docker_tags_proc.returncode == 0:
        logger.error(f"Could not list tags, image \"docker.io/ghcr.io/{repo_name}/{image_name}\" exists"
                     f"Got exit code {list_docker_tags_proc.returncode} for \"{', '.join(list_docker_tags_proc.args)}\". "
                     f"Stderr was: {list_docker_tags_proc.stderr.decode()} ")

    list_tags_json_output: Dict = json.loads(list_docker_tags_proc.stdout.decode().strip())

    if 'Tags' not in list_tags_json_output.keys():
        logger.error(f"Expected 'Tags' in list of keys from list-tags command. Got \"{', '.join(list_tags_json_output.keys())}\" instead.")
        return None

    return list_tags_json_output["Tags"]


def get_docker_image_creation_time(repo_name: str, image_name: str, image_version: str) -> Optional[datetime]:
    """
    Get creation date of docker image
    :param repo_name:
    :param image_name:
    :param image_version:
    :return:
    """
    get_inspection_json_proc = subprocess.run(["docker", "run", "--rm",
                                               "quay.io/skopeo/stable", "inspect",
                                               f"{DOCKER_REGISTRY_PREFIX}/{repo_name}/{image_name}:{image_version}"],
                                              capture_output=True)
    # Check all g
    if not get_inspection_json_proc.returncode == 0:
        logger.error(f"Could not get date from command \"{', '.join(get_inspection_json_proc.args)}\"")
        logger.error(f"Stderr was: {get_inspection_json_proc.stderr.decode()}")
        return None

    # Get creation stamp
    inspection_object = json.loads(get_inspection_json_proc.stdout.decode().strip())

    if 'Created' not in inspection_object.keys():
        return None

    # Ditch microseconds and replace 'Z' with iso format in UTC time
    creation_time_str = re.sub("\.\d+Z", "+00:00", inspection_object["Created"])

    # Return as datetime object
    return datetime.fromtimestamp(datetime.fromisoformat(creation_time_str).timestamp(), tz=timezone.utc)


## Main
def main():
    # Get folders
    folder_list: List[Path] = get_folder_list()

    # Initialise outputs
    images_tags_to_build: List[str] = []

    # Pull skopeo image to assess docker tags
    pull_skopeo_image()

    # Iterate over folders
    for image_path in folder_list:
        # Get image name and image version from image path
        image_name, image_version = str(image_path.relative_to(REPOSITORY_PATH)).split("/")

        # If docker image doesn't exist, then we definitely need to build this image
        if not docker_exists(REPO_NAME, image_name):
            logger.info(f"Docker image for {image_name} doesn't exist so adding {image_name}:{image_version} to build list")
            images_tags_to_build.append(f"{image_name}:{image_version}")
            continue

        image_tag_list: Optional[List] = get_docker_tags_from_image(REPO_NAME, image_name)
        if image_tag_list is None or image_version not in image_tag_list:
            logger.info(f"Could not find \"{image_version}\" in tag list \"{', '.join(image_tag_list) if image_tag_list is not None else 'None'}\" ")
            images_tags_to_build.append(f"{image_name}:{image_version}")
            continue

        # If the docker image does exist, check if it was created before or after the folder was last edited
        folder_modification_time: Optional[datetime] = get_folder_modified_time(image_path)
        docker_image_creation_time: Optional[datetime] = get_docker_image_creation_time(REPO_NAME, image_name, image_version)
        if folder_modification_time is None or docker_image_creation_time is None:
            logger.info(f"Got 'None' for folder_modification_time {folder_modification_time} or 'None' for docker image creation time {docker_image_creation_time}")
            logger.info("Rebuilding")
            images_tags_to_build.append(f"{image_name}:{image_version}")
        elif docker_image_creation_time < folder_modification_time:
            logger.info(f"Rebuilding {image_name}:{image_version} since folder modification time {folder_modification_time} is later than image creation time {docker_image_creation_time}")
            images_tags_to_build.append(f"{image_name}:{image_version}")
        else:
            logger.info(f"Skipping build of {image_name}:{image_version}, folder has not been updated since docker container exists")
            continue

    # Print out image_tags_to_build as a json string that GitHub Actions will read
    image_tags_as_json_string = json.dumps(images_tags_to_build).replace(", ", ",")

    if environ.get("GITHUB_OUTPUT", None) is None:
        print(f"::set-output name=image_tags_to_build::{image_tags_as_json_string}")
    else:
        # Write things the 'new way' for GitHub Actions
        with open(environ.get("GITHUB_OUTPUT"), 'a') as github_output_h:
            github_output_h.write(f"image_tags_to_build={image_tags_as_json_string}\n")

if __name__ == "__main__":
    main()
