#!/bin/sh

set -e

OS=$(uname -s | tr "[:upper:]" "[:lower:]")
ARCH=$(uname -m)

if [ "$ARCH" = "aarch64" ];
then
  ARCH=arm64
fi

VERSION="v3.20.0"
GOOSE_URI="https://github.com/pressly/goose/releases/download/${VERSION}/goose_${OS}_${ARCH}"
GOOSE_BIN="/usr/local/bin/goose"

curl --silent --show-error --location --fail --location --output "${GOOSE_BIN}" "${GOOSE_URI}"

chmod +x "${GOOSE_BIN}"

echo "Goose was installed successfully"
