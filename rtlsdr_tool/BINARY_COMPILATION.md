# Compiling RTL-SDR Tool as a Standalone Binary

This guide explains how to compile the RTL-SDR Tool into a standalone binary executable that can run on a Raspberry Pi without requiring Python to be installed.

## Prerequisites

On the build machine (Raspberry Pi or other computer):

- Python 3.6 or newer
- pip (Python package manager)
- git (optional, for cloning the repository)

For cross-compilation from macOS:
- Docker Desktop for Mac

## Method 1: Compiling Directly on Raspberry Pi

This is the simplest approach, as it ensures compatibility with your specific Raspberry Pi model.

1. Clone or copy the RTL-SDR Tool to your Raspberry Pi:
   ```bash
   git clone https://your-repository-url/rtlsdr_tool.git
   cd rtlsdr_tool
   ```

2. Make the build script executable:
   ```bash
   chmod +x build_binary.sh
   ```

3. Run the build script:
   ```bash
   ./build_binary.sh
   ```

4. The compiled binary will be available at `dist/rtlsdr-tool`

5. You can now copy this binary to any location and run it:
   ```bash
   cp dist/rtlsdr-tool /usr/local/bin/
   rtlsdr-tool -f 100.1e6
   ```

## Method 2: Cross-Compiling from macOS

The build script automatically detects macOS and uses Docker for cross-compilation:

1. Install Docker Desktop for Mac from https://www.docker.com/products/docker-desktop/

2. Clone the repository on your Mac:
   ```bash
   git clone https://your-repository-url/rtlsdr_tool.git
   cd rtlsdr_tool
   ```

3. Make the build script executable:
   ```bash
   chmod +x build_binary.sh
   ```

4. Run the build script:
   ```bash
   ./build_binary.sh
   ```

5. The script will:
   - Create a Dockerfile for the Raspberry Pi environment
   - Build a Docker image with all dependencies
   - Compile the binary inside the Docker container
   - Extract the binary to your local dist/ directory

6. Transfer the binary to your Raspberry Pi:
   ```bash
   scp dist/rtlsdr-tool pi@your-raspberry-pi:/home/pi/
   ```

7. On your Raspberry Pi, make the binary executable and move it to a location in your PATH:
   ```bash
   chmod +x rtlsdr-tool
   sudo mv rtlsdr-tool /usr/local/bin/
   ```

## Method 3: Cross-Compiling from Another Linux System

If you want to build the binary on a non-Raspberry Pi Linux system:

1. Set up a Raspberry Pi cross-compilation environment. Tools like `piwheels` or Docker containers with Raspberry Pi environments can help.

2. Install the dependencies:
   ```bash
   pip install pyinstaller numpy pyrtlsdr
   ```

3. Modify the spec file if needed for cross-compilation:
   - You may need to specify the target architecture in the spec file

4. Run PyInstaller manually:
   ```bash
   pyinstaller rtlsdr_tool.spec --clean
   ```

## Verifying the Binary

The standalone binary should run on any compatible Raspberry Pi without requiring Python or any Python libraries to be installed. The only requirements are the RTL-SDR hardware and drivers.

To test the binary:

```bash
./dist/rtlsdr-tool -f 100.1e6
```

## Troubleshooting

1. **Missing Libraries**: If you encounter errors about missing libraries, you might need to install them on the target system:
   ```bash
   sudo apt-get install libusb-1.0-0
   ```

2. **Permission Issues**: Make sure you have permissions to access the RTL-SDR device:
   ```bash
   sudo cp rtl-sdr.rules /etc/udev/rules.d/
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

3. **Binary Size**: If the binary is too large, make sure UPX is installed during the build process for better compression.

4. **Cross-Compilation Issues**: If you encounter issues with Docker cross-compilation:
   - Make sure Docker Desktop is running
   - Check that you have sufficient disk space
   - Try running Docker with increased memory allocation in Docker Desktop settings 