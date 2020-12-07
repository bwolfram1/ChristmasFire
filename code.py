"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text. All drawing is done
using native displayio modules.

Pinouts are for the 2.4" TFT FeatherWing or Breakout with a Feather M4 or M0.
"""
import time
from random import randrange
import board
import terminalio
import displayio
from adafruit_display_text import label
import adafruit_imageload
from adafruit_bitmap_font import bitmap_font
import adafruit_ili9341
import gc
import neopixel


# Release any resources currently in use for the displays
displayio.release_displays()

spi = board.SPI()
tft_cs = board.D9
tft_dc = board.D10

display_bus = displayio.FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=board.D6
)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)

pixels = neopixel.NeoPixel(board.D11, 1)
pixels[0] = (0, 0, 0)

bitmap, palette = adafruit_imageload.load("/fireplace4bg.bmp",
                                         bitmap=displayio.Bitmap,
                                         palette=displayio.Palette)

sprite_sheet, palette2 = adafruit_imageload.load("/fire2.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)
palette2.make_transparent(0)
# Create a TileGrid to hold the bitmap
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette2,
                            width = 1,
                            height = 1,
                            tile_width = 25,
                            tile_height = 25)
# Create a Group to hold the TileGrid
text_group = displayio.Group(max_size=10, scale=2, x=15, y=40)
text = "Days until Christmas: 21"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
text_group.append(text_area)  # Subgroup for text scaling

group = displayio.Group()
group2 = displayio.Group(scale=2)

# Add the sprite to the Group
group2.append(sprite)
group2.x = 135
group2.y = 145
# Add the TileGrid to the Group
group.append(tile_grid)
group.append(group2)
group.append(text_group)

display.show(group)
print(gc.mem_free())

# Loop forever so you can enjoy your image
source_index = 0
while True:
    sprite[0] = source_index % 4
    source_index += 1
    time.sleep(0.1)