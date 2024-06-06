#!/usr/bin/env python3

"""
Using the tomli-w library
Build an rclone configuration file based on the input arguments provided
"""

# Imports
import argparse
from pathlib import Path
import logging
import tomli_w
import subprocess

# Set logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_args():
    """
    Get args
    :return:
    """

    # Initialise parser
    parser = argparse.ArgumentParser()

    # Set output path
    parser.add_argument(
        "--config-output-path",
        type=str,
        required=True,
        dest="config_output_path",
        help="The output path for the configuration file, the parent directory must exist"
    )

    # Get src args
    src_arguments_parser = parser.add_argument_group(title="src credential options")
    src_arguments_parser.add_argument(
        "--src-access-key-id",
        type=str,
        required=True,
        dest="src_access_key_id",
        help="The AWS access key id for the source configuration"
    )
    src_arguments_parser.add_argument(
        "--src-secret-access-key",
        type=str,
        required=True,
        dest="src_secret_access_key",
        help="The AWS secret access key for the source configuration"
    )
    src_arguments_parser.add_argument(
        "--src-session-token",
        type=str,
        required=True,
        dest="src_session_token",
        help="The AWS session token for the source configuration"
    )
    src_arguments_parser.add_argument(
        "--src-region",
        type=str,
        required=True,
        dest="src_region",
        help="Source AWS Region"
    )

    # Get dest args
    dest_arguments_parser = parser.add_argument_group(title="dest credential options")
    dest_arguments_parser.add_argument(
        "--dest-access-key-id",
        type=str,
        required=True,
        dest="dest_access_key_id",
        help="The AWS access key id for the destination configuration"
    )
    dest_arguments_parser.add_argument(
        "--dest-secret-access-key",
        type=str,
        required=True,
        dest="dest_secret_access_key",
        help="The AWS secret access key for the destination configuration"
    )
    dest_arguments_parser.add_argument(
        "--dest-session-token",
        type=str,
        required=True,
        dest="dest_session_token",
        help="The AWS session token for the destination configuration"
    )
    dest_arguments_parser.add_argument(
        "--dest-region",
        type=str,
        required=True,
        dest="dest_region",
        help="The AWS Dest Region"
    )

    return parser.parse_args()


def check_args(args):
    # Check parent directory of the configuration file exists
    if not Path(args.config_output_path).parent.exists():
        logger.error(f"Parent of {Path(args.config_output_path)} does not exist, exiting")
        raise NotADirectoryError


def build_configuration_file(args):
    configuration_dict = {
        "src": {
            "type": "s3",
            "provider": "AWS",
            "access_key_id": args.src_access_key_id,
            "secret_access_key": args.src_secret_access_key,
            "session_token": args.src_session_token,
            "region": args.src_region
        },
        "dest": {
            "type": "s3",
            "provider": "AWS",
            "access_key_id": args.dest_access_key_id,
            "secret_access_key": args.dest_secret_access_key,
            "session_token": args.dest_session_token,
            "region": args.dest_region
        }
    }

    # Write configuration file
    with open(args.config_output_path, 'wb') as config_h:
        tomli_w.dump(configuration_dict, config_h)

    # Strip '"' from the configuration file
    subprocess.run(
        [
            "sed", "-i", 's/"//g', args.config_output_path
        ]
    )


def main():
    # Get args
    args = get_args()

    # Check args
    check_args(args)

    # Build Configuration file
    build_configuration_file(
        args
    )


if __name__ == "__main__":
    main()
