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
