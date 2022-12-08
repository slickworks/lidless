#!/bin/bash

# Safety checks that all bash scripts should start with.
set -euo pipefail

# Set PYTHON to the LIDLESS_PYTHON env var or default to python3.
PYTHON=${LIDLESS_PYTHON:=python3}

# Print message and exit if chosen python is older than 3.7, or not found at all.
if ! $PYTHON -c 'import sys; assert sys.version_info >= (3,6)' &> /dev/null; then
  echo ""
  echo " ----------------------------------ERROR----------------------------------"
  echo ""
  echo " Lidless requires Python 3.7 or above."
  echo ""
  echo " Install a compatible version and point env var LIDLESS_PYTHON to it, e.g."
  echo ""
  echo "    export LIDLESS_PYTHON=/home/me/.pyenv/versions/3.10.4/bin/python"
  echo ""
  echo " PS: I recommend using pyenv to manage multiple Python installations."
  echo ""
  exit 1
fi

# Get path to this script directory, which is also the lidless module.
THIS_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Set PYTHONPATH to THIS_DIR and run the a module.
PYTHONPATH=$THIS_DIR $PYTHON -m lidless $*
