#!/usr/bin/env bash

set -euo pipefail

# Detect OS and architecture
echo "Detecting platform..."
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

case "$ARCH" in
    x86_64|amd64)
        ARCH=amd64
        ;;
    arm64|aarch64)
        ARCH=arm64
        ;;
    *)
        echo "Unsupported architecture: $ARCH"
        exit 1
        ;;
esac

# Set download URL for the latest release
echo "Fetching latest release info..."
LATEST_URL="https://api.github.com/repos/awslabs/amazon-s3-tar-tool/releases/latest"
RELEASE_JSON=$(curl -sSL "$LATEST_URL")

# Find the correct asset name and download URL
if [[ "$OS" == "darwin" ]]; then
    ASSET_NAME="s3tar-darwin-$ARCH.zip"
elif [[ "$OS" == "linux" ]]; then
    ASSET_NAME="s3tar-linux-$ARCH.zip"
else
    echo "Unsupported OS: $OS"
    exit 1
fi

ASSET_URL=$(echo "$RELEASE_JSON" | grep "browser_download_url" | grep "$ASSET_NAME" | cut -d '"' -f 4)
if [[ -z "$ASSET_URL" ]]; then
    echo "Could not find a release asset for $OS/$ARCH."
    exit 1
fi

echo "Downloading $ASSET_NAME..."
curl -L "$ASSET_URL" -o s3tar.zip
S3_TAR_PATH="${ASSET_NAME%.zip}"

# Unzip and install
unzip -o s3tar.zip
chmod +x "${S3_TAR_PATH}"

# Install location
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"
mv -f ${S3_TAR_PATH} "$INSTALL_DIR/s3tar"

# Clean up
rm -f s3tar.zip

echo "s3tar installed to $INSTALL_DIR/s3tar"
echo "Make sure $INSTALL_DIR is in your PATH."
echo "You can check with: echo \$PATH"
echo "To use s3tar, run: $INSTALL_DIR/s3tar --help"
