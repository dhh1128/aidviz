from ..layout import *

def test_Rect():
    br = Rect(Point(10, 20), Size(30, 40))
    assert br.top_left == Point(10, 20)
    assert br.size == Size(30, 40)
    assert br.bottom_right == Point(40, 60)
    assert br.top_right == Point(40, 20)
    assert br.bottom_left == Point(10, 60)
    assert br.left == 10
    assert br.top == 20
    assert br.right == 40
    assert br.bottom == 60
    assert br.center == Point(25, 40)

def test_Cell():
    cell = Cell(Point(0, 0), Size(64, 32))
    assert cell.edge_height == 8
    assert cell.edge_width == 8
    e0134 = cell.edge_0134_size
    assert e0134 == Size(24, 8)
    e25 = cell.edge_25_size
    assert e25 == Size(8, 16)
    assert cell.nucleus == Rect(Point(8, 8), Size(48, 16))
    assert cell.edge_rect(0) == Rect(Point(8, 0), e0134)
    assert cell.edge_rect(1) == Rect(Point(32, 0), e0134)
    assert cell.edge_rect(2) == Rect(Point(56, 8), e25)
    assert cell.edge_rect(3) == Rect(Point(32, 24), e0134)
    assert cell.edge_rect(4) == Rect(Point(8, 24), e0134)
    assert cell.edge_rect(5) == Rect(Point(0, 8), e25)

