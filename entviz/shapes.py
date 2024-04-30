from lxml import etree

def circle(svg, where, fill_color: str="blue"):
    center = where.center
    return etree.SubElement(svg, 'circle', cx=f"{center.x}", cy=f"{center.y}", r=f"{where.size.width / 2}", fill=fill_color)

def rect(svg, where, fill_color):
    return etree.SubElement(svg, 'rect', x=f"{where.left}", y=f"{where.top}", width=f"{where.size.width}", height=f"{where.size.height}", fill=fill_color)

def canvas(size) -> etree.Element:
    return etree.Element('svg', width=f"{size.width}", height=f"{size.height}", xmlns="http://www.w3.org/2000/svg")

def right_triangle(svg, where, rotation: int, fill_color: str="red"):
    # Calculate coordinates of triangle vertices
    if rotation == 0:
        points = f"{where.top_left} {where.bottom_left} {where.bottom_right}"
    elif rotation == 90:
        points = f"{where.top_left} {where.top_right} {where.bottom_left}"
    elif rotation == 180:
        points = f"{where.top_left} {where.top_right} {where.bottom_right}"
    elif rotation == 270:
        points = f"{where.bottom_left} {where.top_right} {where.bottom_right}"
    else:
        raise ValueError("Rotation degree must be 0, 90, 180, or 270")
    return etree.SubElement(svg, 'polygon', points=points, fill=fill_color)
