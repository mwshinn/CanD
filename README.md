Matplotlib Canvas
-----------------

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

Canvas is a system for laying out axes and plot elements in a figure
within Python and matplotlib.  It provides:

- **A framework for easily creating axes within a figure.** Axes may
  be individually positioned, positioned in grids, or a combination.
- **Automatic synchronization of fonts and font sizes.** Any system
  font may be easily used.  Fonts are synchronized across all text
  present in the figure, including mathematical equations.  Currently
  this is the only reliable cross-platform method for synchronizing
  fonts in matplotlib to our knowledge.
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
  aliasing artifacts.  Canvas allows .png images to be positioned just
  like any other plot element.

Canvas does not provide::

- Methods for plotting data.  Canvas gives you a reference to the axis
  object, with which you may use any of matplotlib's standard plotting
  functions. [Seaborn](https://seaborn.pydata.org/) is a popular
  library which creates elegant and attractive plots with
  little effort, and is mostly compatible with Canvas.
- Zero-thought layouts.  Canvas will not find a good layout for you.
  If you want automatically-positioned subplots, Canvas is not the
  right choice for you. Canvas will, however, make it easy to
  implement a layout you have in your mind.

Canvas is currently pre-alpha software.  Examples and documentation
will be available eventually.

Installation
============

Canvas depends on:

- numpy
- matplotlib
- seaborn
- paranoid-scientist (version 0.2.1 or greater)
- PyMuPDF
- Pillow

Currently it can be installed by placing canvas.py into the same
directory as your plotting script.
