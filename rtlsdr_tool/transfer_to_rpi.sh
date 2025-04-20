#!/bin/bash
# Script to transfer the compiled binary to a Raspberry Pi

# Exit on error
set -e

# Default values
RPI_IP="raspberrypi.local"
RPI_USER="pi"
DEST_DIR="/home/pi"
BINARY_PATH="dist/rtlsdr-tool"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--host)
      RPI_IP="$2"
      shift 2
      ;;
    -u|--user)
      RPI_USER="$2"
      shift 2
      ;;
    -d|--dir)
      DEST_DIR="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [-h|--host hostname] [-u|--user username] [-d|--dir destination_directory]"
      exit 1
      ;;
  esac
done

# Check if binary exists
if [ ! -f "$BINARY_PATH" ]; then
    echo "Error: Binary not found at $BINARY_PATH"
    echo "Please run ./build_binary.sh first"
    exit 1
fi

# Transfer the binary
echo "Transferring rtlsdr-tool binary to $RPI_USER@$RPI_IP:$DEST_DIR/"
scp "$BINARY_PATH" "$RPI_USER@$RPI_IP:$DEST_DIR/"

# Make the binary executable on the Raspberry Pi
echo "Setting executable permissions..."
ssh "$RPI_USER@$RPI_IP" "chmod +x $DEST_DIR/rtlsdr-tool"

echo "Transfer complete!"
echo "To install system-wide on your Raspberry Pi, run:"
echo "  ssh $RPI_USER@$RPI_IP 'sudo mv $DEST_DIR/rtlsdr-tool /usr/local/bin/'"
echo ""
echo "To install udev rules for device permissions, copy rtl-sdr.rules to your Raspberry Pi:"
echo "  scp rtl-sdr.rules $RPI_USER@$RPI_IP:$DEST_DIR/"
echo "  ssh $RPI_USER@$RPI_IP 'sudo cp $DEST_DIR/rtl-sdr.rules /etc/udev/rules.d/ && sudo udevadm control --reload-rules && sudo udevadm trigger'" 