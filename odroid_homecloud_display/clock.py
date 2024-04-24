#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
An analog clockface with date & time.
"""

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106
from time import sleep
from PIL import ImageFont, ImageDraw, Image
import time
import datetime
import os

port = int(os.environ.get('HOMECLOUD_DISPLAY_PORT', "0"))
address = int(os.environ.get('HOMECLOUD_DISPLAY_ADDRESS', "0x3c"), 16)
rotate = int(os.environ.get('HOMECLOUD_DISPLAY_ROTATE', "2"))

serial = i2c(port=port, address=address)
device = ssd1306(serial, rotate=rotate)

font_name = "/usr/share/fonts/truetype/dseg/DSEG7Modern-Bold.ttf"
date_font = ImageFont.truetype(font_name, 20)
time_font = ImageFont.truetype(font_name, 36)

def main():
    while True:
        now = datetime.datetime.now()
        with canvas(device) as draw:
            draw.text((0, 0), now.strftime("%d %b %y"), font=date_font, fill=1)
            draw.text((0, 27), now.strftime("%H:%M"), font=time_font, fill=1)
        time.sleep(60 - now.second - now.microsecond / 1000000) # Display granularity is 1 minute.

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
