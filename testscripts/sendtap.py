from ppadb.client import Client as AdbClient
import os

# Create the ADB client connected to the default ADB server
client = AdbClient(host="127.0.0.1", port=5037)

# Get the list of devices
devices = client.devices()
if len(devices) == 0:
    print("No devices connected")
    exit(1)

device = devices[1]  # Assume the first device is the target

# Send a tap command
device.shell("input swipe 800 250 100 250")

