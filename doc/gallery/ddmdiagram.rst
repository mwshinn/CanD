Generalized Drift Diffusion Model diagram
=========================================

Summary
-------

Here, we will show how to build each individual component found in the diagram
describing the generalized drift diffusion model (GDDM), as seen in `Figure 1
<https://elifesciences.org/articles/56938/figures#fig1>`_ from `Shinn et
al. 2020 <https://elifesciences.org/articles/56938>`_.  This is a good
demonstration because it does not require data files to produce.

Setting up the figure
~~~~~~~~~~~~~~~~~~~~~

First, we import the plotting libraries and define some basic properties:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin preamble
   :end-before: # End preamble

Define a function we will use later to make the plotting look nice:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin plot function
   :end-before: # End plot function


Now, we initialize the Canvas object within CanD:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin canvas initialization
   :end-before: # End canvas initialization

DDM schematic
~~~~~~~~~~~~~

We create a new unit, which we call "absolute2".  We do this so that we can use
a separate coordinate system for each part of the plot.  This makes it easy to
adjust the position of the different parts separately.  Then, we set it as the
default unit so that we don't have to worry about adding "absolute2" to the end
of all of our Points:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin default unit
   :end-before: # End default unit

We add two axes, one for the actual DDM, and one for the plot showing the change
in evidence over time:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin other axes
   :end-before: # End other axes

First, we simulate the model to create the diagram.  Note that we make some
cosmetic changes to the DDM trace for the purpose of clarity within the
diagram:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin model simulation
   :end-before: # End model simulation

Next, we plot the trace on the axis, and draw the upper and lower bounds on the
same axis:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin ddm plot
   :end-before: # End ddm plot

Now, we annotate the DDM diagram.  First, we draw an an arrow to denote the
non-decision time.  We make the arrow a distance indicator, and change the shape
to make it attractive.  We position it using the non-decision time startpoint,
determined from the coordinates within the axis:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin ddm annotate
   :end-before: # End ddm annotate

Label the bounds:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin ddm bounds label
   :end-before: # End ddm bounds label

Draw an arrow indicating the drift rate, and label it:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin drift rate arrow
   :end-before: # End drift rate arrow

Draw and label the starting point:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin x0 label
   :end-before: # End x0 label

Draw and label the evidence over time:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin label evidence over time
   :end-before: # End label evidence over time

Full DDM schematic
~~~~~~~~~~~~~~~~~~

First, we set up a grid of axes for the starting point, variable drift rate, and
non-decision time features of the Full DDM, as well as the evidence over time
axis:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin set up full ddm
   :end-before: # End set up full ddm

The following will allow us to draw any distribution sideways on an axis.  We
write this as a function because, while it is simply a uniform distribution
here, we will want to draw a more complicated distribution later for the GDDM.
This functions by transforming the points to data space, setting the clip off,
and then filling in the region between the curve and the axis.  This is mostly
performed in pure matplotlib, and does not require features from CanD:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin make starting pos
   :end-before: # End make starting pos

We also draw an arbitrary distribution for the non-decision time.  By contrast,
this uses some features of CanD.  It operates by creating a new axis on top of
the existing axis, turning off the spines, and drawing the distribution on the
new axis.  Then, it uses CanD to draw an "arrow" (that looks like "|---"),
similar to the one drawn on the DDM plot:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin make nd time
   :end-before: # End make nd time

Lastly, we draw the drift rate.  We seek to draw an arrow with a Gaussian
distribution at the bottom.  We accomplish this by defining a Gaussian
distribution, rotating it by 45 degrees, placing it on a new axis.  We set the
position of the new axis based on the position of the arrow:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin full drift rate
   :end-before: # End full drift rate

And, as before, we plot the constant evidence signal:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin evidence ddm
   :end-before: # End evidence ddm

GDDM
~~~~

First, we work on the six main plots showing GDDM features.  We will look at the
evidence streams later.  As in the Full DDM case, create a grid of axes:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin gddm grid
   :end-before: # End gddm grid

We can reuse the code from the Full DDM to easily plot the starting position
distribution:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin gddm starting pos
   :end-before: # End gddm starting pos

and the non-decision time distribution:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin gddm nd time
   :end-before: # End gddm nd time

To form the curved arrow in the drift rate plot, we create a sine-like wave
showing what we want, and then rotate it by 45 degrees, the same way we did
above.  We use the rotated coordinates as the start of the arrow, and then make
the arrow short.  We need to set the xlim and ylim before drawing the arrow but
after plotting the function, or else matplotlib may readjust the axis limits
after the arrow has been drawn.

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin gddm drift
   :end-before: # End gddm drift

We draw bounds as red lines which converge to the center.  This is mostly pure
matplotlib.

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin gddm bounds
   :end-before: # End gddm bounds

Draw a grid of arrows.  We want the arrows to face up when below the midpoint
and down when above it.  So we loop through x coordinates and y coordinates in a
grid.

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin leaky
   :end-before: # End leaky

We do the same thing, except with arrows facing the other way.

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin unstable
   :end-before: # End unstable

Create a grid of axes to use for the different evidence streams:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin evidence grid
   :end-before: # End evidence grid

Now plot the streams on these axes:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin gddm evidence
   :end-before: # End gddm evidence

Add section labels:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin section labels
   :end-before: # End section labels

Finally, save the figure:

.. literalinclude:: ../downloads/ddmdiagram.py
   :language: python
   :start-after: # Begin save
   :end-before: # End save

.. image:: ../_static/images/ddmdiagram.png
