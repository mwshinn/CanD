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

for ax in axes:
    points.append(Point(.3, .2, ax))
    points.append(Point(0, 0, ax))
    points.append(Point(0, 1, ax))
    points.append(Point(100, 0, ax))
    points.append(Point(.1, -.2, ax) + Vector(1, 1, "absolute"))
    points.append(Point(.1, -.2, ax) - Vector(1, 1, "absolute"))
    points.append(Point(1, 1, ax) >> Point(.3, .1, "absolute"))
    points.append(Point(1, 1, ax) << Point(.3, .1, "figure"))
    points.append(Point(1, 1, ax) | Point(.3, .1, "figure"))
    points.append(Point(.1, -.2, "figure") + (Point(1.1, 2.1, ax) - Point(.3, .6, "absolute"))/2)
    
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

def test_point_indentities():
    c = Canvas(5,5)
    c.add_unit("newunit", Width(.5, "figure") + Height(.6, "figure"), Point(.3, .3))
    c.add_axis("ax1", Point(.4, .4), Point(.9, .95))
    for p in points:
        assert points_close(c.convert_to_figure_coord(p+Vector(0,0,"ax1")), c.convert_to_figure_coord(p)+c.convert_to_figure_length(Vector(0,0,"ax1")))

def test_point_meet_right():
    c = Canvas(5,5)
    c.add_unit("newunit", Width(.5, "figure") + Height(.6, "figure"), Point(.3, .3))
    c.add_axis("ax1", Point(.4, .4), Point(.9, .95))
    for p1 in points:
        for p2 in points:
            assert points_close(c.convert_to_figure_coord(p1) >> c.convert_to_figure_coord(p2), c.convert_to_figure_coord(p1 >> p2))

def test_point_meet_left():
    c = Canvas(5,5)
    c.add_unit("newunit", Width(.5, "figure") + Height(.6, "figure"), Point(.3, .3))
    c.add_axis("ax1", Point(.4, .4), Point(.9, .95))
    for p1 in points:
        for p2 in points:
            assert points_close(c.convert_to_figure_coord(p1) << c.convert_to_figure_coord(p2), c.convert_to_figure_coord(p1 << p2))
            
def test_point_mean():
    c = Canvas(5,5)
    c.add_unit("newunit", Width(.5, "figure") + Height(.6, "figure"), Point(.3, .3))
    c.add_axis("ax1", Point(.4, .4), Point(.9, .95))
    for p1 in points:
        for p2 in points:
            assert points_close(c.convert_to_figure_coord(p1) | c.convert_to_figure_coord(p2), c.convert_to_figure_coord(p1 | p2))

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



