import colorsys
import math

def rgb_to_hsv(rgb):
    r, g, b = rgb
    return colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

def hsv_to_rgb(hsv):
    h, s, v = hsv
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)

def adjust_luminosity(color, luminosity):
    h, s, v = color
    return h, s, luminosity

def complementary_color(rgb):
    hsv = rgb_to_hsv(rgb)
    h = (hsv[0] + 0.5) % 1.0
    luminosity = 1.0 - math.sqrt(hsv[2])  # Invert luminosity and increase contrast
    complementary_hsv = (h, hsv[1], hsv[2])
    adjusted_complementary_hsv = adjust_luminosity(complementary_hsv, luminosity)
    return hsv_to_rgb(adjusted_complementary_hsv)

# Example RGB value (background color)
background_color = (200, 200, 200)  # Gray

# Calculate complementary color
foreground_color = complementary_color(background_color)

print("Background Color (RGB):", background_color)
print("Foreground Color (RGB):", foreground_color)
