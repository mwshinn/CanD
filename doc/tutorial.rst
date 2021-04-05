Tutorial
========

Introduction
------------

The following tutorial will begin by describing the general paradigm of a CanD
canvas, followed by a description of some of the main components which can be
added to a canvas, and conclude with an annotated example.

The Canvas
----------

What is a canvas?
~~~~~~~~~~~~~~~~~

A canvas in CanD, given by the :class:`.Canvas` object, describes the physical
layout of the multi-paneled figure.  Primarily, it contains a set of axes, which
are normal matplotlib axes objects.  It also may contain other plot elements.
It can be thought of as a replacement for the matplotlib Figure object.

To start, we will want to import three core elements::

    from cand import Canvas, Point, Vector

These are, in general, the three elements you probably want to import.
:class:`.Canvas` can be used to create a new canvas, and :class:`.Point` and
:class:`.Vector` are used for measurements, which we will discuss soon. 

To create a canvas ``c`` which is 6 inches wide and 3 inches high, write::

    c = Canvas(6, 3, "inches")

Note that we specified the size of the canvas in inches.  There are many
possible units we can use, including:

- "in" (or "inch" or "inches"): Size in inches
- "cm" (or "centimeter", "centimetre", "centimeters", or "centimetres"):
  Size in centimeters.
- "mm" (or "millimeter", "millimetre", "millimeters", or "millimetres"):
  Position in millimeters.
- "pt" (or "point" or "points"): The distance in points.
- "px" (or "pixel" or "pixels"): The distance in pixels.  (Note that the
  relationship between pixels and the other units depends on the DPI at which
  the figure is exported, more on this later in the tutorial.)

Positions on the canvas
~~~~~~~~~~~~~~~~~~~~~~~

Once we have created a canvas of a given size, we can access positions on the
canvas using any units we would like.  Each of the units above can be used not
only to specify the size of the canvas, but also to specify a position on the
canvas.  Each of these assumes that the position (0,0) is at the bottom left of
the canvas.  We specify a point by specifying the x position, y position, and
unit as arguments to "Point", such as ``Point(3, 2, "cm")`` to access the point
three centimeters from the left and two centimeters from the bottom, or
``Point(0, 1, "in")`` to access the point on the left side of the figure, one inch
from the bottom.

In addition to the units above, each canvas defines a set of units
which may be used to position elements on that canvas.  These include:

- "absolute": The default position, measured in matplotlib's native coordinate
  system (currently inches).  The origin is the bottom left corner of the
  figure.  These coordinates are square, so one unit in the x direction is the
  same physical distance as one unit in the y direction.  This is the default
  unit.
- "-absolute": Identical to "absolute", except with the origin in the upper
  right corner.
- "figure": The fraction of the figure, where (0,0) is the bottom left corner
  and (1,1) is the upper right corner.  These coordinates may not be square,
  i.e., if the figure itself is not square, then a displacement in the x
  direction may be a different visual distance than a displacement in the y
  direction.
- "-figure": Indentical to "figure", except with the origin in the upper
  right corner.
- "default" (or none): The default unit.  This is set to "absolute" when the
  canvas is created, but this can be changed.  For example, ``Point(1, 2,
  "default")`` and ``Point(1, 2)`` are equivalent.

We can also use different units for the x coordinate than we use for the y
coordinate by specifying the unit as a tuple of the two units.  For example,
``Point(0.5, 1.5, ("in", "cm"))`` specifies the point 

That's a lot of units we can use to position elements on the canvas!  We will
see even more units introduced later in this tutorial.

Measuring distances
~~~~~~~~~~~~~~~~~~~

In addition to measuring positions on the canvas, we can measure distances.
Distances are measured using the :class:`.Vector` object.  Vectors are similar
to Points, except they do not have an origin.  Thus, they measure distances and
sizes of elements.  Vectors can use the same units as Points.  For example,
``Vector(1, 2, "in")`` measures 1 inch in the x direction, and two inches in the y
direction.

Vectors and points are distinct because they have different functions.  For
instance, as we will see in the next section, we can add a Vector and a Vector,
but we cannot add a Point and a Point in a meaningful way.  Thus, we have two
distinct objects: Points, specifying positions, and Vectors, specifying
distances or sizes.

Units can also be created from existing units.  Suppose we want to define a new
unit of "shifted_inches", which is the same asthe unit "inches" but with an
origin half a unit up and half a unit to the right.  For our canvas ``c``, we can
create this unit with::

    c.add_unit("shifted_inches", Vector(1, 1, "inches"), origin=Point(.5, .5, "inches"))

Likewise, if we want a unit "in_cm" with inches on the x axis and centimeters on
the y axis, but keeping the origin at the bottom left hand side of the canvas,
we can do::

    c.add_unit("in_cm", Vector(1, 1, ("inches", "cm")))

These new units can be used like existing units, e.g., ``Vector(1.5, 2.5,
"in_cm")``.

Vector and Point arithmetic
~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to perform arithmetic on vectors, similar to the way we perform
vector operations in linear algebra.  Two vectors can be added and subtracted,
and vectors can be multiplied and divided by a scalar.  For example, ``Vector(0,
1, "cm") + Vector(1, 1, "cm")`` is identical to ``Vector(1, 2, "cm")``, and
``2*Vector(1, .5, "in")`` is identical to ``Vector(2, 1, "in")``.

Likewise, it is possible to perform operations on vectors with different units.
For example, ``Vector(1, 0, "in") + Vector(1, 1, "cm")`` is identical to
``Vector(3.54, 1, "cm")``, which is approximately equal to ``Vector(1.3937, .3937,
"in")``. Likewise, ``Vector(1, 2, "cm") + Vector(.5, .5, "figure")`` is a valid
vector, but the size of the vector depends on the size of the canvas, since
``Vector(.5, .5, "figure")`` is defined as half of the size of the canvas.

There are several operations we can perform between vectors:

- "+": Vector addition, e.g., ``Vector(0, 1) + Vector(2, 0) == Vector(2, 1)``
- "-": Either the negative of a vector, e.g., ``-Vector(1, 2) == Vector(-1, -2)``,
  or vector subtraction, e.g., ``Vector(2, 2) - Vector(.5, 1) == Vector(1.5, 1)``
- "*": Multiply a vector by a scalar, e.g., ``2.5 * Vector(1, 2) == Vector(2.5, 5)``
- "/": Divide a vector by a scalar, e.g., ``Vector(4, 2)/2 == Vector(2, 1)``

There are also a few operations which are not standard linear algebra
operations.

- ">>": Take the x value of the first vector and the y value of the
  second vector, discarding the rest, e.g., ``Vector(1, 2) >> Vector(3, 4) ==
  Vector(1, 4)``
- "<<": Take the y value of the first vector and the x value of the second
  vector, discarding the rest, e.g., ``Vector(1, 2) << Vector(3, 4) ==
  Vector(3, 2)``
- "@": Rotate the vector by a given number of degrees.  Note that the rotation
  is always performed in square coordinates, so a 45 degree rotation will always
  appear to be a 45 degree rotation.  In other words, the vector will first be
  converted to "absolute" units and then rotated.  In square coordinates, this
  does not make a difference, so for example, ``Vector(0, 1, "in") @ 45 ==
  Vector(1/sqrt(2), 1/sqrt(2), "in")``

We can also perform operations between Points and Vectors.  For example, if we
want a point at the center of the figure but shifted up by 1 cm, we can do
``Point(.5, .5, "figure") + Vector(0, 1, "cm")``.

Operations defined between Points and Vectors are:

- "+": Shift a point by an amount given by a vector, e.g., ``Point(1, 2) +
  Vector(2, 3) == Point(3, 5)``.
- "-": Shift a point by the inverse of a vector, e.g., ``Point(5, 5) -
  Vector(1, 2) == Point(4, 3)``.

There are also operations defined between two Points:

- "-": Find the vector which connects the second point to the first point, e.g.,
  ``Point(4, 3) - Point(1, 2) == Vector(3, 1)``.
- ">>": Take the x value of the first point and the y value of the
  second point, discarding the rest, e.g., ``Point(1, 2) >> Point(3, 4) ==
  Point(1, 4)``
- "<<": Take the y value of the first vector and the x value of the second
  vector, discarding the rest, e.g., ``Point(1, 2) << Point(3, 4) ==
  Point(3, 2)``
- "|": Find the point in the middle of the two given points, e.g., ``Point(1, 1)
  | Point(2, 3) == Point(1.5, 2)``.

Creating an axis
~~~~~~~~~~~~~~~~

TODO

Adding geometric shapes
~~~~~~~~~~~~~~~~~~~~~~~

add_box, add_ellipse, add_arrow, add_poly, add_line, add_marker, add_rect, 

Adding images
~~~~~~~~~~~~~

Adding text
~~~~~~~~~~~

Adding plot elements
~~~~~~~~~~~~~~~~~~~~

add_legend, add_colorbar, add_figure_labels

Adding grids of axes
~~~~~~~~~~~~~~~~~~~~

Saving
~~~~~~

