def luminance(rgb):
    """
    Calculate the gamma-corrected luminance of an RGB color value.
    
    The simple method of getting luminance is just to assume that however much red, green, and blue
    we see, that's how much luminance we have. This does not account for the fact that the human eye
    perceives a fixed quantity of green light to be more luminous than that same quantity of red light
    (and red to be more luminous than blue), because of the sensitivity of the rods and cones in the
    eye to different light frequencies.
    
    This method fixes that problem and gives a more realistic idea of what the perceived luminance of
    a color is, for a typical human eye. 
    """
    rs = rgb[0] / 255
    gs = rgb[1] / 255
    bs = rgb[2] / 255

    def gamma_correction(c):
        if c <= 0.03928:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4

    rs_gamma = gamma_correction(rs)
    gs_gamma = gamma_correction(gs)
    bs_gamma = gamma_correction(bs)

    L = (0.2126 * rs_gamma) + (0.7152 * gs_gamma) + (0.0722 * bs_gamma)
    return L

# Example usage:
rgb_color = (128, 200, 50)  # Example RGB color, change it to your desired color
luminance_value = luminance(rgb_color)
print("Relative luminance:", luminance_value)