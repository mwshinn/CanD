# Let's walk through how the Canvas library works.  To do this, we
# will create a labeled scatterplot, where some of the labels are axes
# themselves.

from canvas import Canvas, Point, Vector
import numpy as np

# Each Canvas object represents a single display of axes, similar to a
# matplotlib "Figure" object.  The size is specified in inches by
# default, but this can be changed to other units, such as cm or pt.
# We also specify 8 pt font instead of the default of 12.  For
# demonstration, we uset he font "Impact", but the default is the much
# more sensible Helvetica Neue LT.
c = Canvas(5, 3, "inches", fontsize=8, font="Impact")

# Create a square scatterplot axis, which we will name "scatter".  Put
# it on the left side with left and bottom margin of .55 in and top margin of .2 in
c.add_axis("scatter", Point(.55, .55, "inches"), Point(2.8, 2.8, "inches"))

# Now generate some data which we can plot on this axis.
np.random.seed(0)
data = np.random.random((2,10))

# To plot the data, first we need to get the matplotlib axis object
# which corresponds to the "scatter" axis.  Once we have it, we can
# use it like any ordinary matplotlib axis.
ax = c.ax("scatter")
ax.scatter(data[0], data[1])
ax.set_xlabel("$\\sum_i \\theta_i$")
ax.set_ylabel("$\\Delta$Y")

# To see what we have so far, we can use the show() function.  Note
# that, unlike matplotlib's show() function, this will not clear the
# plot after displaying it.  Also, notice how the fonts are
# automatically displayed in the font Impact, including the LaTeX
# portions.
c.show()


# Now let's label a single point with an arrow.  Let's choose the
# first point.
point_x, point_y = data[:,0]
# To label this point with an arrow and text, we first draw the arrow.
# We will do this drawing with "Point" and "Vector" objects.  These
# each contain two coordinates and a unit, specified as their three
# arguments.  There are many potential types of units, as we will soon
# see.  Here, we will use "cm" for units of centimeters and "scatter",
# the unit for data points on the "scatter" axis.  Let's say we want
# the arrow to extend 1.1 cm up and 1.4 cm to the left.
arrow_size = Vector(-1.1, -1.4, "cm")
arrow_start = Point(point_x, point_y, "scatter") # "scatter" 
c.add_arrow(arrow_start+arrow_size, arrow_start)

# To annotate this arrow, we add text aligned at the bottom of the
# arrow.
c.add_text("My\npoint", arrow_start+arrow_size, verticalalignment="top")

# Likewise, let's add a label next to each point indicating the point
# number.
for i in range(0, len(data[0,:])):
    c.add_text(str(i), Point(data[0,i], data[1,i], "scatter") + Vector(.2, 0, "cm"), horizontalalignment="left")

# Now let's check our work.  Notice again that the font is correct
# changed to "Impact".
c.show()


# Suppose each of these points on the scatterplot represents more
# complex data, so we want to associate a plot with three of them.  We
# can make a grid of axes.  Then we can loop through them for each
# point.
c.add_grid(["point7", "point8", "point5"], 3, Point(3.6, .5, "inches"), Point(4.9, 2.8, "inches"), spacing=Vector(.5, .5, "inches"))
for i in [7, 8, 5]:
    axname = "point"+str(i)
    ax = c.ax(axname)
    ax.plot(np.random.random(10))
    ax.set_yticks([])
    ax.spines['right'].set_visible(True)
    ax.spines['top'].set_visible(True)
    # Draw lines from the top and bottom of the plot to the point.
    # The unit "axis_point1" represents the relative position with
    # respect to the axis location, where (0,0) is the bottom left and
    # (1,1) is the upper right.
    c.add_line(Point(data[0,i], data[1,i], "scatter"), Point(0, 0, "axis_"+axname), linewidth=.5, alpha=.5, color='k', linestyle='--')
    c.add_line(Point(data[0,i], data[1,i], "scatter"), Point(0, 1, "axis_"+axname), linewidth=.5, alpha=.5, color='k', linestyle='--')


# Suppose we also want to include a small image of a sun in the upper
# right corner.  If the image is saved in .png format, it can be
# easily added to the figure.
#
# There are a few different options for specifying the position of the
# image.  As with an axis, we could specify both the position of the
# bottom left corner.  However, unless the image is square, this could
# be a pain in the butt to calculate the exact dimensions to avoid
# stretching the image.  Instead, we can specify either the width or
# the height of the image and the position to have the dimensions be
# determined automatically.
c.add_image("sun.png", pos=Point(4.95, 2.95, "inches"), width=Vector(.3, 0, "inches"), horizontalalignment="right", verticalalignment="top")


# Finally, since we have several figures, we would like to number them
# "a", "b", "c" and "d".  There is a convenience function to do this
# automatically in a standardized format - simply list the desired
# letter and axis name as a tuple.  An option third entry of the tuple
# can specify an offset if desired.
c.add_figure_labels([("a", "scatter"), ("b", "point7"), ("c", "point8"), ("d", "point5")])



# Once we are done, we can save this as a low-resolution png, a
# high-resolution png, and a pdf.
c.save("test.pdf")
c.save("test.png")
c.save("test-hires.png", dpi=450)
