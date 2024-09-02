#!/usr/bin/env bash

# Start the daemon
"${ICI_HOME}/ici-uploader" start-daemon 1>/dev/null 2>&1

# Run the ici-uploader command
"${ICI_HOME}/ici-uploader" "${@:1}"
