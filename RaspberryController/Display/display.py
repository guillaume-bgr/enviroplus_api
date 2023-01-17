import ST7735
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium as UserFont
import logging

class LCD :
    def __init__(self):
        logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
        self.disp = ST7735.ST7735(
            port=0,
            cs=1,
            dc=9,
            backlight=12,
            rotation=270,
            spi_speed_hz=10000000
        )
                # Initialize display.
        self.disp.begin()

        # Width and height to calculate text position.
        self.width = self.disp.width
        self.height = self.disp.height
        # New canvas to draw on.
        self.img = Image.new('RGB', (self.width, self.height), color=(0, 0, 0))
        self.draw = ImageDraw.Draw(self.img)


    def displayText(self, fontSize, textColor, backColor, text):

        # Text settings.
        font = ImageFont.truetype(UserFont, fontSize)

        message = text
        size_x, size_y = self.draw.textsize(message, font)

        # Calculate text position
        x = (self.width - size_x) / 2
        y = (self.height / 2) - (size_y / 2)

        # Draw background rectangle and write text.
        self.draw.rectangle((0, 0, 160, 80), backColor)
        self.draw.text((x, y), message, font=font, fill=textColor)
        self.disp.display(self.img)
        
    def stopLCD(self):
        self.disp.set_backlight(0)
