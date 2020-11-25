import sensor
import image
from pyb import USB_VCP
import pyb

# Specify communication method: "print" "usb" "can"
COMMS_METHOD = "usb"

# make USB_VCP object
# this lets us know if targets are being
# detected without having to print it and
# we can see if the target is aligned as well
usb = USB_VCP()
red = pyb.LED(1)
green = pyb.LED(2)
blue = pyb.LED(3)

FRAME_WIDTH = 320 # screen center (pixels) horizontal
FRAME_HEIGHT = 240 # screen center (pixels) vertical

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.RGB565
sensor.set_framesize(sensor.QVGA) # or sensor.QVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
clock = time.clock()

# LAB color space
thresholds = [(20, 100), (-128, -24), (-48, 51)] # green light


def findObject(img):
    blobs = img.find_blobs(thresholds, area_threshold = 10)

    areas = []

    for blob in blobs:
       areas.push(blob.area())

    biggest_blob = areas.index(max(areas)

    if ((biggest_blob.cx() < FRAME_WIDTH / 2 + 30 and biggest_blob.cx() > FRAME_WIDTH / 2 - 30) and
    (biggest_blob.cy() < FRAME_HEIGHT / 2 + 30 and biggest_blob.cy() > FRAME_HEIGHT / 2 - 30)):
        return true

    return false

while(True):
    img = sensor.snapshot()

    detection = findObject(img)

    if detection:
        green.on()
        red.off()
    else:
        red.on()
        green.off()

    if(COMMS_METHOD == "print"):
        print(detection)
    elif(COMMS_METHOD == "usb"): # sending the data via USB serial to the robot
        if detection:
            usb.send(1)
        else:
            usb.send(0)
