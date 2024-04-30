import random
import string
import colorsys

def contrast_color(background_color):
    print(background_color)
    r, g, b = background_color
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if l < 0.5:
        return (255, 255, 255)  # White for dark backgrounds
    else:
        return (0, 0, 0)  # Black for light backgrounds

def generate_grid_svg(background_colors, border_styles):
    grid_width = 600
    grid_height = 400
    rows = 4
    cols = 3
    horizontal_spacing = 0.05 * grid_width / cols
    vertical_spacing = 0.05 * grid_height / rows
    box_width = (grid_width - (cols - 1) * horizontal_spacing) / cols  # width of each box
    box_height = (grid_height - (rows - 1) * vertical_spacing) / rows  # height of each box

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{grid_width}" height="{grid_height}">'''

    for row in range(rows):
        for col in range(cols):
            x = col * (box_width + horizontal_spacing)
            y = row * (box_height + vertical_spacing)
            text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(3, 4)))
            background_color = background_colors[row * cols + col] if row * cols + col < len(background_colors) else "white"
            foreground_color = contrast_color(background_color)
            border_style = border_styles[row * cols + col] if row * cols + col < len(border_styles) else "solid"
            font_size = min(box_width, box_height) * 0.25  # Adjust font size based on box size

            svg_content += f'''
            <g transform="translate({x}, {y})">
                <rect width="{box_width}" height="{box_height}" fill="{background_color}" />
                <text x="{box_width / 2}" y="{box_height / 2}" dominant-baseline="middle" text-anchor="middle" fill="{foreground_color}" font-size="{font_size}px">{text}</text>
            '''

            if border_style == "solid":
                svg_content += f'<rect x="1" y="1" width="{box_width - 2}" height="{box_height - 2}" fill="none" stroke="{foreground_color}" stroke-width="4"/>'
            elif border_style == "dashed":
                svg_content += f'<rect x="1" y="1" width="{box_width - 2}" height="{box_height - 2}" fill="none" stroke="{foreground_color}" stroke-width="4" stroke-dasharray="5,5"/>'
            elif border_style == "dotted":
                svg_content += f'<rect x="1" y="1" width="{box_width - 2}" height="{box_height - 2}" fill="none" stroke="{foreground_color}" stroke-width="4" stroke-dasharray="1,3"/>'
            elif border_style == "none":
                pass
            else:
                raise ValueError("Invalid border style")

            svg_content += '\n</g>'

    svg_content += '\n</svg>'
    return svg_content

import random

# Example usage:
background_colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(12)]
border_styles = ["solid", "dashed", "dotted", "none"] * 3

svg_code = generate_grid_svg(background_colors, border_styles)

with open("grid_output.svg", "w") as f:
    f.write(svg_code)
