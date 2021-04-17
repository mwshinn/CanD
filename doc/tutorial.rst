Tutorial
========

Introduction
------------

The following tutorial will begin by describing the general paradigm of a CanD
canvas, followed by a description of some of the main components which can be
added to a canvas, and conclude with an annotated example.

The Canvas
----------

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

Once we have created the canvas, we can view it using any of the following three
commands::

    c.show() # Show a new window containing the canvas
    c.show_jupyter() # Display the canvas inline in a jupyter notebook
    c.save("output.png") # Save the canvas to the file "output.png"
    c.save("output.pdf") # Save the canvas to the file "output.pdf"

This is all great, but there is nothing useful about seeing an empty canvas.
Let's look at how to position plots and other elements on the canvas.

Positions on the canvas
-----------------------

Once we have created a canvas of a size we are satisfied with, we can access
positions on the canvas using any units we would like.  Each of the units above
can be used not only to specify the size of the canvas, but also to specify a
position on the canvas.  Each of these assumes that the position (0,0) is at the
bottom left of the canvas.  We specify a point by specifying the x position, y
position, and unit as arguments to "Point", such as ``Point(3, 2, "cm")`` to
access the point three centimeters from the left and two centimeters from the
bottom, or ``Point(0, 1, "in")`` to access the point on the left side of the
figure, one inch from the bottom.

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
-------------------

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

Vector/Point arithmetic
---------------------------

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

While all of these operators may seem daunting at first, as you gain experience
using CanD, you will begin to find them more intuitive.

Creating an axis
----------------

Now that we have learned how to describe positions and distances on the canvas,
let's learn how to plot.  In order to plot, we must first create an axis.  Any
given Canvas may have multiple axes.  `Axes
<https://matplotlib.org/stable/api/axes_api.html#matplotlib.axes.Axes>`_ are
Matplotlib objects, and so to plot on them, you can use all standard Matplotlib
commands.  Note that you will need to use the so-called `"object-oriented API"
<https://matplotlib.org/stable/api/index.html#the-object-oriented-api>`_ in
Matplotlib.  If you are used to using the so-called `"Pyplot API"
<https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.html#module-matplotlib.pyplot>`_
(i.e., Matlab-style plt.[something] commands), you should find this intuitive,
and most of the commands have similar names.  (One place you may have seen `Axis
<https://matplotlib.org/stable/api/axes_api.html#matplotlib.axes.Axes>`_ objects
before is in the result of "`plt.gca()
<https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.gca.html>`_".)

To create an axis, we use :meth:`.Canvas.add_axis`.  We must specify the name of
the axis (a unique identifier we will use to access that axis subsequently), the
lower left corner of the axis, and the upper right corner of the axis.  For
example, to create an axis on Canvas ``c`` named "myaxis" with lower left corner
an inch from the bottom left, and 1 inch high and one inch wide::

    ax = c.add_axis("myaxis", Point(1, 1, "in"), Point(2, 2, "in"))

Now, ``ax`` will be the axis object, and the canvas will have an empty axis on
it.  To see this, run any of the visualization routines listed above, such as::

    c.show()

Since ``ax`` is a `Matplotlib axis object
<https://matplotlib.org/stable/api/axes_api.html#matplotlib.axes.Axes>`_, we can
plot to it the same way we would normally do in Matplotlib.  For example, we can
add a scatterplot::

    ax.scatter(np.random.rand(10), np.random.rand(10))
    c.show()

We can also access axis objects after we make them.  For axis "myaxis", use
``c.ax("myaxis")`` to access the axis.  A common paradigm in CanD is to declare
axes at the beginning, and then use them later.  For instance::

    c = Canvas(5, 5, "in")
    c.add_axis("myaxis1", Point(1, 1, "in"), Point(2, 2, "in"))
    c.add_axis("myaxis2", Point(3, 1, "in"), Point(4, 4, "in"))
    c.add_axis("myaxis3", Point(1, 3, "in"), Point(2, 4, "in"))
    [...]
    ax = c.ax("myaxis1")
    [...]
    ax = c.ax("myaxis1")
    [...]
    ax = c.ax("myaxis1")
    [...]

It is also possible to use this function to call axes directly.  For instance::

    c = Canvas(5, 5, "in")
    c.add_axis("myaxis1", Point(1, 1, "in"), Point(2, 2, "in"))
    c.ax("myaxis1").plot([1, 2, 3], [1, 2, 3])

Units are automatically created to go along with any new axis we create.  In
particular, two units are created.  If the axis is named "myaxis", then the two
units are

- Name identical to the axis name (in this case, "myaxis"): These are the data
  coordinates of the axis.  If we plot the point (123, 456) on the axis (e.g.,
  in a scatter plot), then this point will respond to wherever that point
  happens to be, adjusting for the x- and y-axis limits.  Note that this uses
  the position where the data coordinate is located at the time the unit is
  used, rather than the time when the plot is displayed.
- The axis name prepended with "axis_" (in this case, "axis_myaxis"): These
  coordinates are relative to the location of the axis.  The origin (0,0) is
  located at the bottom left corner of the axis, and the point (1,1) is located
  at the upper right corner of the axis.

These units can be used in exactly the same way as above.  We will see an
example of this below.

Text
----

In its simplest form, we can add text using the command
:meth:`.Canvas.add_text`.  The first argument is the text we would like to show,
followed by the position of the text.  We may optionally specify alignment
through the optional ``ha`` or ``horizontalalignment`` and ``va`` or
``verticalalignment`` arguments.  The ``size`` argument specifies font size,
``style`` can be set to ``italic``, and ``weight`` can be set to ``bold``.  Math
and unicode can be used as normal.  For example::

    c = Canvas(3, 3, "in")
    c.set_default_unit("figure")
    c.add_text("Center", Point(.5, .5))
    c.add_text("Bottom left", Point(0, 0), ha="left", va="bottom", style="italic")
    c.add_text("Upper right", Point(1, 1), size=20, ha="right", va="top", weight="bold", style="italic")
    c.add_text(r"$\int_0^{10} x^\alpha$", Point(.25, .75))
    c.add_text("Юникод", Point(.75, .25), weight="bold")

Changing the font
-----------------

CanD has implemented a system (called "Fontant") for selecting fonts which
improves upon Matplotlib's.  In Matplotlib, fonts are selected with a "best
guess" at what you meant.  It can sometimes be difficult to choose between
similar versions of the same font, or to find the correct name for the font you
would like to use.  Additionally, if there is a slight difference in the name
you specified vs the actual name of the font (e.g., if you specified "Helvetica"
instead of "Helvetica Std"), Matplotlib will fall back to the default font.
Additionally, Matplotlib is inequipped to deal with fonts with different
varieties.  For example, sometimes it will randomly substitute stylistic
alternatives of fonts you have selected, when multiple fonts match.

CanD improves upon this system in two ways.  First, CanD is better able to guess
what you meant than Matplotlib.  It uses a more sophisticated algorithm for
guessing the font name and the default version of the font.  Second, if there is
ever any ambiguity in the font selection, CanD will throw an error and ask you
to be more specific.  Additionally, CanD's font management system will
synchronize fonts across the document, including math fonts.  In summary, CanD's
font management is unlikely to make surprising font choices.

We can specify this to :meth:`.Canvas.add_text` using the ``font`` argument.
Then, we disambiguate the font with further arguments.  For example, if you run
the following::

    c = Canvas(3, 3, "in")
    c.add_text("Hello", Point(.5, .5, "figure"), font="Lucida")

you may receive the following error::

    cand.fontant.MultipleFontsFoundError: Please be more specific in specifying font family.
    Specify one of the following font names:
        "Lucida Bright", "Lucida Calligraphy", "Lucida Console", "Lucida Fax", "Lucida Handwriting", "Lucida Math Std", "Lucida Sans Std", "Lucida Sans Typewriter", "Lucida Sans Typewriter Std", "Lucida Sans Unicode", "Lucida Std", "Lucida Typewriter Std"

Since there are multiple fonts which include the name "Lucida", but none is a
perfect match, we need to specify which one we want.  We can fix this by
specifying which font we want, changing the code to::

    c.add_text("Hello", Point(.5, .5, "figure"), font="Lucida Console")

Sometimes, there may be multiple versions of a font.  For instance, suppose we
try to use `Inconsolata <https://en.wikipedia.org/wiki/Inconsolata>`_::

    c.add_text("Hello", Point(.2, .2, "figure"), font="Inconsolata")

This gives the following error::

    cand.fontant.MultipleFontsFoundError: Please specify a stretch using the function argument stretch=[value].  Valid values for this font are:
        "expanded", "ultracondensed", "ultraexpanded", "condensed", "semiexpanded", "extraexpanded", "extracondensed", "normal", "semicondensed"

Thus, we need to choose a stretch value for this font from the list.  Specifying
the stretch fixes the problem::

    c.add_text("Hello", Point(.2, .2, "figure"), font="Inconsolata", stretch="condensed")

Additionally, some fonts may offer additional features beyond the default.  For
instance, `Raleway <https://www.theleagueofmoveabletype.com/raleway>`_ provides
more weights beyond "bold"::

    c = Canvas(2, 3, "in")
    for i,weight in enumerate(["thin", "extralight", "light",
                               "regular", "medium", "semibold",
                               "bold", "extrabold", "black"]):
        c.add_text(weight, Point(1, 2.5-i/4, "in"), weight=weight, font="Raleway", style="normal")
        

To make sure fonts are consistent across the document, including axis tick
labels, we can use the :meth:`.Canvas.set_font` function.  This also allows the
``ticksize`` argument for setting the size of tick labels.  For example, to set
the entire figure to be Helvetica with 6pt font and 5pt font for axis tick
labels, use one of the following, depending on which version of Helvetica you
have installed::

    c.set_font("Nimbus Sans", size=6, ticksize=5)
    c.set_font("Helvetica", size=6, ticksize=5)
    c.set_font("Helvetica", stretch="normal", size=6, ticksize=5)

To add together everything we've learned so far about text and fonts, let's
create a labeled scatterplot showing the number of fingers vs the number of
heart chambers across animals::

    from cand import Canvas, Point, Vector
    import seaborn as sns
    import pandas
    # Use a 4in x 4in canvas
    c = Canvas(4, 4, "in")
    # Use "Lucida Handwriting" as the default font for the entire plot.
    c.set_font("Lucida Hand", size=14)
    # We will only use one axis in this figure.
    ax = c.add_axis("fin_v_cham", Point(.2, .2), Point(.7, .9))
    # padding is the offset from text to figure label
    padding = Vector(.2, .1, "cm")
    # Let's use these example data
    df = pandas.DataFrame({"fing": [5, 1, 4, 0, 0],
                           "cham": [4, 4, 3, 3, 2],
                           "anim": ["human", "horse", "frog", "snake", "fish"]})
    ax.scatter(df["cham"], df["fing"], c='k', marker='x')
    # For each of our animals, show the animal's name next to the data point
    for row in df.iterrows():
        c.add_text(row[1]['anim'], Point(row[1]['cham'], row[1]['fing'], "fin_v_cham")+padding, ha="left")

    # Finish off the plot and display
    ax.set_ylabel("# fingers")
    ax.set_xlabel("# chambers in heart")
    sns.despine(ax=ax)
    c.show()


Geometric shapes
----------------

Geometric shapes can be added to any plot by specifying them with Points and
Vectors.  These are similar to `several functions built into matplotlib
<https://matplotlib.org/stable/api/patches_api.html>`_, but the matplotlib
functions do not support specifying positions using Points and Vectors.

Points and lines
................

A point or marker, similar to one that would be drawn in a Matplotlib
scatterplot, can be added with :meth:`.Canvas.add_marker`.  The first argument
is the position, and the remaining arguments are identical to those of `Lines2D
<https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D>`_.

Likewise, a line can be drawn with :meth:`.Canvas.add_line`.  The first two
arguments are Points specifying the endpoints of the line, and the remaining
arguments are identical to those of `Lines2D
<https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D>`_.

For example::

    c = Canvas(2, 2, "in")
    c.add_marker(Point(.5, .25), marker="*", markersize=12, color='g')
    c.add_marker(Point(.5, .75), marker="o", markersize=12)
    c.add_line(Point(0, .5), Point(1, .5), linewidth=3, color="r")

Note that these are not intended replace normal matplotlib plotting functions.
When plotting on axes, it is usually more convenient to use the standard
matplotlib "plot" and "scatter" functions.

Polygons
........

Rectangles can be specified using the :meth:`.Canvas.add_rect` function by
providing two Points as corners, the lower left and the upper right.  All subsequent
arguments are identical to those for `matplotlib.patches.Polygon
<https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Polygon.html#matplotlib-patches-polygon>`_

Polygons in general can be drawn with :meth:`.Canvas.add_polygon`, where the
first argument is a list of Points which serve as the vertices of the polygon.
All subsequent arguments are identical to those for `matplotlib.patches.Polygon
<https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Polygon.html#matplotlib-patches-polygon>`_
Notably, if you would like to draw an open polygon, use the "closed" argument.

It is also possible to draw "`fancy boxes
<https://matplotlib.org/stable/gallery/shapes_and_collections/fancybox_demo.html#sphx-glr-gallery-shapes-and-collections-fancybox-demo-py>`_",
such as those with rounded corners, jagged edges, or shapes which look like
giant arrows.  These utilize the :meth:`.Canvas.add_polygon` function.  The
first to arguments are Points, specifying the lower left and upper right
corners.  All subsequent arguments are passed to
`matplotlib.patches.FancyBboxPatch
<https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.FancyBboxPatch.html#matplotlib.patches.FancyBboxPatch>`_.

For example::

    c = Canvas(4,3,"in")
    c.add_rect(Point(.2, .7, "in"), Point(3.8, .9, "in"), color='k')
    c.add_box(Point(.2, .2, "in"), Point(3.8, .4, "in"), color='k', boxstyle='round')
    c.add_box(Point(.5, 1.8, "in"), Point(1.5, 2.2, "in"), boxstyle="rarrow", fill=True, color=(.3, .7, .1))
    c.add_poly([Point(3.1, 2.1, "in"), Point(3.3, 2.8, "in"), Point(2.9, 2.7, "in")], color='k')

Arrows
......

add_arrow

Other
.....

add_ellipse,

Images
------

Plot elements
-------------

add_legend, add_colorbar, add_figure_labels

Grids of axes
-------------

Saving
------

