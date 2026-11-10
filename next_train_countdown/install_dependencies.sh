#!/usr/bin/env bash
set -euo pipefail

# Install system dependencies for the Pimoroni Unicorn HAT Mini on Ubuntu.
# Run with: bash install_dependencies.sh

sudo apt update
sudo apt install -y \
  python3 \
  python3-pip \
  python3-dev \
  i2c-tools \
  build-essential \
  git \
  curl

# Install the Unicorn HAT Mini Python library
pip3 install unicornhatmini

# Optional: enable I2C if it is not already enabled on the Raspberry Pi.
# On Ubuntu for Raspberry Pi this is usually already available.
# For Raspberry Pi OS use raspi-config -> Interface Options -> I2C.

echo "Dependencies installed."
