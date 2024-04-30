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

if __name__ == '__main__':
    from layout import Rect, Point, Size
    svg = canvas(Size(500, 500))
    rect(svg, Rect(Point(400, 100), Size(100, 300)), "yellow")
    circle(svg, Rect(Point(100, 400), Size(50, 50)), "pink")
    right_triangle(svg, Rect(Point(250, 250), Size(100, 100)), 0, 'purple')
    
    with open('shapes.svg', 'wb') as f:
        f.write(etree.tostring(etree.ElementTree(svg), encoding='utf-8', xml_declaration=True))
        print('saved')
