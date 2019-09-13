from canvas import *
import numpy as np

lower_points = [Point(.3, .2, "newunit"),
                Point(.02, .4, "absolute")]

def points_close(p1, p2):
    return np.isclose(p1.x, p2.x) and np.isclose(p1.y, p2.y)

vectors = []
points = []
axes = ["default", "figure", "newunit", "axis_ax1", "ax1", "absolute"]
for ax in axes:
    vectors.append(Vector(.3, .7, ax))
    vectors.append(Vector(-.2, -.9, ax)+Vector(.22, .1, "absolute"))
    vectors.append(Vector(0, .3, ax)+Vector(.01, -.01, "ax1")-Vector(1.1, 1.1, "default"))
    vectors.append((Point(.2, .3, ax) - Point(.5, .1, "newunit")))
    vectors.append((Point(.2, .3, ax) >> Point(1, 1, "absolute")) - Point(.5, .1, "newunit"))
    vectors.append((Point(.2, .3, ax) << Point(1, 1, "absolute")) - Point(.5, .1, "newunit"))
    vectors.append((Point(.2, .3, ax) | Point(1, 1, "absolute")) - Point(.5, .1, "newunit"))

for v in [(0, 0), (1, 0), (0, 1), (1.1, -1.3)]:
    vectors.append(Vector(*v, "figure"))
    vectors.append(Vector(*v, "absolute"))
    vectors.append(Vector(*v, "newunit"))
for v in [-.4, 0, 1]:
    vectors.append(Width(v, "default"))
    vectors.append(Height(v, "newunit"))

def test_width_height_objects():
    def make_vec(x,y,binop):
        if binop:
            return Vector(x,y,"a") + Vector(x, y, "b")
        else:
            return Vector(x, y)
    for binop in [True, False]:
        assert isinstance(make_vec(1, 0, binop), Width)
        assert isinstance(make_vec(0, 1, binop), Height)
        assert isinstance(make_vec(1, 0, binop), Vector)
        assert isinstance(make_vec(0, 1, binop), Vector)
        assert not isinstance(make_vec(0, 0, binop), Width)
        assert not isinstance(make_vec(0, 0, binop), Height)
        assert not isinstance(make_vec(1, 2, binop), Width)
        assert not isinstance(make_vec(1, 2, binop), Height)
    assert isinstance(Width(3), Vector)
    assert isinstance(Height(3), Vector)
    assert isinstance(Width(3, "a")+Width(2, "b"), Vector)
    assert isinstance(Height(3, "a")+Height(2, "b"), Vector)

def test_width_and_height_methods():
    c = Canvas(5, 5)
    c.add_unit("newunit", Width(.5, "figure") + Height(.6, "figure"), Point(.3, .3))
    c.add_axis("ax1", lower_points[0], Point(.9, .95))
    for v1 in vectors:
        h = c.convert_to_figure_coord(v1.height())
        w = c.convert_to_figure_length(v1.width())
        v = c.convert_to_figure_coord(v1)
        assert points_close(v, h+w)
        assert points_close(h, v.height())
        assert points_close(w, v.width())

def test_associative_vector_multiplication():
    for l in lower_points:
        c = Canvas(5, 5)
        c.add_unit("newunit", Width(.5, "figure") + Height(.6, "figure"), Point(.3, .3))
        c.add_axis("ax1", l, Point(.9, .95))
        for v1 in vectors:
            p1 = c.convert_to_figure_coord(2.1*(1.2*v1))
            p2 = c.convert_to_figure_coord((2.1*1.2)*v1)
            assert points_close(p1, p2), f"Failed for {p1} and {p2}"

def test_associative_vector_division():
    for l in lower_points:
        c = Canvas(5, 5)
        c.add_unit("newunit", Width(.5, "figure") + Height(.6, "figure"), Point(.3, .3))
        c.add_axis("ax1", l, Point(.9, .95))
        for v1 in vectors:
            p1 = c.convert_to_figure_coord(v1/1.2/2.1)
            p2 = c.convert_to_figure_coord(v1/(1.2*2.1))
            assert points_close(p1, p2), f"Failed for {p1} and {p2}"

def test_vector_identities():
    c = Canvas(5, 5)
    c.add_unit("newunit", Width(.5, "figure") + Height(.6, "figure"), Point(.3, .3))
    c.add_axis("ax1", Point(.4, .4), Point(.9, .95))
    for v in vectors:
        assert points_close(c.convert_to_figure_coord(v), c.convert_to_figure_coord(v+Vector(0,0))) # Additive identity
        assert points_close(Vector(0, 0), c.convert_to_figure_coord(v-v)) # Additive identity via subtraction
        assert points_close(c.convert_to_figure_coord(v), c.convert_to_figure_coord(v*1)) # Multiplicative identity
        assert points_close(c.convert_to_figure_coord(v), c.convert_to_figure_coord(v*1)) # Multiplicative identity


def test_linear_vector_multiplication():
    for l in lower_points:
        c = Canvas(5, 5)
        c.add_unit("newunit", Width(.5, "figure") + Height(.6, "figure"), Point(.3, .3))
        c.add_axis("ax1", l, Point(.9, .95))
        for v1 in vectors:
            p1 = 2.3*c.convert_to_figure_coord(v1)
            p2 = c.convert_to_figure_coord(2.3*v1)
            assert points_close(p1, p2), f"Failed for {v1}"

def test_linear_vector_division():
    for l in lower_points:
        c = Canvas(5, 5)
        c.add_unit("newunit", Width(.5, "figure") + Height(.6, "figure"), Point(.3, .3))
        c.add_axis("ax1", l, Point(.9, .95))
        for v1 in vectors:
            p1 = c.convert_to_figure_coord(v1)/2.3
            p2 = c.convert_to_figure_coord(v1/2.3)
            assert points_close(p1, p2), f"Failed for {v1}"

def test_associativity():
    c = Canvas(5, 5)
    c.add_unit("newunit", Width(.5, "figure") + Height(.6, "figure"), Point(.3, .3))
    c.add_axis("ax1", lower_points[0], Point(.9, .95))
    for v1 in vectors:
        for v2 in vectors:
            for p0 in [Point(.2, .2, "ax1"), Point(0, 2, "newunit")]:
                p1 = c.convert_to_figure_coord(p0 + (v1+v2))
                p2 = c.convert_to_figure_coord((p0 + v1) + v2)
                assert points_close(p1, p2), f"Failed for {p1} and {p2}"
                p1 = c.convert_to_figure_coord(v1 + (p0+v2))
                p2 = c.convert_to_figure_coord((v1 + p0) + v2)
                assert points_close(p1, p2), f"Failed for {p1} and {p2}"

def test_linear_vector_addition():
    for l in lower_points:
        c = Canvas(5, 5)
        c.add_unit("newunit", Width(.5, "figure") + Height(.6, "figure"), Point(.3, .3))
        c.add_axis("ax1", l, Point(.9, .95))
        for v1 in vectors:
            for v2 in vectors:
                p1 = c.convert_to_figure_coord(v1) + c.convert_to_figure_coord(v2)
                p2 = c.convert_to_figure_coord(v1+v2)
                assert points_close(p1, p2), f"Failed for {p1} and {p2}"


def test_commutative_vector_addition():
    for l in lower_points:
        c = Canvas(5, 5)
        c.add_unit("newunit", Width(.5, "figure") + Height(.6, "figure"), Point(.3, .3))
        c.add_axis("ax1", l, Point(.9, .95))
        for v1 in vectors:
            for v2 in vectors:
                p1 = c.convert_to_figure_coord(v1 + v2)
                p2 = c.convert_to_figure_coord(v2 + v1)
                assert points_close(p1, p2), f"Failed for {p1} and {p2}"

def test_commutative_vector_multiplication():
    for l in lower_points:
        c = Canvas(5, 5)
        c.add_unit("newunit", Width(.5, "figure") + Height(.6, "figure"), Point(.3, .3))
        c.add_axis("ax1", l, Point(.9, .95))
        for v1 in vectors:
            p1 = c.convert_to_figure_coord(v1*3)
            p2 = c.convert_to_figure_coord(3*v1)
            assert points_close(p1, p2), f"Failed for {p1} and {p2}"

def test_example_canvas():
    c = Canvas(4, 4, fontsize=9)
    c.add_axis("ax1", Point(.1, .1, "figure"), Point(.5, .5, "figure"))
    c.add_axis("ax2", Point(2.3, 2.3, "absolute"), Point(-.1, -.1, "-absolute"))
    c.ax("ax1").plot(np.linspace(0, 4, 100), np.sin(np.linspace(0, 4, 100)))
    c.ax("ax2").plot(np.linspace(0, 4, 5), np.linspace(0, 4, 5))
    # TODO

# TODO add (Point-Point) and (BinopPoint-BinopPoint) into test battery
# TODO add list of points to test
# TODO test |, >>, and <<
