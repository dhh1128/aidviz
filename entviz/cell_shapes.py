from .layout import Cell
from .shapes import *

def edge_triangle(svg, cell: Cell, edge: int, fill_color: str):
    size = Size(cell.edge_width, cell.edge_height)
    inside = cell.edge_rect(edge)
    if edge in [3, 4]:
        where = Rect(cell.edge_rect)
    if rotation == 0:
        points = f"{where.top_left} {where.bottom_left} {where.bottom_right}"
    elif rotation == 90:
        points = f"{where.top_left} {where.top_right} {where.bottom_left}"
    elif rotation == 180:
        points = f"{where.top_left} {where.top_right} {where.bottom_right}"
    elif rotation == 270:
        points = f"{where.bottom_left} {where.top_right} {where.bottom_right}"
    else:

    points = f"{where.top_left} {where.bottom_left} {where.bottom_right}"
    return etree.SubElement(svg, 'polygon', points=points, fill=fill_color)

def edge_rect(svg: etree.Element, cell: Cell, edge: int, fill_color: str="brown"):
    return rect(svg, cell.edge_rect(edge), fill_color)

