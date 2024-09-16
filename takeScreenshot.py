from ppadb.client import Client as AdbClient
import os

# Create the ADB client connected to the default ADB server
client = AdbClient(host="127.0.0.1", port=5037)

# Get the list of devices
devices = client.devices()
#print(devices)

if len(devices) == 0:
    print("No devices connected")
    exit(1)

device = devices[0]  # Assume the first device is the target

# Send a tap command
#device.shell("input tap 437 1220")

# Use the screencap function to capture the screen
screenshot_data = device.screencap()

with open("screenshot.png", "wb") as f:
    f.write(screenshot_data)

print("Screenshot saved as screenshot.png in the current directory.")