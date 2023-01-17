from PIL import Image, ImageDraw, ImageFont, ImageFilter
import ST7735
from fonts.ttf import RobotoMedium as UserFont

class Display:
    def __init__(self):
         # Create an LCD instance
        self.disp = ST7735.ST7735(
            port=0,
            cs=1,
            dc=9,
            backlight=12,
            rotation=270,
            spi_speed_hz=10000000
        )
         # Display setup
        self.delay = 0.5 # Debounce the proximity tap when choosing the data to be displayed
        self.mode = 0 # The starting mode for the data display
        self.last_page = 0
        self.light = 1
        # Width and height to calculate text position
        self.width = self.disp.width
        self.height = self.disp.height
        # The position of the top bar
        self.top_pos = 25
        # Set up canvas and fonts
        self.img = Image.new('RGB', (self.width, self.height), color=(0, 0, 0))
        self.draw = ImageDraw.Draw(self.img)
        self.x_offset = 2
        self.y_offset = 2
        # Set up fonts
        self.font_size_small = 10
        self.font_size_sm = 12
        self.font_size_smm = 14
        self.font_size_medium = 16
        self.font_size_ml = 18
        self.font_size_large = 20
        self.smallfont = ImageFont.truetype(UserFont, self.font_size_small)
        self.font_sm = ImageFont.truetype(UserFont, self.font_size_sm)
        self.font_smm = ImageFont.truetype(UserFont, self.font_size_smm)
        self.mediumfont = ImageFont.truetype(UserFont, self.font_size_medium)
        self.font_ml = ImageFont.truetype(UserFont, self.font_size_ml)
        self.largefont = ImageFont.truetype(UserFont, self.font_size_large)
        self.message = ""
        # Initialize display
        self.disp.begin()
       

        
    def display_startup(self, message):
        text_colour = (255, 255, 255)
        back_colour = (85, 15, 15)
        error_message = "{}".format(message)
        draw = ImageDraw.Draw(self.img)
        size_x, size_y = draw.textsize(message, self.mediumfont)
        x = (self.width - size_x) / 2
        y = (self.height / 2) - (size_y / 2)
        draw.rectangle((0, 0, 160, 80), back_colour)
        draw.text((x, y), error_message, font=self.mediumfont, fill=text_colour)
        self.disp.display(self.img)

    # Display Error Message on LCD
    def display_error(self, message):
        text_colour = (255, 255, 255)
        back_colour = (85, 15, 15)
        error_message = "System Error\n{}".format(message)
        draw = ImageDraw.Draw(self.img)
        size_x, size_y = draw.textsize(message, self.mediumfont)
        x = (self.width - size_x) / 2
        y = (self.height / 2) - (size_y / 2)
        draw.rectangle((0, 0, 160, 80), back_colour)
        draw.text((x, y), error_message, font=self.mediumfont, fill=text_colour)
        self.disp.display(self.img)
        
    def get_width(self):
        return self.width