import paranoid as pns
import numpy as np
import matplotlib
import matplotlib.figure
import PIL
import fitz as mupdf # PyMuPDF
import tempfile
import atexit
import os

# If IPython is installed, try to import the display code for it.
try:
    from IPython.display import Image as IPython_Image, display as IPython_display
except ImportError:
    pass

class Metric(pns.Type):
    """A Paranoid Scientist Type for Points and Vectors."""
    def test(self, v):
        assert isinstance(v, Point) or isinstance(v, Vector)
    def generate(self):
        yield Point(0, 0)
        yield Point(.3, .1, "absolute")
        yield Point(.1, .1, "figure")
        yield Point(-.1, .1, "figure")
        yield Point(-.1, -3)
        yield Point(2, 2)
        yield Width(.3)
        yield Width(-.1)
        yield Width(0, "figure")
        yield Height(-1, "absolute")
        yield Height(2, "unique")

@pns.paranoidclass
class Point:
    """A point on the canvas in an arbitrary coordinate system.

    A point represents a specific location on the canvas.  It
    represents an x and y coordinate in a specific coordinate system,
    given by `x`, `y`, and `coordinate`, respectively.  Coordinate
    systems are specified as strings, and are interpreted according to
    a Canvas object.

    Points and vectors can be added or subtracted to produce another
    point.  Points cannot be multiplied or divided by scalars.  Points
    cannot be added to each other, but they can be subtracted to
    produce the vector connecting the two points.

    """
    def __new__(cls, x, y, coordinate="default"):
        if isinstance(coordinate, tuple):
            return Point(x, 0, coordinate[0]) >> Point(0, y, coordinate[1])
        else:
            obj = object.__new__(cls)
            obj.x = x
            obj.y = y
            obj.coordinate = coordinate
            return obj
    def __repr__(self):
        return f'{self.__class__.__name__}({self.x}, {self.y}, "{self.coordinate}")'
    @pns.accepts(pns.Self, Metric)
    def __add__(self, other):
        if isinstance(other, Vector):
            if self.coordinate == other.coordinate and self.coordinate != "various":
                return Point(self.x + other.x, self.y + other.y, self.coordinate)
            else:
                return BinopPoint(self, '+', other)
        raise ValueError(f"Invalid addition between {repr(self)} and {repr(other)}.")
    @pns.accepts(pns.Self, Metric)
    def __sub__(self, other):
        if isinstance(other, Vector):
            if self.coordinate == other.coordinate:
                return Point(self.x - other.x, self.y - other.y, self.coordinate)
            else:
                return BinopPoint(self, '-', other)
        elif isinstance(other, Point):
            if self.coordinate == other.coordinate:
                return Vector(self.x - other.x, self.y - other.y, self.coordinate)
            else:
                return BinopVector(self, '-', other)
        raise ValueError(f"Invalid subtraction between {repr(self)} and {repr(other)}.")
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.coordinate == other.coordinate)
    def __iter__(self):
        yield self.x
        yield self.y
    def __rshift__(self, other):
        if not isinstance(other, Point):
            raise ValueError(f"Invalid meet >> operation between {repr(self)} and {repr(other)}.")
        if self.coordinate == other.coordinate:
            return Point(self.x, other.y, self.coordinate)
        else:
            return BinopPoint(self, '>>', other)
    def __lshift__(self, other):
        return other >> self
    def __or__(self, other):
        if not isinstance(other, Point):
            raise ValueError(f"Invalid mean | operation between {repr(self)} and {repr(other)}.")
        if self.coordinate == other.coordinate:
            return Point((self.x+other.x)/2, (self.y+other.y)/2, self.coordinate)
        else:
            return BinopPoint(self, '|', other)

    @staticmethod
    def _generate():
        yield Point(0, 0)
        yield Point(.3, .1, "absolute")
        yield Point(.1, .1, "figure")

@pns.paranoidclass
class Vector:
    """A vector in an arbitrary coordinate system.

    A Vector represents a difference in location on the canvas.  It
    represents a width and a height in a specific coordinate system,
    given by `x`, `y`, and `coordinate`, respectively.  Coordinate
    systems are specified as strings, and are interpreted according to
    a Canvas object.

    Vectors can be added or subtracted to other vectors or points.
    They can also be multiplied and divided by scalars.

    A Vector which only has an x component is automatically cast to a
    "Width" object, and with only a y component is a "Height" object.

    """
    def __new__(cls, x, y, coordinate="default"):
        if isinstance(coordinate, tuple):
            return Vector(x, 0, coordinate[0]) >> Vector(0, y, coordinate[1])
        else:
            obj = object.__new__(cls)
            obj.x = x
            obj.y = y
            obj.coordinate = coordinate
            return obj
    def __repr__(self):
        return f'{self.__class__.__name__}({self.x}, {self.y}, "{self.coordinate}")'
    @pns.accepts(pns.Self, Metric)
    def __add__(self, other):
        if isinstance(other, Point):
            return other + self
        elif isinstance(other, Vector):
            if self.coordinate == other.coordinate:
                return Vector(self.x + other.x, self.y + other.y, self.coordinate)
            else:
                return BinopVector(self, '+', other)
        raise ValueError(f"Invalid addition between {repr(self)} and {repr(other)}.")
    @pns.accepts(pns.Self, pns.Self)
    def __sub__(self, other):
        if self.coordinate == other.coordinate:
            return Vector(self.x - other.x, self.y - other.y, self.coordinate)
        else:
            return BinopVector(self, '-', other)
    @pns.accepts(pns.Self, pns.Number)
    def __mul__(self, other):
        return Vector(self.x * other, self.y * other, self.coordinate)
    @pns.accepts(pns.Self, pns.Number)
    def __rmul__(self, other):
        return self * other
    def __neg__(self):
        return -1* self
    @pns.accepts(pns.Self, pns.Number)
    @pns.requires("other != 0")
    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other, self.coordinate)
    def __rshift__(self, other):
        if not isinstance(other, Vector):
            raise ValueError(f"Invalid meet >> operation between {repr(self)} and {repr(other)}.")
        if self.coordinate == other.coordinate:
            return Vector(self.x, other.y, self.coordinate)
        else:
            return BinopVector(self, '>>', other)
    def __lshift__(self, other):
        return other >> self
    def width(self):
        """Returns a Width object representing the x component of the Vector."""
        return Width(self.x, self.coordinate)
    def height(self):
        """Returns a Height object representing the y component of the Vector."""
        return Height(self.y, self.coordinate)
    def flipx(self):
        return Vector(-self.x, self.y, self.coordinate)
    def flipy(self):
        return Vector(self.x, -self.y, self.coordinate)
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.coordinate == other.coordinate)
    def __iter__(self):
        yield self.x
        yield self.y
    @classmethod
    def _generate(cls):
        yield Height(.3)
        yield Width(.5)

def Width(x, coordinate="default"):
    return Vector(x, 0, coordinate)

def Height(y, coordinate="default"):
    return Vector(0, y, coordinate)

@pns.paranoidclass
class MetaBinop:
    coordinate = "various"
    op_table = {'+': lambda lhs,rhs : lhs + rhs,
                '-': lambda lhs,rhs : lhs - rhs,
                '*': lambda lhs,rhs : lhs * rhs,
                '/': lambda lhs,rhs : lhs / rhs,
                '>>': lambda lhs,rhs : lhs >> rhs,
                '|': lambda lhs,rhs : lhs | rhs}
    @pns.accepts(pns.Unchecked, pns.Or(Metric, pns.Number), pns.Set(['+', '-', '*', '/', '>>', '|']), pns.Or(Metric, pns.Number))
    def __new__(cls, lhs, op, rhs):
        obj = object.__new__(cls)
        obj.lhs = lhs
        obj.op = op
        obj.rhs = rhs
        return obj
    def __repr__(self):
        # Make it look like a MetaBinop with two Points or two Vectors
        # is a point with the tuple-based naming scheme
        if self.op == '>>' and (not isinstance(self.lhs, MetaBinop)) and (not isinstance(self.rhs, MetaBinop)):
            if isinstance(self, BinopPoint):
                classname = "Point"
            elif isinstance(self, BinopVector):
                classname = "Vector"
            return f'{classname}({self.lhs.x}, {self.rhs.y}, ({repr(self.lhs.coordinate)}, {repr(self.rhs.coordinate)}))'
        # Add parens if the point is a binop
        lhstext = f'({repr(self.lhs)})' if isinstance(self.lhs, MetaBinop) and self.lhs.op != '>>' else repr(self.lhs)
        rhstext = f'({repr(self.rhs)})' if isinstance(self.rhs, MetaBinop) and self.rhs.op != '>>' else repr(self.rhs)
        return f'{lhstext} {self.op} {rhstext}'
    def __eq__(self, other):
        return (self.lhs == other.lhs) and (self.op == other.op) and (self.rhs == other.rhs)

@pns.paranoidclass
class BinopPoint(MetaBinop,Point):
    """A Point which is a composite of points and vectors in different bases.

    Each Vector and Point's coordinate system depends on the Canvas
    object, and thus, we cannot immediately compute sums or
    differences of Vector or Point objects.  Instead, this object
    represents a node in a tree of operations on Vector and Point
    objects which results in a Point object.

    """
    @pns.accepts(pns.Self, Vector)
    def __add__(self, rhs):
        if isinstance(rhs, Vector):
            return BinopPoint(self, '+', rhs)
    @pns.accepts(pns.Self, Metric)
    def __sub__(self, rhs):
        if isinstance(rhs, Vector):
            return BinopPoint(self, '-', rhs)
        elif isinstance(rhs, Point):
            return BinopVector(self, '-', rhs)
    def __lshift__(self, rhs):
        return rhs >> self
    def __rshift__(self, rhs):
        if isinstance(rhs, Point):
            return BinopPoint(self, '>>', rhs)
        else:
            raise ValueError(f"Invalid meet >> between {repr(self)} and {repr(other)}.")
    def __or__(self, rhs):
        if isinstance(rhs, Point):
            return BinopPoint(self, '|', rhs)
        else:
            raise ValueError(f"Invalid mean | between {repr(self)} and {repr(other)}.")

@pns.paranoidclass
class BinopVector(MetaBinop,Vector):
    """A Vector which is a composite of points and vectors in different bases.

    Each Vector and Point's coordinate system depends on the Canvas
    object, and thus, we cannot immediately compute sums or
    differences of Vector or Point objects.  Instead, this object
    represents a node in a tree of operations on Vector and Point
    objects which results in a Vector object.

    """
    @pns.accepts(pns.Self, Metric)
    def __add__(self, rhs):
        if isinstance(rhs, Vector):
            return BinopVector(self, '+', rhs)
        elif isinstance(rhs, Point):
            return rhs + self
    @pns.accepts(pns.Self, Vector)
    def __sub__(self, rhs):
        return BinopVector(self, '-', rhs)
    @pns.accepts(pns.Self, pns.Number)
    def __mul__(self, rhs):
        return BinopVector(self, '*', rhs)
    @pns.accepts(pns.Self, pns.Number)
    def __truediv__(self, rhs):
        return BinopVector(self, '/', rhs)
    def __rshift__(self, rhs):
        if isinstance(rhs, Vector):
            return BinopVector(self, '>>', rhs)
        else:
            raise ValueError(f"Invalid meet >> between {repr(self)} and {repr(other)}.")
    def __lshift__(self, rhs):
        return rhs >> self
    def width(self):
        """Returns a BinopVector object representing the x component of the Vector."""
        # Handle cases where we use a scalar instead of a vector
        return ((Point(0, 0, "figure") + self) >> Point(0, 0, "figure")) - Point(0, 0, "figure")
    def height(self):
        """Returns a BionpVector object representing the y component of the Vector."""
        return ((Point(0, 0, "figure") + self) << Point(0, 0, "figure")) - Point(0, 0, "figure")
    def flipx(self):
        return (-self) >> self
    def flipy(self):
        return self >> (-self)
    @classmethod
    def _generate(cls):
        yield cls(Point(0, 1), '+', Point(3, 2, "absolute"))
        yield cls(Point(-.2, .2), '-', cls(Point(0, -1, "absolute"), '+', Width(2, "otherunit")))

@pns.paranoidclass
class Canvas:
    """Canvas is a convenient way of arranging and organizing axes and other elements on a figure.

    Create a Canvas by specifying its x and y size in inches (`size_x`
    and `size_y`).  Optionally, specify the font size in points
    (`fontsize`) and the font name as a valid postscript font (`font`).

    A Canvas makes it easy to add create attractive composite layouts
    in matplotlib.  When a figure consists of just a single axis, it
    is not difficult to create an attractive layout.  However, when
    many axes are combined (e.g. into subpanels), it becomes more
    difficult to standardize the components such as font size and
    style.  Additionally, for non-grid layouts, it is difficult to
    correctly compute the position of the axes, align text and arrows,
    and other layout-related tasks.  Canvas provides a set of features
    to make layouts and fonts trivial.

    """
    @pns.accepts(pns.Self, pns.Number, pns.Number, pns.String, pns.String, pns.Number, pns.Maybe(pns.Number))
    @pns.paranoidconfig(unit_test=False)
    def __init__(self, size_x, size_y, unit="inches", font="Helvetica Neue LT Std", fontsize=8, fontsize_ticks=None):
        self.axes = dict()
        self.default_unit = "figure"
        self.fontsize = fontsize
        self.fontsize_ticks = fontsize_ticks if fontsize_ticks is not None else fontsize
        self.font = font
        self.images = []
        self.tmpfiles = []
        atexit.register(self._cleanup)
        self.localRc = {}
        # Set up font sizes
        self.localRc['font.size'] = fontsize
        self.localRc['axes.titlesize'] = fontsize
        self.localRc['axes.labelsize'] = fontsize
        self.localRc['xtick.labelsize'] = fontsize_ticks or fontsize
        self.localRc['ytick.labelsize'] = fontsize_ticks or fontsize
        self.localRc['legend.fontsize'] = fontsize
        self.localRc['figure.titlesize'] = fontsize
        
        self.backend = "default"
        # Create default units.  Dictionary of tuples indexed by unit
        # name.  First two elements are x and y scale (with respect to
        # inches) and the last is the origin of the coordinate system.
        if unit in ["inches", "in", "inch"]:
            size_x_inches = size_x
            size_y_inches = size_y
        elif unit in ["cm", "centimeter", "centimeters", "centimetre", "centimetres"]:
            size_x_inches = size_x/2.54
            size_y_inches = size_y/2.54
        elif unit in ["mm", "millimeter", "millimeters", "millimetre", "millimetres"]:
            size_x_inches = size_x/25.4
            size_y_inches = size_y/25.4
        else:
            raise ValueError("Invalid unit")
        self.units = dict()
        self.add_unit("in", Vector(1/size_x_inches, 1/size_y_inches, "figure"))
        self.units["inch"] = self.units["in"]
        self.units["inches"] = self.units["in"]
        self.add_unit("cm", Vector(1/2.54, 1/2.54, "inches"))
        self.units["centimeters"] = self.units["cm"]
        self.units["centimeter"] = self.units["cm"]
        self.units["centimetres"] = self.units["cm"]
        self.units["centimetre"] = self.units["cm"]
        self.add_unit("mm", Vector(.1, .1, "cm"))
        self.units["millimeter"] = self.units["mm"]
        self.units["millimeters"] = self.units["mm"]
        self.units["millimetre"] = self.units["mm"]
        self.units["millimetres"] = self.units["mm"]
        self.add_unit("pt", Vector(1/72, 1/72, "inches"))
        self.units["point"] = self.units["pt"]
        self.units["points"] = self.units["pt"]
        # Create matplotlib figure object
        figsize = (size_x_inches, size_y_inches)
        self.figure = matplotlib.figure.Figure(figsize=figsize)
        self.size = figsize # Size of the figure in inches
    def _cleanup(self):
        for f in self.tmpfiles:
            os.remove(f)
    def _get_font(self, weight="roman", style="normal", size=None, stretch="normal"):
        if size is None:
            size = self.fontsize
        # Add a font manager as a static variable because it is a
        # singleton in matplotlib but it takes forever to construct
        # for some reason.
        if not hasattr(self.__class__, "_fm"):
            self.__class__._fm = matplotlib.font_manager.FontManager()
        fp = matplotlib.font_manager.FontProperties(weight=weight, style=style, size=size, family=self.font, stretch=stretch)
        fontfile = self.__class__._fm.findfont(fp, fallback_to_default=False)
        print(fontfile, stretch, size, style, weight)
        fprops = matplotlib.font_manager.FontProperties(fname=fontfile, size=size)
        return fprops
    @pns.accepts(pns.Self, pns.Maybe(pns.String), pns.String)
    def use_latex(self, preamble=None, engine="pdflatex"):
        """Use latex to render all text.

        `engine` is the latex engine ("texsystem" in matplotlib lingo)
        used to render the text.  It can be "pdflatex", "lualatex", or
        "xelatex".

        Note that this will break math font compatibility.  Because
        latex is being used to render the fonts, you must import a
        package that allows latex to render in the desired font.  For
        example, if `engine` is "pdflatex", to get Helvetica, set
        preamble=r"\\usepackage[scaled]{helvet}\\usepackage[helvet]{sfmath}".
        """
        self.backend = "latex"
        self.latex_engine = engine
        self.latex_preamble = preamble
    @pns.accepts(pns.Self, pns.String, Vector, Point)
    @pns.requires('self.is_valid_identifier(name)')
    @pns.ensures('not self.is_valid_identifier(name)')
    def add_unit(self, name, scale, origin=Point(0, 0, "figure")):
        """Create a new unit of measure.

        A unit is defined by an affine transformation.  It has an
        origin and a scale in the x and y dimensions.  The name of the
        unit is given by `name`, the scale in the x and y directions
        is given by `scale`, and the origin of the coordinate system
        is optionally specified by `origin`.

        """
        scale = self.convert_to_figure_length(scale)
        origin = self.convert_to_figure_coord(origin)
        self.units[name] = (scale.width().x, scale.height().y, origin)
    @pns.accepts(pns.Self, pns.String)
    @pns.requires("self.is_unit(name)")
    def set_default_unit(self, name):
        """Changes the default unit for the Canvas.

        When a unit is not specified for a Point or a Vector, it uses
        the default unit of the Canvas.  The default is initially set
        to figure coordinates.

        """
        self.default_unit = name
    @pns.accepts(pns.Self, pns.String, Point, Point)
    @pns.requires("self.is_valid_identifier(name)")
    @pns.ensures("not self.is_valid_identifier(name)")
    def add_axis(self, name, pos_ll, pos_ur):
        """Create a new axis on the Canvas.

        Create a new matplotlib axis named `name`, with the lower left
        corner at point `pos_ll` and the upper right corner at
        `pos_ur`.  Note that the axis labels, title, and other
        elements may fall outside of this bounding box.  The axis of a
        Canvas object "c" with name "axname" can be accessed by:

            ax = c.ax("axname")

        Then, ax can be used like a normal matplotlib axis.

        This also creates two new coordinate systems: one is given by
        the axis' name, which uses the coordinates of the data in the
        axis, and "axis_" prepended to the axis' name, which is (0,0)
        at the lower left corner and (1,1) at the upper right corner

        """
        assert name not in self.axes.keys(), "Axis name alredy exists"
        assert name != "figure", "Invalid axis name"
        pt_ll = self.convert_to_figure_coord(pos_ll)
        pt_ur = self.convert_to_figure_coord(pos_ur)
        ax = self.figure.add_axes([pt_ll.x, pt_ll.y, pt_ur.x-pt_ll.x, pt_ur.y-pt_ll.y], label=name)
        self.axes[name] = ax
        return ax
    @pns.accepts(pns.Self, pns.String)
    @pns.ensures("self.is_unit(name)")
    def ax(self, name):
        """Return the axis of name `name`."""
        return self.axes[name]
    #@pns.accepts(pns.Self, pns.String, Point, Point, pns.Unchecked, pns.Or(pns.Tuple(pns.Number, pns.Number), matplotlib.colors.Normalize))
    def add_colorbar(self, name, pos_ll, pos_ur, cmap, bounds, **kwargs):
        ax = self.add_axis(name, pos_ll, pos_ur)
        if isinstance(bounds, tuple):
            norm = matplotlib.colors.Normalize(vmin=bounds[0], vmax=bounds[1])
        else:
            norm = bounds
        size = self.convert_to_figure_coord(pos_ur - pos_ll)
        orientation = "horizontal" if size.x*self.size[0] > size.y*self.size[1] else "vertical"
        colorbar = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation=orientation, **kwargs)
        return colorbar
    @pns.accepts(pns.Self, pns.String)
    @pns.returns(pns.Boolean)
    def is_unit(self, name):
        """Whether the value is a in use as a unit of measure.
        
        `name` is a name to test.  Returns True if it is in use or
        False if it is not.

        """
        if name in ["default", "figure", "absolute", "-absolute", "various"]:
            return True
        if name in self.axes.keys():
            return True
        if not name.startswith("axis_") and self.is_unit("axis_"+name):
            return True
        if name in self.units.keys():
            return True
        return False
    @pns.accepts(pns.Self, pns.String)
    @pns.returns(pns.Boolean)
    def is_valid_identifier(self, name):
        """Whether the value can be used as an axis or unit name.
        
        `name` is a name to test.  Returns True if it can be used or
        False if it cannot (e.g. it is a reserved keyword).

        """
        if name.startswith("axis_"):
            return False
        return not self.is_unit(name)
    @pns.accepts(pns.Self, Metric)
    @pns.returns(Metric)
    @pns.ensures("return.coordinate == 'figure'")
    def convert_to_figure_coord(self, point):
        """Convert the coordinate system of the Point or Vector `point` to be "figure".

        We can convert any coordinate system to the "figure"
        coordinate system for a given Point or Vector.  This is useful
        for comparing Points and Vectors, and also used internally as
        a universal coordinate system.  It also collapses Binop
        objects into Points or Vectors.

        """
        if isinstance(point, Vector):
            return self.convert_to_figure_length(point)
        if point.coordinate == "default":
            return self.convert_to_figure_coord(Point(point.x, point.y, self.default_unit))
        if point.coordinate == "figure":
            return point
        if point.coordinate == "absolute":
            return Point(point.x/self.size[0], point.y/self.size[1], "figure")
        if point.coordinate == "-absolute":
            return Point(1-point.x/self.size[0], 1-point.y/self.size[1], "figure")
        if point.coordinate in self.axes.keys():
            tf_data = self.axes[point.coordinate].transData
            tf_fig = self.figure.transFigure.inverted()
            x,y = tf_fig.transform(tf_data.transform((point.x, point.y)))
            return Point(x, y, "figure")
        if point.coordinate.startswith("axis_") and point.coordinate[5:] in self.axes.keys():
            tf_ax = self.axes[point.coordinate[5:]].transAxes
            tf_fig = self.figure.transFigure.inverted()
            x,y = tf_fig.transform(tf_ax.transform((point.x, point.y)))
            return Point(x, y, "figure")
        if point.coordinate in self.units:
            u = point.coordinate
            return Vector(point.x*self.units[u][0], point.y*self.units[u][1], "figure") + self.units[u][2]
        if isinstance(point, BinopPoint):
            # Call recursively, but handle the scalar case separately
            if isinstance(point.lhs, Point) or isinstance(point.lhs, Vector):
                lhs = self.convert_to_figure_coord(point.lhs)
            else:
                lhs = point.lhs
            if isinstance(point.rhs, Point) or isinstance(point.rhs, Vector):
                rhs = self.convert_to_figure_coord(point.rhs)
            else:
                rhs = point.rhs
            return BinopPoint.op_table[point.op](lhs, rhs)
        raise ValueError("Invalid point coordinate system %s" % point.coordinate)
    @pns.accepts(pns.Self, Vector)
    @pns.returns(Vector)
    @pns.ensures("return.coordinate == 'figure'")
    def convert_to_figure_length(self, vector):
        """Convert the coordinate system of the Vector `vector` to be "figure".

        We can convert any coordinate system to the "figure"
        coordinate system for a given Vector.  This is useful for
        comparing vectors, and also used internally as a universal
        coordinate system.  It also collapses BinopVectors into
        Vectors.

        """
        if vector.coordinate == "figure":
            return vector
        elif isinstance(vector, BinopVector):
            # Call recursively, but handle the scalar case separately
            if isinstance(vector.lhs, Point) or isinstance(vector.lhs, Vector):
                lhs = self.convert_to_figure_coord(vector.lhs)
            else:
                lhs = vector.lhs
            if isinstance(vector.rhs, Point) or isinstance(vector.rhs, Vector):
                rhs = self.convert_to_figure_coord(vector.rhs)
            else:
                rhs = vector.rhs
            return BinopVector.op_table[vector.op](lhs, rhs)
        else:
            origin = Point(0, 0, vector.coordinate)
            return self.convert_to_figure_coord(origin+vector) - self.convert_to_figure_coord(origin)
    @pns.accepts(pns.Self, pns.List(Point))
    def add_poly(self, points, **kwargs):
        """Draw a polygon with given vertices.

        Vertices are passed as a list of Point objects via the
        `points` argument.  All other keyword arguments are passed
        directly to matplotlib.patches.Polygon.

        """
        np_points = np.zeros((len(points), 2))
        for i,p in enumerate(points):
            pt = self.convert_to_figure_coord(p)
            np_points[i] = [pt.x, pt.y]
        if "fill" not in kwargs.keys():
            kwargs['fill'] = False
        poly = matplotlib.patches.Polygon(np_points, closed=False, transform=self.figure.transFigure, **kwargs)
        self.figure.add_artist(poly)
    @pns.accepts(pns.Self, Point, Point)
    def add_rect(self, pos_ll, pos_ur, **kwargs):
        """Draw a rectangle.

        The lower left corner is the Point `pos_ll` and the upper
        right corner is the Point `pos_ur`.  All other keyword
        arguments are passed directly to matplotlib.patches.Polygon.

        """
        pt_ll = self.convert_to_figure_coord(pos_ll)
        pt_ur = self.convert_to_figure_coord(pos_ur)
        connect = pt_ur - pt_ll
        # When drawing a box you have to duplicate the last point for
        # some reason... probably a bug in matplotlib
        self.add_poly([pt_ll, pt_ll+connect.height(), pt_ur, pt_ll+connect.width(), pt_ll, pt_ll], **kwargs)
    @pns.accepts(pns.Self, Point, Point)
    def add_box(self, pos_ll, pos_ur, **kwargs):
        """Draw a bounding box.

        The lower left corner is the Point `pos_ll` and the upper
        right corner is the Point `pos_ur`.  All other keyword
        arguments are passed directly to
        matplotlib.patches.FancyBboxPatch.

        Note that this differs from add_rect because it uses the
        FancyBboxPatch rather than matplotlib.patches.Polygon.  Thus,
        this function can be used for, e.g., boxes with round corners
        """
        pt_ll = self.convert_to_figure_coord(pos_ll)
        pt_ur = self.convert_to_figure_coord(pos_ur)
        diff = pt_ur - pt_ll
        if "fill" not in kwargs.keys():
            kwargs['fill'] = False
        if 'mutation_scale' not in kwargs.keys():
            kwargs['mutation_scale'] = (diff.x/self.size[0] +  diff.y/self.size[1])/2
        box = matplotlib.patches.FancyBboxPatch(tuple(pt_ll), diff.x, diff.y, transform=self.figure.transFigure, **kwargs)
        self.figure.add_artist(box)
    @pns.accepts(pns.Self, Point, Point)
    def add_ellipse(self, pos_ll, pos_ur, **kwargs):
        """Draw an ellipse.

        The lower left corner is the Point `pos_ll` and the upper
        right corner is the Point `pos_ur`.  Note that rotation is not
        currently possible because it is not clear in which coordinate
        system the rotation would be applied.  All other keyword
        arguments are passed directly to matplotlib.patches.Ellipse.
        """
        pt_ll = self.convert_to_figure_coord(pos_ll)
        pt_ur = self.convert_to_figure_coord(pos_ur)
        diff = pt_ur - pt_ll
        center = pt_ll | pt_ur
        if "angle" in kwargs.keys():
            print("Warning: the 'angle' keyword passed to add_ellipse may give unexpected results.")
        # When drawing a box you have to duplicate the last point for
        # some reason... probably a bug in matplotlib
        e = matplotlib.patches.Ellipse(xy=tuple(center), width=diff.width().x, height=diff.height().y, **kwargs)
        self.figure.add_artist(e)
    def add_arrow(self, frm, to, arrowstyle="->,head_width=4,head_length=8", lw=2, linestyle='solid', **kwargs):
        """Draw an arrow.

        Draw an arrow from Point `frm` to Point `to`.  All other
        keyword arguments are passed directly to
        matplotlib.patches.FancyArrowPath.  Reasonable default
        arguments are given, but these can be overridden.

        """
        pt_frm = self.convert_to_figure_coord(frm)
        pt_to = self.convert_to_figure_coord(to)
        pt_delta = pt_frm - pt_to
        if "linewidth" in kwargs:
            lw = kwargs['linewidth']
        arrow = matplotlib.patches.FancyArrowPatch(tuple(pt_frm), tuple(pt_to), transform=self.figure.transFigure,
                                                       arrowstyle=arrowstyle, lw=lw, linestyle=linestyle, **kwargs)
        self.figure.patches.append(arrow)
    def add_text(self, text, pos, weight="roman", size=None, stretch="normal", style="normal", **kwargs):
        """Add text at a given point.

        Draw the text `text` at Point `pos`.  The argument `weight`
        specifies the font weight, which varies depending on the
        weights of the font, but potential options may be "light",
        "roma", "bold", "heavy", "black".  The size is given by `size`
        in points, which defaults to the Canvas' default. The width is
        given by "stretch", which can be "consensed", "normal", or
        "wide", depending on the font.  All other keyword arguments
        are passed to matplotlib.pyplot.text.  Notably, the
        `horizontalalignment` and `verticalalignment` arguments are
        often useful.  (`ha` and `va` are also accepted as aliases for
        matplotlib compatibility).
        """
        if size is None:
            size = self.fontsize
        print("Adding text", text)
        kwargs = kwargs.copy()
        if 'horizontalalignment' not in kwargs:
            kwargs['horizontalalignment'] = kwargs['ha'] if 'ha' in kwargs else 'center'
        if 'verticalalignment' not in kwargs:
            kwargs['verticalalignment'] = kwargs['va'] if 'va' in kwargs else 'center'
        pt = self.convert_to_figure_coord(pos)
        # Check valid font names with matplotlib.font_manager.FontManager().findfont(name)
        #self.figure.text(pt.x, pt.y, text, transform=self.figure.transFigure, fontdict={'fontname': "Helvetica Neue LT Std", "fontsize": 20})
        fprops = self._get_font(weight=weight, size=size, stretch=stretch, style=style)
        self.figure.text(pt.x, pt.y, text, transform=self.figure.transFigure,
                         fontproperties=fprops, fontsize=size, **kwargs)
    def add_line(self, frm, to, **kwargs):
        """Draw a line.

        Draw a line from Point `frm` to Point `to`.  All other keyword
        arguments are passed directly to matplotlib.lines.Line2D.

        """
        frm = self.convert_to_figure_coord(frm)
        to = self.convert_to_figure_coord(to)
        l2d = matplotlib.lines.Line2D([frm.x, to.x], [frm.y, to.y], **kwargs)
        self.figure.add_artist(l2d)
    def add_marker(self, pos, **kwargs):
        """Draw a matplotlib marker.

        Plot a marker at Point `pos`.  All other keyword arguments are
        passed directly to matplotlib.lines.Line2D.

        """
        pos = self.convert_to_figure_coord(pos)
        l2d = matplotlib.lines.Line2D([pos.x], [pos.y], **kwargs)
        self.figure.add_artist(l2d)
    @pns.accepts(pns.Self, Point, pns.List(pns.Tuple(pns.String, pns.Dict(k=pns.String, v=pns.Unchecked))), pns.Maybe(pns.Natural1), Metric, Metric, Metric)
    def add_legend(self, pos_tl, els, fontsize=None, line_spacing=Height(2.2, "Msize"), sym_width=Width(2.3, "Msize"), padding_sep=Width(1.2, "Msize")):
        """Add a legend without using the matplotlib API.

        The top-left corner of the legend should be located at the
        Point `pos_tl`.  The `els` argument should be a list of tuples
        representing the elements to include in the legend.  The first
        element of each tuple should be the name of the legend item,
        the second element should be a dictionary of line properties
        to be passed to the add_line and add_marker functions.  To
        withhold drawing a line and only draw markers, set 'linestyle'
        to the string 'None'.

        Additional parameters control formatting.  `line_spacing`
        determines spacing between each line of descriptive text in
        the legend.  `sym_width` is the width of the symbols (lines
        and markers). `padding_sep` is the separation between the
        symbols and the descriptive text.
        """
        if fontsize is None:
            fontsize = self.fontsize
        pos_tl = self.convert_to_figure_coord(pos_tl)
        assert len(els) >= 1
        # Get the text height
        fprops = self._get_font()
        t = matplotlib.textpath.TextPath((0,0), "M", size=fontsize, prop=fprops)
        bb = t.get_extents().inverse_transformed(self.figure.transFigure)
        if self.is_valid_identifier("Msize"):
            self.add_unit("Msize", Vector(self.fontsize, self.fontsize, "point"))
        # All params are in units of M width or height
        padding_top = Height(0, "Msize") # Space on top of figure
        padding_left = Width(0, "Msize") # Space on left of lines
        # Convert these to an easier coordinate system
        padding_top = self.convert_to_figure_length(padding_top)
        padding_left = self.convert_to_figure_length(padding_left)
        padding_sep = self.convert_to_figure_length(padding_sep)
        line_spacing = self.convert_to_figure_length(line_spacing)
        sym_width = self.convert_to_figure_length(sym_width)
        top_left = pos_tl - padding_top + padding_left
        for i in range(0, len(els)):
            # Figure out the vertical position of this element of the legend
            y_offset = -1*line_spacing*i
            print(y_offset)
            # Draw the text
            self.add_text(els[i][0],
                          top_left + sym_width + padding_sep + y_offset,
                          horizontalalignment="left", size=fontsize)
            pt1 = top_left + y_offset
            pt2 = top_left + sym_width + y_offset
            # Draw the line
            params_nomarker = els[i][1].copy()
            params_nomarker['markersize'] = 0
            self.add_line(pt1, pt2, **params_nomarker)
            # Draw the marker.  We need this in an if statement due to
            # a bug in matplotlib.
            params_noline = els[i][1].copy()
            params_noline['linestyle'] = 'None'
            self.add_marker(pt1+(pt2-pt1)/2, **params_noline)
    @pns.accepts(pns.Self, pns.List(pns.Or(pns.Tuple(pns.String, pns.String),
                                           pns.Tuple(pns.String, pns.String, Metric))),
                 pns.Natural0)
    @pns.requires("all((l[1] in self.axes.keys()) or (self.is_unit(l[1])) for l in labs)")
    def add_figure_labels(self, labs, size=12):
        """Add letter labels to axes.

        `labs` should be a list of tuples of length 2 or 3.  The first
        element of each tuple is a string of the label text, most
        commonly a single lowercase letter.  The second element of the
        tuple is the name of an axis on the canvas.  The optional
        final element may be either a point (to specify manual
        positioning) or a vector (to specify an offset from the
        default position).
        """

        for l in labs:
            offset = Vector(-.15, .12, "absolute")
            loc = Point(0, 1, "axis_"+l[1] if l[1] in self.axes.keys() else l[1])
            if len(l) == 3:
                if isinstance(l[2], Vector):
                    offset += l[2]
                elif isinstance(l[2], Point):
                    offset = l[2]
            self.add_text(l[0], loc+offset, weight="heavy", size=size)
    def fix_fonts(self):
        """Convert all text to the desired font.

        This function will fix all font objects within the figure.
        This must be called before displaying or saving the Canvas.
        Usually this is called automatically, but can be called
        manually as well.
        """
        fprops = self._get_font()
        fprops_bold = self._get_font(weight="bold")
        fprops_it = self._get_font(style="italic")
        fprops_ticks = self._get_font(size=self.fontsize_ticks)
        for ax in self.figure.axes:
            for label in ax.get_xticklabels():
                label.set_fontproperties(fprops_ticks)
            for label in ax.get_yticklabels():
                label.set_fontproperties(fprops_ticks)
            ax.set_xlabel(ax.get_xlabel(), fontproperties=fprops)
            ax.set_ylabel(ax.get_ylabel(), fontproperties=fprops)
            ax.set_title(ax.get_title(), fontproperties=fprops)
            if ax.legend_:
                for t in ax.legend_.texts:
                    t.set_fontproperties(fprops)
        # Get Helvetica for math as well
        self.localRc['mathtext.fontset'] = 'custom'
        self.localRc['mathtext.rm'] = fprops.get_fontconfig_pattern()
        self.localRc['mathtext.default'] = "rm"
        self.localRc['mathtext.bf'] = fprops_bold.get_fontconfig_pattern()
        self.localRc['mathtext.it'] = fprops_it.get_fontconfig_pattern()
        self.localRc['mathtext.cal'] = fprops.get_fontconfig_pattern()
        self.localRc['mathtext.tt'] = fprops.get_fontconfig_pattern()
        self.localRc['mathtext.sf'] = fprops.get_fontconfig_pattern()
        # Workaround for a bug in matplotlib where there are no
        # negative signs in front of axis labels in latex mode
        if self.backend == "latex":
            for ax in self.figure.axes:
                labels = ax.get_yticklabels()
                ticks = ax.get_yticks()
                for i in range(0, len(labels)):
                    if labels[i].get_text().strip() == "":
                        l = "%g" % ticks[i]
                        labels[i].set_text(l)
                ax.set_yticklabels(labels)
    def _grid_space(self, frm, to, spacing, count):
        dist = to-frm
        figsize = (dist-(count-1)*spacing)/count
        pos = []
        for i in range(0, count):
            base = frm+i*(figsize+spacing)
            pos.append((base, base+figsize))
        return pos
    @pns.accepts(pns.Self, pns.List(pns.Maybe(pns.String)), pns.Natural1, Point, Point, pns.Maybe(Vector), pns.Maybe(Vector), pns.Maybe(Vector), pns.Maybe(Vector), pns.Maybe(Vector), pns.Maybe(Vector), pns.Maybe(pns.String))
    @pns.requires("int(spacing_x is not None) + int(size_x is not None) + int(spacing is not None) + int(size is not None) == 1") # Exactly one of spacing_x, size_x, spacing, or size must be specified
    @pns.requires("int(spacing_y is not None) + int(size_y is not None) + int(spacing is not None) + int(size is not None) == 1") # Exactly one of spacing_y, size_y, spacing, or size must be specified
    def add_grid(self, names, nrows, pos_ll, pos_ur, spacing_x=None, spacing_y=None, spacing=None, size_x=None, size_y=None, size=None, unitname=None):
        """Create a grid of axes.

        Axes are specified by the `names` argument, a
        (one-dimensional) list of strings specifying the names of the
        axes to be created on the grid.  Optionally an element may be
        None, indicating that no axis should be created at this
        location on the grid.  Names start on the top line and go left
        to right and then line by line, just like words on a page.

        The argument `nrows` specifies how many rows should be
        created; the number of columns is implied by the number of
        rows and the length of `names`.

        The lower left corner of the grid is located as Point `pos_ll`
        and the upper right corner is at Point `pos_ur`.

        There are two ways to specify spacing of axes.  One method is
        to specify the size of the axes by the Vector `size`, or
        component-wise by the Width `size_x` and Height `size_y`.
        Axes will be automatically spaced to maintain the given size
        The other method is to specify the spacing of the axes with
        the Vector `spacing` or component-wise with the Width
        `spacing_x` and Height `spacing_y`.  The axes will be
        automatically sized to give the desired spacing.  Finally, it
        is possible to mix these styles by specifying `spacing_x` and
        `size_y` or vice versa.

        Optionally, `unitname` may specify a name for relative units
        based on the grid as a whole, i.e. where the origin is located
        at the bottom left corner of the bottom left figure in the
        grid, and (1,1) is located at the upper right corner of the
        upper right grid.
        """
        if spacing is not None:
            spacing_x = spacing.width()
            spacing_y = spacing.height()
        if size is not None:
            size_x = size.width()
            size_y = size.height()
        ncols = len(names)//nrows + int(len(names) % nrows != 0)
        pt_ll = self.convert_to_figure_coord(pos_ll)
        pt_ur = self.convert_to_figure_coord(pos_ur)
        if size_x is not None:
            size_x = self.convert_to_figure_length(size_x)
            if ncols > 1:
                spacing_x = ((pt_ur - pt_ll).width() - size_x * ncols)/(ncols-1)
            elif ncols == 1:
                spacing_x = size_x*0
                w = (pt_ur-pt_ll).width()
                pt_ll = pt_ll + (w - size_x)/2
                pt_ur = pt_ur - (w - size_x)/2
            print("Spacing", spacing_x)
        if size_y is not None:
            size_y = self.convert_to_figure_length(size_y)
            if nrows > 1:
                spacing_y = ((pt_ur - pt_ll).height() - size_y * nrows)/(nrows-1)
            elif nrows == 1:
                spacing_y = size_y*0
                h = (pt_ur-pt_ll).height()
                pt_ll = pt_ll + (h - size_y)/2
                pt_ur = pt_ur - (h - size_y)/2
            print("Spacing", spacing_y)
        spacing_x = self.convert_to_figure_length(spacing_x)
        spacing_y = self.convert_to_figure_length(spacing_y)
        posx = self._grid_space(pt_ll.x, pt_ur.x, spacing_x.x, ncols)
        posy = list(reversed(self._grid_space(pt_ll.y, pt_ur.y, spacing_y.y, nrows)))
        for i in range(0, len(names)):
            x = i % ncols
            y = i // ncols
            if names[i] is not None:
                self.add_axis(names[i], Point(posx[x][0], posy[y][0], "figure"), Point(posx[x][1], posy[y][1], "figure"))
        if unitname is not None:
            assert self.is_valid_identifier(unitname), "Invalid axis name"
            self.add_unit(unitname, (pt_ur-pt_ll), pt_ll)

    @pns.accepts(pns.Self, pns.String, pns.Maybe(pns.Natural1))
    def save(self, filename, dpi=None, *args, **kwargs):
        """Save the Canvas to a png or pdf file.

        The filename is specified by the string `filename`.
        Optionally, when `filename` ends in .png, the `dpi` argument
        may specify the dots per inch (dpi) of the output .png file,
        where larger numbers indicate a higher resolution and larger
        file size.  Any additional arguments or keyword arguments are
        passed to the "savefig" function in matplotlib.
        """
        filetypes = ['png', 'pdf']
        filetype = next(ft for ft in filetypes if filename.endswith("."+ft))
        assert (dpi is None) or filename.endswith(".png"), "DPI argument only supported for png files"
        self.fix_fonts()
        # Lazy importing of matplotlib backend
        if self.backend == "latex":
            from matplotlib.backends.backend_pgf import FigureCanvasPgf
            mplcanvas = FigureCanvasPgf(self.figure)
            matplotlib.rc('pgf', texsystem=self.latex_engine)
            if self.latex_preamble is not None:
                preamble = matplotlib.rcParams.setdefault('pgf.preamble', [])
                preamble.append(self.latex_preamble)
        elif self.backend == "default":
            from matplotlib.backends.backend_agg import FigureCanvasAgg
            mplcanvas = FigureCanvasAgg(self.figure)
        with matplotlib.rc_context(rc=self.localRc):
            self.figure.savefig(filename, dpi=dpi, *args, **kwargs)
        if filetype == "png":
            with PIL.Image.open(filename) as img:
                img = img.convert('RGBA')
                for image in self.images:
                    if image[0].endswith(".pdf"): # Convert pdf to png first
                        pdf = mupdf.open(image[0])
                        page = pdf[0]
                        imgpath = tempfile.mkstemp('.png')[1]
                        zoom = int(np.ceil(dpi/72)) if dpi else 1
                        page.getPixmap(alpha=True, matrix=mupdf.Matrix(zoom, zoom)).writeImage(imgpath)
                    else:
                        imgpath = image[0]
                    with PIL.Image.open(imgpath) as subimg:
                        subimg = subimg.convert('RGBA')
                        imwidth = img.size[0]
                        imheight = img.size[1]
                        pos_ll = image[1]
                        pos_ur = image[2]
                        # subimg.thumbnail(size)
                        bounds = (int(imwidth*pos_ll.x), int(imheight*(1-pos_ur.y)), int(imwidth*pos_ur.x), int(imheight*(1-pos_ll.y)))
                        print(bounds)
                        subimg_size = (bounds[2]-bounds[0], bounds[3]-bounds[1])
                        subimg = subimg.resize(subimg_size, PIL.Image.LANCZOS)
                        img.alpha_composite(subimg, bounds[0:2])
                img.save(filename)
        elif filetype == "pdf":
            pdf = mupdf.open(filename)
            page = pdf[0]
            pwidth = page.bound().width
            pheight = page.bound().height
            for image in self.images:
                pos_ll = image[1]
                pos_ur = image[2]
                rect = mupdf.Rect(pwidth*pos_ll.x, pheight*(1-pos_ur.y), pwidth*pos_ur.x, pheight*(1-pos_ll.y))
                print(rect)
                print(page.bound())
                #rect = mupdf.Rect(0.0, 0.0, 200.0, 200.0)
                #imagedoc = mupdf.open(image[0])
                #imagepdf_bytes = imagedoc.convertToPDF()
                #imagepdf = mupdf.open("pdf", imagepdf_bytes)
                #page.showPDFpage(rect, imagepdf)
                if image[0].endswith(".pdf"):
                    toinsert = mupdf.open(image[0])
                    page.showPDFpage(rect, src=toinsert, keep_proportion=False)
                else:
                    page.insertImage(rect, filename=image[0], keep_proportion=False)
            pdf.saveIncr()
            pdf.close()
    def add_image(self, filename, pos, unitname=None, height=None, width=None, horizontalalignment=None, verticalalignment=None, ha=None, va=None):
        """Add a png or pdf image to the Canvas.

        Insert a .png or .pdf file overlaid on the Canvas.  The string
        `filename` is the filename of the image, the Point `pos` is
        the location of the image, aligned according to
        `horizontalalignment` (may be "left", "center", or "right")
        and `verticalalignment` (may be "top", "center", or "bottom").
        For compatibility, `ha` and `va` may be used instead.  Either
        a Height `height` or a Width `width` must be specified.  The
        image will be scaled in the unspecified direction to maintain
        the aspect ratio.  If both `height` and `width` are specified,
        then the image's aspect ratio will be ignored.

        Note: As the conversion processes for png and pdf export use
        different libraries, there may be slight differences in output
        depending on output format.

        Optionally, `unitname` may specify a unit for the image,
        i.e. the origin is located at the bototm left corner of the
        image, and (1,1) is located at the upper right corner of the
        image.
        """
        if horizontalalignment is None:
            horizontalalignment = ha if ha is not None else "center"
        if verticalalignment is None:
            verticalalignment = va if va is not None else "center"
        pos_ll = self.convert_to_figure_coord(pos)
        assert height is not None or width is not None, "Either height or width must be given"
        if filename.endswith(".pdf"):
            pdf = mupdf.open(filename)
            page = pdf[0]
            imwidth = page.bound().width
            imheight = page.bound().height
        else:
            with PIL.Image.open(filename) as img:
                imwidth = img.size[0]
                imheight = img.size[1]
        if width is None:
            height = self.convert_to_figure_length(height.height())
            width = Width(height.y * (self.size[1]/self.size[0]) * (imwidth/imheight), "figure")
            print("width is", width*self.size[0], height*self.size[1])
        elif height is None:
            width = self.convert_to_figure_length(width.width())
            height = Height(width.x * (self.size[0]/self.size[1]) * (imheight/imwidth), "figure")
            print("Height is", height*self.size[1], width*self.size[0])
        else:
            height = self.convert_to_figure_length(height.height())
            width = self.convert_to_figure_length(width.width())
        pos_ur = pos_ll + height + width
        if horizontalalignment == "center":
            shift = (pos_ur-pos_ll).width()/2
            pos_ur -= shift
            pos_ll -= shift
        elif horizontalalignment == "right":
            shift = (pos_ur-pos_ll).width()
            pos_ur -= shift
            pos_ll -= shift
        if verticalalignment == "center":
            shift = (pos_ur-pos_ll).height()/2
            pos_ur -= shift
            pos_ll -= shift
        elif verticalalignment == "top":
            shift = (pos_ur-pos_ll).height()
            pos_ur -= shift
            pos_ll -= shift
        assert 0 <= pos_ll.x and 0 <= pos_ll.y and pos_ur.x <= 1 and pos_ur.y <= 1, "Coordinates must not go off the screen"
        filetypes = ["png", "jpg", "jpeg", "gif", "pdf"]
        assert any(ft for ft in filetypes if filename.endswith("."+ft))
        self.images.append((filename, pos_ll, pos_ur))
        if unitname is not None:
            assert self.is_valid_identifier(unitname), "Invalid axis name"
            self.add_unit(unitname, (pos_ur-pos_ll), pos_ll)
    def show(self, **kwargs):
        """Display the Canvas in a new window (non-blocking) or in Jupyter.

        Keyword arguments are the same as they are for Canvas.save,
        with the exception of "filename", which is of course not
        available here.
        """
        # Test if we are in a Jupyter notebook or in the IPython
        # interpreter.
        in_jupyter = True
        try:
            get_ipython
        except NameError:
            in_jupyter = False
        # Save a temporary image file with the plot
        tmp = tempfile.mkstemp('.png')[1]
        self.tmpfiles.append(tmp)
        self.save(tmp, **kwargs)
        # Display, either in a new window, or in Jupyter
        if in_jupyter:
            IPython_display(IPython_Image(filename=tmp))
        else:
            PIL.Image.open(tmp).show()
        


        
# c = Canvas(6,6)
# c.add_axis("axname", Point(.05, .05), Point(.95, .95))
# c.ax("axname").plot([1, 2, 3])
# #coords = c.add_legend(Point(.1, .9), [LegendItem("M1", "k", linestyle='-'), LegendItem("M2", "r", linestyle='-', lw=7), LegendItem("M3", "r", linestyle='-', lw=2, markersize=10, marker="o"), LegendItem("M4", "r", linestyle='-', lw=2, markersize=10, marker="o")])
# c.add_legend(Point(.4, .9), [LegendItem("M1", "k"), LegendItem("M2", "r"), LegendItem("M3", "b")], fontsize=12)
# c.add_image("smiley.png", Point(0, 1), width=Width(1), verticalalignment="top", horizontalalignment="left")
# #c.save("output.pdf")
# c.show()
# #plt.show()


# TODO:
# TODO add "thin" to font-manager.py in matplotlib line 81
# Jupyter support: https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html
