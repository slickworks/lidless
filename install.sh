#!/bin/bash
set -euo pipefail

INSTALL_DIR=~/lidless
echo "Select installation directory (default: $INSTALL_DIR)"
read -p ">" input
INSTALL_DIR=${input:-$INSTALL_DIR}
echo $INSTALL_DIR

cd INSTALL_DIR
git clone git@github.com:slickworks/lidless.git src