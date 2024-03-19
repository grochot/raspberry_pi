import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from gpiozero import Button

import json
import select
import time 

from sensors import *

# udp client (sender) configuration
# set destination IP and port -> your PC

# udp clinet (listener) configuration
# set own IP to bind -> Raspberry Pi
UDP_IP_SELF = "169.254.133.53"
UDP_PORT_SELF = 8803

# sock = socket.socket(socket.AF_INET, # Internet
#                      socket.SOCK_DGRAM) # UDP

sock_in = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock_in.bind((UDP_IP_SELF, UDP_PORT_SELF))

# preapre buttons
button = []
button.append(Button(6))
button.append(Button(13))
button.append(Button(19))
button.append(Button(26))

# display initialization
disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# clear working buffer of the display
draw.rectangle((0,0,width,height), outline=0, fill=0)

# print some text to working buffer
x = 0
top = -2
draw.text((x, top),       "  Technika Sensorowa",  font=font, fill=255)
draw.text((x, top+8),     "      Magnetometr",  font=font, fill=255)
draw.text((x, top+16),    "	2023",  font=font, fill=255)
draw.text((x, top+25),    "Stop",  font=font, fill=255)

# update the display
disp.image(image)
disp.display()


sensor = sensors()

while True:
    # terminate if button 0 pressed
    if button[0].is_pressed:
        break
    # when recieve any packet - measure and send data to PC
    ready = select.select([sock_in], [], [], 0.1)
    if ready[0]:
        message, address = sock_in.recvfrom(1024)
        print("GET DATA REQUEST", message.decode())
        mag = sensor.read_mag_raw()
        data = json.dumps(mag)
        sock_in.sendto(bytes(data, "utf-8"), address)
        time.sleep(0.1)

# display termination info
draw.rectangle((0,0,width,height), outline=0, fill=0)
draw.text((x, top),       "  Technika Sensorowa",  font=font, fill=255)
draw.text((x, top+8),     "      Magnetometr",  font=font, fill=255)
draw.text((x, top+16),    "	2023",  font=font, fill=255)
draw.text((x, top+25),    "Terminated...",  font=font, fill=255)
disp.image(image)
disp.display()

