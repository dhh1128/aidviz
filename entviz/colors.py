def relative_luminance(rgb):
    """
    Calculate the gamma-corrected luminance of an RGB color value. This is the luminance value
    used for accessibility purposes in web design, to ensure that text is readable against a
    background color. The luminance value is a number between 0 and 1, where 0 is black and 1 is
    white. See https://www.w3.org/WAI/GL/wiki/Relative_luminance.
    
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
        if c <= 0.04045:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4

    rs_gamma = gamma_correction(rs)
    gs_gamma = gamma_correction(gs)
    bs_gamma = gamma_correction(bs)

    Y = (0.2126 * rs_gamma) + (0.7152 * gs_gamma) + (0.0722 * bs_gamma)
    return Y
