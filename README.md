CanD - Easily create complex layouts in Matplotlib
--------------------------------------------------

<img align="right" src="cand-logo.png" width="30%" padding="50px">

*Do you plot in Matplotlib, build your diagrams in Inkscape or
Illustrator, and then lay out your figures in InDesign or Powerpoint?
Do you wish you could easily generate scientific figures exclusively
in a single Python script?  CanD gives you the best of all possible worlds.*

CanD features
============

CanD (CANvas Designer) is a system for laying out axes and plot
elements in a figure within Python and Matplotlib.  It provides:

- **A framework for precisely specifying the position of subplots.** Axes may be
  individually positioned, positioned in grids, or a combination.
- **Improved font management.** Alternative to the matplotlib font manager.  Any
  system font may be easily used.  Fonts are synchronized across all text
  present in the figure, including mathematical equations.  Currently this is
  the only reliable cross-platform method for synchronizing fonts in matplotlib
  to our knowledge.
- **An affine algebra system for specifying positions.** Points and
  vectors from different coordinate systems may be used
  interchangeably.  This allows for unprecedented control over element
  positioning.
- **A unified interface for plot elements**.  This allows lines,
  arrows, polygons, and text to be drawn with a single line of code.
  For example, it is easy to draw an arrow from a data point in a
  scatterplot to a plot in a different subpanel.
- **Easy positioning of raster (.png) images.** Currently, importing
  an image directly into matplotlib is difficult and results in
  aliasing artifacts.  CanD allows .png images to be positioned just
  like any other plot element.

CanD does **not** provide:

- Methods for plotting data.  CanD gives you a reference to the axis
  object, with which you may use any of matplotlib's standard plotting
  functions. [Seaborn](https://seaborn.pydata.org/) is a popular
  library which creates elegant and attractive plots with
  little effort, and is mostly compatible with CanD.
- Zero-thought layouts.  CanD will not find a good layout for you.
  If you want automatically-positioned subplots, CanD is not the
  right choice for you. CanD will, however, make it easy to
  implement a layout you have in your mind.

CanD is currently pre-alpha software.  Examples and documentation
will be available eventually.

Example
=======

```python
from cand import Canvas, Vector, Point
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Create a canvas 10 cm x 15 cm.  Use Lucida as the font.
c = Canvas(15, 10, "cm", font="Lucida Std")

# Add an axis from the point (2,2) to (14,8) in centimeters.  Name it "sinewave", 
# and plot a sine wave on it.
c.add_axis("sinewave", Point(2, 2, "cm"), Point(14, 8, "cm"))
ax = c.ax("sinewave")
ax.plot(np.linspace(0, 2*np.pi, 500), np.sin(np.linspace(0, 2*np.pi, 500)))
sns.despine(ax=ax)

# Create an inset axis which is 1 x 1 inch, positioned on the right side of the 
# plot, 75% of the way across and 60% up on the "sinewave" axis.  Name it "sineinset".
insetsize = Vector(1, 1, "inches")
insetloc = Point(.75, .6, "axis_sinewave")
c.add_axis("sineinset", insetloc, insetloc+insetsize)
c.ax("sineinset").plot(np.linspace(0, np.pi), np.sin(np.linspace(0, np.pi)))

# Add a arrow pointing to the peak of one sine wave to the other, i.e. (pi/2,1) 
# in data coordinates (i.e. units of the "sinewave" or "sineinset" axis).
c.add_arrow(Point(np.pi/2, 1, "sinewave"), Point(np.pi/2, 1, "sineinset"))

# Add a watermark of the CanD logo in the lower right corner.
c.add_image("cand-logo.png", Point(1, 0, "figure"), width=Vector(2, 0, "cm"), 
            ha="right", va="bottom")

# Save as a .pdf file, and then show the result
c.save("demo_plot.pdf")
c.show()
```



Why CanD?
=========

Matplotlib is a powerful plotting library, but as a result of this
power comes complexity.  Publication-quality figures require complex
layouts with tight positioning and alignment of multiple display
elements across different axes.  They also often require mixing raster
and vector images, and tight control over font size and style.  These
are in practice quite difficult in matplotlib, not only because of the
amount of code required for these tasks, but also due to the
difficulty of keeping the different parts of the figure in sync with
respect to alignment and style.

Due to this difficulty, users will often export plots from matplotlib
and manually position them within PowerPoint, Inkscape, InDesign, or
other software.  Without extra care, font sizes and line thicknesses
may not be consistent, and figures can easily get out of sync with one
another.


Installation
============

CanD depends on:

- numpy
- matplotlib
- seaborn
- paranoid-scientist (version 0.2.1 or greater)
- PyMuPDF
- Pillow

Install with:

    pip install CanD

or by downloading the package from github and running:

    python setup.py install

