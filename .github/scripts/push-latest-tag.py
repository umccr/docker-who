#!/usr/bin/env python3

"""
Given a repository and latest tag in environment args
Check if tag is the latest on docker and if so push as the latest tag

Credit where it's due:
* Pushing a fat manifest tag:
  * https://sher-chowdhury.medium.com/copying-fat-manifests-from-one-docker-registry-to-another-d9e52aba8555

"""

# Imports
from os import environ
import logging
import subprocess
import sys
import json
from typing import Dict, List, Optional, Union
import hashlib
from semantic_version import Version

# Globals
SKOPEO_IMAGE = "quay.io/skopeo/stable:latest"

# Glocals
REGISTRY = environ["REGISTRY"]
REGISTRY_PREFIX = f"docker://{REGISTRY}"
ORG_NAME = environ["ORG_NAME"]
USERNAME = environ["USERNAME"]
PASSWORD = environ["PASSWORD"]
REPO_TAG = environ["REPO_TAG"]

# Set logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s',
                              '%m-%d-%Y %H:%M:%S')
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setFormatter(formatter)
logger.addHandler(stderr_handler)

# Functions
def is_valid_version(version_str: str) -> bool:
    """
    Determine if a valid version
    :param version_object:
    :return:
    """

    try:
        _ = Version(version_str)
        return True
    except ValueError:
        return False


def pull_skopeo_container() -> None:
    """
    Pull down the skopeo container
    :return:
    """
    logger.info(f"Pulling down the skopeo image \"{SKOPEO_IMAGE}\"")

    docker_pull_proc = subprocess.run(["docker", "pull", f"{SKOPEO_IMAGE}"],
                                      capture_output=True)

    if not docker_pull_proc.returncode == 0:
        logger.error(f"Could not successfully pull down the skopeo image \"{SKOPEO_IMAGE}\"")
        logger.error(f"Args were {', '.join(docker_pull_proc.args)}")
        logger.error(f"Stderr was {docker_pull_proc.stderr.decode()}")

        sys.exit(1)

    logger.info(f"Pulled down the skopeo image \"{SKOPEO_IMAGE}\"")


def create_skopeo_container() -> str:
    """
    Create the skopeo container and return the container id
    :return:
    """

    # Create docker container
    docker_create_container_proc = subprocess.run(["docker", "create",
                                                   "--entrypoint", "/bin/bash",
                                                   "--interactive",
                                                   f"{SKOPEO_IMAGE}"],
                                                  capture_output=True)

    if not docker_create_container_proc.returncode == 0:
        logger.error(f"Error creating the skopeo container, args were {', '.join(docker_create_container_proc.args)}")
        logger.error(f"Stderr was {docker_create_container_proc.stderr.decode()}")
        sys.exit(1)

    docker_container_id = docker_create_container_proc.stdout.decode().strip()

    return docker_container_id


def start_skopeo_container(container_id) -> None:
    """
    In theory this function and the one above could have been merged
    But nice to separate things out a little ey?
    :param container_id:
    :return:
    """
    # Create docker container
    docker_start_container_proc = subprocess.run(["docker", "start", f"{container_id}"],
                                                  capture_output=True)

    if not docker_start_container_proc.returncode == 0:
        logger.error(f"Error starting the skopeo container, args were {', '.join(docker_start_container_proc.args)}")
        logger.error(f"Stderr was {docker_start_container_proc.stderr.decode()}")
        sys.exit(1)


def check_container_is_running(container_id) -> bool:
    """
    Check that the start command actually got out container to start running
    :param container_id:
    :return:
    """
    docker_running_check_proc = subprocess.run(["docker", "container", "inspect",
                                                "--format", "{{.State.Running}}",
                                                container_id],
                                               capture_output=True)

    if not docker_running_check_proc.returncode == 0:
        logger.error(f"Error creating the skopeo container, args were {', '.join(docker_running_check_proc.args)}")
        logger.error(f"Stderr was {docker_running_check_proc.stderr.decode()}")
        sys.exit(1)

    # Output is either 'true' or 'false'
    return json.loads(docker_running_check_proc.stdout.decode())


def login_to_ghcr_in_skopeo_container(org_name: str, username: str, password: str, container_id: str) -> None:
    """
    Log in to the ghcr org_name inside the running skopeo container
    :param org_name:
    :param username:
    :param password:
    :param container_id:
    :return:
    """

    # Get login proc
    login_proc = subprocess.run(["docker", "exec",
                                 "--interactive",
                                 f"{container_id}",
                                 "skopeo", "login", f"{REGISTRY}",
                                 "--username", f"{username}",
                                 "--password-stdin"],
                                input=password.encode(),
                                capture_output=True,
                                # Don't hang for more than 20 seconds
                                timeout=20)

    # Check login proc succeeded
    if not login_proc.returncode == 0:
        logger.error(f"Error logging in to skopeo container, args were {', '.join(login_proc.args)}")
        logger.error(f"Stderr was {login_proc.stderr.decode()}")
        sys.exit(1)

    logger.info("Successfully logged into ghcr.io")


def check_login_in_skopeo_container(org_name: str, username: str, container_id: str) -> None:
    """
    Check that the login returns the user we expected
    :param org_name:
    :param username:
    :param container_id:
    :return:
    """

    # Get login proc
    check_login_proc = subprocess.run(["docker", "exec",
                                       "--interactive",
                                       f"{container_id}",
                                       "skopeo", "login",
                                       "--get-login", f"{REGISTRY}"],
                                       capture_output=True,
                                       # Don't hang for more than 20 seconds
                                       timeout=20)

    # Check login proc succeeded
    if not check_login_proc.returncode == 0:
        logger.error(f"Error checking login args were {', '.join(check_login_proc.args)}")
        logger.error(f"Stderr was {check_login_proc.stderr.decode()}")
        sys.exit(1)

    login_username = check_login_proc.stdout.decode().strip()

    if not login_username == username:
        logger.error(f"Expected login of {username} but got {login_username}")
        sys.exit(1)


def get_tags_of_image(org_name: str, image_name: str, container_id):
    """
    Get tags of an image
    :param org_name:
    :param image_name:
    :param container_id:
    :return:
    """

    list_tags_proc = subprocess.run(["docker", "exec",
                                     "--interactive",
                                     f"{container_id}",
                                     "skopeo", "list-tags",
                                     f"{REGISTRY_PREFIX}/{org_name}/{image_name}"],
                                    capture_output=True)

    if not list_tags_proc.returncode == 0:
        logger.error(f"Error listing tags, args were {', '.join(list_tags_proc.args)}")
        logger.error(f"Stderr was {list_tags_proc.stderr.decode()}")
        sys.exit(1)

    list_tags_json_output: Dict = json.loads(list_tags_proc.stdout.decode().strip())

    if 'Tags' not in list_tags_json_output.keys():
        logger.error(f"Expected 'Tags' in list of keys from list-tags command. Got \"{', '.join(list_tags_json_output.keys())}\" instead.")
        return None

    return list_tags_json_output["Tags"]


def is_tag_latest(tag_list: List, image_version: str) -> bool:
    """
    Compare this tag to all the tags and determine if its the latest version
    :param tag_list:
    :param image_version:
    :return:
    """

    # Ensure image_version can be parsed
    if not is_valid_version(image_version):
        logger.error(f"Cannot parse image version: \"{image_version}\"")
        raise ValueError

    # Filter non-semver tags (like latest)
    versioned_tag_list = filter(lambda x: is_valid_version(x), tag_list)

    for tag in versioned_tag_list:
        if Version(image_version) < Version(tag):
            return False

    return True


def get_hex_digest(org_name: str, image_name: str, image_version: str, container_id: str) -> str:
    """
    Get the hex digest of the manifest file
    :param org_name:
    :param image_name:
    :param image_version:
    :param container_id:
    :return:
    """

    get_manifest_digest_proc = subprocess.run(["docker", "exec",
                                               "--interactive", f"{container_id}",
                                               "skopeo", "inspect",
                                               "--raw",
                                               f"{REGISTRY_PREFIX}/{org_name}/{image_name}:{image_version}"],
                                              capture_output=True)

    if not get_manifest_digest_proc.returncode == 0:
        logger.error(f"Error getting manifest, args were {', '.join(get_manifest_digest_proc.args)}")
        logger.error(f"Stderr was {get_manifest_digest_proc.stderr.decode()}")
        sys.exit(1)


    # Get manifest file as a raw json
    manifest_json_str = get_manifest_digest_proc.stdout.decode().strip()

    # Get hashlib
    shasum_str = hashlib.sha256(manifest_json_str.encode()).hexdigest()

    logger.info(f"Got the manifest {shasum_str} for manifest \"{REGISTRY_PREFIX}/{org_name}/{image_name}:{image_version}\"")

    return shasum_str


def push_latest(org_name: str, image_name: str, image_version:str, manifest_shasum: str, container_id) -> None:
    """
    Run copy command inside skopeo container to push image version to latest
    :param org_name:
    :param image_name:
    :param image_version:
    :param manifest_shasum:
    :param container_id:
    :return:
    """

    copy_proc = subprocess.run(["docker", "exec",
                                "--interactive", f"{container_id}",
                                "skopeo", "copy",
                                "--all",
                                f"{REGISTRY_PREFIX}/{org_name}/{image_name}@sha256:{manifest_shasum}",
                                f"{REGISTRY_PREFIX}/{org_name}/{image_name}:latest"],
                               capture_output=True)

    # Check copy proc succeeded
    if not copy_proc.returncode == 0:
        logger.error(f"Error copying container, args were {', '.join(copy_proc.args)}")
        logger.error(f"Stderr was {copy_proc.stderr.decode()}")
        sys.exit(1)

    logger.info(f"Successfully copied the container from "
                f"\"{REGISTRY_PREFIX}/{org_name}/{image_name}:{image_version}\" to "
                f"\"{REGISTRY_PREFIX}/{org_name}/{image_name}:latest\"")



def main():
    # Step 1: Pull down skopeo container
    pull_skopeo_container()

    # Step 2: Start container
    container_id = create_skopeo_container()
    start_skopeo_container(container_id=container_id)

    # Step 2a: Check container has started
    check_container_is_running(container_id=container_id)

    # Step 3: Log in to ghcr in skopeo container
    login_to_ghcr_in_skopeo_container(org_name=ORG_NAME,
                                      username=USERNAME,
                                      password=PASSWORD,
                                      container_id=container_id)

    # Step 3a: Verify login in skopeo container
    check_login_in_skopeo_container(org_name=ORG_NAME,
                                    username=USERNAME,
                                    container_id=container_id)

    # Step 4: Get image tags
    image_tags = get_tags_of_image(org_name=ORG_NAME,
                                   image_name=REPO_TAG.split(":", 1)[0],
                                   container_id=container_id)

    # Step 5: Compare tags to current tag
    is_latest_tag = is_tag_latest(tag_list=image_tags,
                                  image_version=REPO_TAG.split(":", 1)[-1])

    # Step 6: Push latest tag
    if is_latest_tag:
        shasum_str = get_hex_digest(org_name=ORG_NAME,
                                    image_name=REPO_TAG.split(":", 1)[0],
                                    image_version=REPO_TAG.split(":", 1)[-1],
                                    container_id=container_id)

        push_latest(org_name=ORG_NAME,
                    image_name=REPO_TAG.split(":", 1)[0],
                    image_version=REPO_TAG.split(":", 1)[-1],
                    manifest_shasum=shasum_str,
                    container_id=container_id)

if __name__ == "__main__":
    main()