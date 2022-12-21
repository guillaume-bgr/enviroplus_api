#!/usr/bin/env python3

import time
import colorsys
import sys
import ST7735
import math
import bme680
try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

from bme280 import BME280
from pms5003 import PMS5003, ReadTimeoutError as pmsReadTimeoutError
from enviroplus import gas
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from fonts.ttf import RobotoMedium as UserFont
import logging

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("""all-in-one.py - Displays readings from all of Enviro plus' sensors
Press Ctrl+C to exit!
""")

# BME280 temperature/pressure/humidity sensor
bme280 = BME280()

# PMS5003 particulate sensor
# pms5003 = PMS5003()

# Create ST7735 LCD display class
st7735 = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)

# Initialize display
st7735.begin()

WIDTH = st7735.width
HEIGHT = st7735.height

# Set up canvas and font
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
font_size = 20
font = ImageFont.truetype(UserFont, font_size)

message = ""

# The position of the top bar
top_pos = 25

# Displays data and text on the 0.96" LCD
def display_text(variable, data, unit):
    # Maintain length of list
    values[variable] = values[variable][1:] + [data]
    # Scale the values for the variable between 0 and 1
    vmin = min(values[variable])
    vmax = max(values[variable])
    colours = [(v - vmin + 1) / (vmax - vmin + 1) for v in values[variable]]
    # Format the variable name and value
    message = "{}: {:.1f} {}".format(variable[:4], data, unit)
    logging.info(message)
    draw.rectangle((0, 0, WIDTH, HEIGHT), (255, 255, 255))
    for i in range(len(colours)):
        # Convert the values to colours from red to blue
        colour = (1.0 - colours[i]) * 0.6
        r, g, b = [int(x * 255.0) for x in colorsys.hsv_to_rgb(colour, 1.0, 1.0)]
        # Draw a 1-pixel wide rectangle of colour
        draw.rectangle((i, top_pos, i + 1, HEIGHT), (r, g, b))
        # Draw a line graph in black
        line_y = HEIGHT - (top_pos + (colours[i] * (HEIGHT - top_pos))) + top_pos
        draw.rectangle((i, line_y, i + 1, line_y + 1), (0, 0, 0))
    # Write the text at the top in black
    draw.text((0, 0), message, font=font, fill=(0, 0, 0))
    st7735.display(img)

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.read()
        temp = int(temp) / 1000.0
    return temp

values = {}

def get_stream_data():
    # Tuning factor for compensation. Decrease this number to adjust the
    # temperature down, and increase to adjust up
    factor = 2.25

    cpu_temps = [get_cpu_temperature()] * 5

    delay = 0.5  # Debounce the proximity tap
    mode = 0     # The starting mode
    last_page = 0
    light = 1

    # Create a values dict to store the data
    variables = ["temperature",
                "pressure",
                "humidity",
                "light",
                "oxidised",
                "reduced",
                "nh3",
                "pm1",
                "pm25",
                "pm10"]


    for v in variables:
        values[v] = [1] * WIDTH


    datas = 0
    # The main loop
    try:
        #while True:
            proximity = ltr559.get_proximity()

            # If the proximity crosses the threshold, toggle the mode
            if proximity > 1500 and time.time() - last_page > delay:
                mode += 1
                mode %= len(variables)
                last_page = time.time()
                
            if mode == 0:
            # One mode for each variable
                # variable = "temperature"
                unit_temp = "C"
                cpu_temp = get_cpu_temperature()
                # Smooth out with some averaging to decrease jitter
                cpu_temps = cpu_temps[1:] + [cpu_temp]
                avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
                raw_temp = bme280.get_temperature()
                data_temp = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
                display_text("temperature", data_temp, unit_temp)

                # variable = "pressure"
                unit_pres = "hPa"
                data_pres = bme280.get_pressure()
                display_text("pressure", data_pres, unit_pres)

                # variable = "humidity"
                unit_hum = "%"
                data_hum = bme280.get_humidity()
                display_text("humidity", data_hum, unit_hum)

                # variable = "light"
                unit_light = "Lux"
                if proximity < 10:
                    data_light = ltr559.get_lux()
                else:
                    data_light = 1
                display_text("light", data_light, unit_light)

                # variable = "oxidised"
                unit_oxi = "kO"
                data_oxi = gas.read_all()
                data_oxi = data_oxi.oxidising / 1000
                display_text("oxidised", data_oxi, unit_oxi)

                # variable = "reduced"
                unit_red = "kO"
                data_red = gas.read_all()
                data_red = data_red.reducing / 1000
                display_text("reduced", data_red, unit_red)

                # variable = "nh3"
                unit_nh3 = "kO"
                data_nh3 = gas.read_all()
                nh3_r0 = 750000
                data_nh3 = data_nh3.nh3 / 1000
                display_text("nh3", data_nh3, unit_nh3)
                
                datas = dict(temperature = data_temp, pressure = data_pres, humidity = data_hum, light = data_light, oxidised = data_oxi, reduced = data_red, nh3 = data_nh3)

            if mode == 7:
                # variable = "pm1"
                unit = "ug/m3"
                try:
                    data = pms5003.read()
                except pmsReadTimeoutError:
                    logging.warning("Failed to read PMS5003")
                else:
                    data = float(data.pm_ug_per_m3(1.0))
                    display_text(variables[mode], data, unit)

            if mode == 8:
                # variable = "pm25"
                unit = "ug/m3"
                try:
                    data = pms5003.read()
                except pmsReadTimeoutError:
                    logging.warning("Failed to read PMS5003")
                else:
                    data = float(data.pm_ug_per_m3(2.5))
                    display_text(variables[mode], data, unit)

            if mode == 9:
                # variable = "pm10"
                unit = "ug/m3"
                try:
                    data = pms5003.read()
                except pmsReadTimeoutError:
                    logging.warning("Failed to read PMS5003")
                else:
                    data = float(data.pm_ug_per_m3(10))
                    display_text(variables[mode], data, unit)
                    
            if datas : 
                return datas
        
    # Exit cleanly
    except KeyboardInterrupt:
        sys.exit(0)


