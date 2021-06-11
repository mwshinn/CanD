FAQs
====

What is the difference between CanD, Seaborn, and Matplotlib?
-------------------------------------------------------------

Matplotlib is a plotting library for Python.  Most other scientific
visualization libraries (including CanD and Seaborn) use Matplotlib under the
hood.

Seaborn is a set of convenience functions for Matplotlib which make it easy to
make beautiful plots.  It introduces new types of plots.

CanD is a system to build complex figures, especially multipanel figures.
Matplotlib makes it convenient to arrange plots in a grid, but it is difficult
to build detailed arrangements of plot elements.  CanD provides an intuitive
interface for designing multipanel figures with precise positioning.


How is plotting with Matplotlib different to plotting with CanD?
----------------------------------------------------------------

CanD can be used to design the layout, but does not perform plotting itself.
After designing a layout with CanD, you will have access to the Matplotlib
"Axis" objects, e.g., the kind you would obtain if you ran "plt.gca()".  Most
convenience functions in pyplot (i.e. anything which starts "plt.") have
equivalents which operate directly on the Axis object.  See the `Matplotlib Axis
object <https://matplotlib.org/stable/api/axis_api.html>`_ for more information.
This is sometimes called the Matplotlib "Object oriented API".


Why do the "add_arrow" and "add_line" function have imprecise positions for line/arrow endpoints?
-------------------------------------------------------------------------------------------------

By default, matplotlib does not draw lines at the specified position, but
instead, draws them with a gap.  CanD respects this default.  To draw lines with
precise positions, use the arguments `shrinkA=0` and `shrinkB=0`.


Why do I get "Paranoid" errors?
-------------------------------

`Paranoid Scientist <http://paranoid-scientist.readthedocs.io>`_ is a library
for verifying the accuracy of scientific software.  It is used to check the
entry and exit conditions of functions.  Paranoid Scientist will, overall,
decrease the probability of an undetected error by increasing the number of bugs
overall.

Most of the time, if you obtain such an error, it means you have passed the
wrong arguments to a CanD function.  Check to make sure you are using the
function correctly.  The error message will often give you hints on why your
choice of a function argument was incorrect.

If you have already confirmed that you are using the correct arguments but
continue to receive the error, please open a `bug report
<https://github.com/mwshinn/cand/issues>`_.

Why don't the minus signs in my axis label work in my favorite font?
--------------------------------------------------------------------

Matplotlib uses the Unicode minus sign by default for negative values, which not
all fonts support.  `See the matplotlib documentation to disable this
<https://matplotlib.org/stable/gallery/text_labels_and_annotations/unicode_minus.html>`_.


Why can't CanD find the bold or italic version of my favorite font?
-------------------------------------------------------------------

Not all fonts are supported by matplotlib, and hence by CanD.  If your font is
not a truetype or opentype font, matplotlib may still provide some support if
you have an .afm file to go along with your font.  CanD drops this support.

If your font *is* a truetype or opentype font, then you may want to double check
that matplotlib is properly supporting your font!  Matplotlib automatically
substitutes the "best match" font for the one you specified.  Thus, it may be
replacing your desired font with a different font for the bold or italic text!

For example, "ttc" (truetype collection) is a common format for Mac computers
which encapsulates multiple fonts in one.  Matplotlib (and hence CanD) only
support accessing the first font in the collection.  Matplotlib will
automatically substitute other fonts for the subsequent fonts in the collection,
but CanD will not.

The lack of automatic substitution was an intentional design decision in CanD,
just as automatic substitution was an intentional design decision in matplotlib.
CanD's font system (fontant) is intended to make sure you have full control over
how your figure is created.  It also prevents occasional mistakes in the
automatic substitution.  For example, it is possible that running the same code
twice in matplotlib will produce different outputs.  This happens if two fonts
are equally good "best matches" to an unavailable font.  CanD is designed to
avoid this behavior by throwing an error if the font is not available.
