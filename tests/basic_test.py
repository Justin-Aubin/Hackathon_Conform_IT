from hackathon_conform_it.justinLib import is_intersection, merge_intersection

def test_is_intersection():
    # (x, y, w, h)
    box1 = (2, 2, 3, 3)

    box2 = (1, 1, 2, 2)
    box3 = (1, 3, 2, 1)
    box4 = (1, 4, 2, 2)
    box5 = (3, 1, 1, 2)
    box6 = (3, 3, 1, 1)
    box7 = (3, 4, 1, 2)
    box8 = (4, 1, 2, 2)
    box9 = (4, 3, 2, 1)
    box10 = (4, 4, 2, 2)

    box11 = (0, 0, 2, 2)
    box12 = (0, 3, 2, 1)
    box13 = (0, 5, 2, 2)
    box14 = (3, 0, 1, 2)
    box15 = (3, 3, 1, 1)
    box16 = (3, 5, 1, 2)
    box17 = (5, 0, 2, 2)
    box18 = (5, 3, 2, 1)
    box19 = (5, 5, 2, 2)

    assert is_intersection(box1, box2)
    assert is_intersection(box1, box3)
    assert is_intersection(box1, box4)
    assert is_intersection(box1, box5)
    assert is_intersection(box1, box6)
    assert is_intersection(box1, box7)
    assert is_intersection(box1, box8)
    assert is_intersection(box1, box9)
    assert is_intersection(box1, box10)

    assert not is_intersection(box1, box11)
    assert not is_intersection(box1, box12)
    assert not is_intersection(box1, box13)
    assert not is_intersection(box1, box14)
    assert is_intersection(box1, box15)
    assert not is_intersection(box1, box16)
    assert not is_intersection(box1, box17)
    assert not is_intersection(box1, box18)
    assert not is_intersection(box1, box19)

def test_merge_intersection():
    # (x, y, w, h)
    box2 = (1, 1, 2, 2)
    box6 = (3, 3, 1, 1)
    box10 = (4, 4, 2, 2)
    box11 = (0, 0, 2, 2)
    box1 = (2, 2, 3, 3)

    assert merge_intersection([box2, box6, box10, box11]) == [(0, 0, 3, 3), (3, 3, 1, 1), (4, 4, 2, 2)]
    assert merge_intersection([box2, box6, box10, box11, box1]) == [(0, 0, 6, 6)]
