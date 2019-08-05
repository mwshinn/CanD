import paranoid as pns
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import PIL
import fitz as mupdf # PyMuPDF
import tempfile
import atexit
import os

class Metric(pns.Type):
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
    @pns.accepts(pns.Self, pns.Number, pns.Number, pns.String)
    def __init__(self, x, y, coordinate="default"):
        self.x = x
        self.y = y
        self.coordinate = coordinate
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
                return BinopPoint(self, '-', other)
        raise ValueError(f"Invalid subtraction between {repr(self)} and {repr(other)}.")
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.coordinate == other.coordinate)
    @staticmethod
    def _generate():
        yield Point(0, 0)
        yield Point(.3, .1, "absolute")
        yield Point(.1, .1, "figure")

@pns.paranoidclass
class Vector:
    def __new__(cls, x, y, coordinate="default"):
        if y == 0 and cls == Vector and x != 0:
            return Width(x, coordinate)
        elif x == 0 and cls == Vector and y != 0:
            return Height(y, coordinate)
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
    def width(self):
        return Width(self.x, self.coordinate)
    def height(self):
        return Height(self.y, self.coordinate)
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.coordinate == other.coordinate)
    @classmethod
    def _generate(cls):
        yield Height(.3)
        yield Width(.5)

class Width(Vector):
    def __new__(cls, x, coordinate="default"):
        obj = object.__new__(cls)
        obj.x = x
        obj.y = 0
        obj.coordinate = coordinate
        return obj
    def __repr__(self):
        return f'{self.__class__.__name__}({self.x}, "{self.coordinate}")'

class Height(Vector):
    def __new__(cls, y, coordinate="default"):
        obj = object.__new__(cls)
        obj.x = 0
        obj.y = y
        obj.coordinate = coordinate
        return obj
    def __repr__(self):
        return f'{self.__class__.__name__}({self.y}, "{self.coordinate}")'


@pns.paranoidclass
class MetaBinop:
    coordinate = "various"
    op_table = {'+': lambda lhs,rhs : lhs + rhs,
                '-': lambda lhs,rhs : lhs - rhs}
    @pns.accepts(pns.Self, Metric, pns.Set(['+', '-']), Metric)
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op
    def __repr__(self):
        if self.op == '-' and isinstance(self.rhs, MetaBinop):
            return f'{repr(self.lhs)} {self.op} ({repr(self.rhs)})'
        else:
            return f'{repr(self.lhs)} {self.op} {repr(self.rhs)}'
    def __eq__(self, other):
        return (self.lhs == other.lhs) and (self.op == other.op) and (self.rhs == other.rhs)

@pns.paranoidclass
class BinopPoint(MetaBinop,Point):
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

@pns.paranoidclass
class BinopVector(MetaBinop,Vector):
    def __new__(cls, lhs, op, rhs):
        if cls == BinopVector and isinstance(lhs, Width) and isinstance(rhs, Width):
            return BinopWidth(lhs, op, rhs)
        elif cls == BinopVector and isinstance(lhs, Height) and isinstance(rhs, Height):
            return BinopHeight(lhs, op, rhs)
        else:
            return object.__new__(cls)
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
        return BinopVector(self.lhs*rhs, self.op, self.rhs*rhs)
    @pns.accepts(pns.Self, pns.Number)
    def __truediv__(self, rhs):
        return BinopVector(self.lhs/rhs, self.op, self.rhs/rhs)
    def width(self):
        return self.op_table[self.op](self.lhs.width(), self.rhs.width())
    def height(self):
        return self.op_table[self.op](self.lhs.height(), self.rhs.height())
    @classmethod
    def _generate(cls):
        yield cls(Point(0, 1), '+', Point(3, 2, "absolute"))
        yield cls(Point(-.2, .2), '-', cls(Point(0, -1, "absolute"), '+', Width(2, "otherunit")))

class BinopWidth(BinopVector,Width):
    pass

class BinopHeight(BinopVector,Height):
    pass

class LegendItem:
    # Accepts the same arguments as matplotlib.lines.Line2D
    def __init__(self, text, color, **kwargs):
        self.text = text
        kwargs['color'] = color
        self.params = kwargs

@pns.paranoidclass
class Canvas:
    @pns.accepts(pns.Self, pns.Number, pns.Number, pns.Number, pns.String)
    @pns.paranoidconfig(unit_test=False)
    def __init__(self, size_x, size_y, fontsize=12, font="Helvetica Neue LT Std"):
        self.figure = plt.figure(figsize=(size_x, size_y))
        self.size = (size_x, size_y)
        self.axes = dict()
        self.units = dict()
        self.default_unit = "figure"
        self.fontsize = fontsize
        self.font = font
        self.images = []
        self.tmpfiles = []
        atexit.register(self._cleanup)
        self.localRc = {}
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
            self.__class__._fm = plt.matplotlib.font_manager.FontManager()
        fp = plt.matplotlib.font_manager.FontProperties(weight=weight, style=style, size=size, family=self.font, stretch=stretch)
        fontfile = self.__class__._fm.findfont(fp, fallback_to_default=False)
        print(fontfile, stretch, size, style, weight)
        fprops = plt.matplotlib.font_manager.FontProperties(fname=fontfile, size=size)
        return fprops
    @pns.accepts(pns.Self, pns.String, Vector, Point)
    @pns.requires('name not in self.units')
    def add_unit(self, name, scale, origin=Point(0, 0, "figure")):
        scale = self.convert_to_figure_length(scale)
        origin = self.convert_to_figure_coord(origin)
        self.units[name] = (scale.width().x, scale.height().y, origin)
    @pns.accepts(pns.Self, pns.String, Point, Point)
    @pns.requires("self.is_unit(name)")
    def set_default_unit(self, name):
        self.default_unit = name
    @pns.accepts(pns.Self, pns.String, Point, Point)
    @pns.requires("self.is_valid_identifier(name)")
    @pns.ensures("not self.is_valid_identifier(name)")
    def add_axis(self, name, pos_ll, pos_ur):
        assert name not in self.axes.keys(), "Axis name alredy exists"
        assert name != "figure", "Invalid axis name"
        pt_ll = self.convert_to_figure_coord(pos_ll)
        pt_ur = self.convert_to_figure_coord(pos_ur)
        ax = self.figure.add_axes([pt_ll.x, pt_ll.y, pt_ur.x-pt_ll.x, pt_ur.y-pt_ll.y], label=name)
        self.axes[name] = ax
        sns.despine(ax=ax)
        return ax
    @pns.accepts(pns.Self, pns.String)
    @pns.requires("name in self.axes.keys()")
    @pns.ensures("name not in self.axes.keys()")
    def delete_axis(self, name):
        self.figure.delaxes(self.ax(name))
        del self.axes[name]
    @pns.accepts(pns.Self, pns.String)
    @pns.ensures("self.valid_identifier(name)")
    def ax(self, name):
        return self.axes[name]
    @pns.accepts(pns.Self, pns.String, Point, Point, pns.Unchecked, pns.Or(pns.Tuple(pns.Number, pns.Number), plt.matplotlib.colors.Normalize))
    def add_colorbar(self, name, pos_ll, pos_ur, cmap, bounds, **kwargs):
        ax = self.add_axis(name, pos_ll, pos_ur)
        if isinstance(bounds, tuple):
            norm = plt.matplotlib.colors.Normalize(vmin=bounds[0], vmax=bounds[1])
        else:
            norm = bounds
        size = pos_ur - pos_ll
        orientation = "horizontal" if size.width().l > size.height().l else "vertical"
        colorbar = plt.matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation=orientation, **kwargs)
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
        if ident in self.units.keys():
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
            return BinopPoint.op_table[point.op](self.convert_to_figure_coord(point.lhs),
                                                 self.convert_to_figure_coord(point.rhs))
        raise ValueError("Invalid point coordinate system %s" % point.coordinate)
    @pns.accepts(pns.Self, Vector)
    @pns.returns(Vector)
    @pns.ensures("return.coordinate == 'figure'")
    def convert_to_figure_length(self, vector):
        if vector.coordinate == "figure":
            return vector
        elif isinstance(vector, BinopVector):
            return BinopVector.op_table[vector.op](self.convert_to_figure_length(vector.lhs),
                                                   self.convert_to_figure_length(vector.rhs))
        else:
            origin = Point(0, 0, vector.coordinate)
            return self.convert_to_figure_coord(origin+vector) - self.convert_to_figure_coord(origin)
    @pns.accepts(pns.Self, pns.List(Point))
    def draw_poly(self, points, **kwargs):
        np_points = np.zeros((len(points), 2))
        for i,p in enumerate(points):
            pt = self.convert_to_figure_coord(p)
            np_points[i] = [pt.x, pt.y]
        if "fill" not in kwargs.keys():
            kwargs['fill'] = False
        poly = plt.matplotlib.patches.Polygon(np_points, closed=False, transform=self.figure.transFigure, **kwargs)
        self.figure.patches.append(poly)
        plt.draw()
    @pns.accepts(pns.Self, Point, Point)
    def draw_rect(self, pos_ll, pos_ur, **kwargs):
        pt_ll = self.convert_to_figure_coord(pos_ll)
        pt_ur = self.convert_to_figure_coord(pos_ur)
        # When drawing a box you have to duplicate the last point for
        # some reason... probably a bug in matplotlib
        self.draw_poly([Point(pt_ll.x, pt_ll.y), Point(pt_ll.x, pt_ur.y), Point(pt_ur.x, pt_ur.y),
                        Point(pt_ur.x, pt_ll.y), Point(pt_ll.x, pt_ll.y), Point(pt_ll.x, pt_ll.y)], **kwargs)
    def draw_arrow(self, frm, to, arrowstyle="->,head_width=4,head_length=8", lw=2, linestyle='solid', **kwargs):
        pt_frm = self.convert_to_figure_coord(frm)
        pt_to = self.convert_to_figure_coord(to)
        pt_delta = pt_frm - pt_to
        arrow = plt.matplotlib.patches.FancyArrowPatch(tuple(pt_frm), tuple(pt_to), transform=self.figure.transFigure,
                                                       arrowstyle=arrowstyle, lw=lw, linestyle=linestyle, **kwargs)
        self.figure.patches.append(arrow)
    def add_text(self, text, pos, weight="roman", size=None, stretch="normal", **kwargs):
        if size is None:
            size = self.fontsize
        print("Adding text", text)
        kwargs = kwargs.copy()
        if 'horizontalalignment' not in kwargs:
            kwargs['horizontalalignment'] = 'center'
        if 'verticalalignment' not in kwargs:
            kwargs['verticalalignment'] = 'center'
        pt = self.convert_to_figure_coord(pos)
        # Check valid font names with plt.matplotlib.font_manager.FontManager().findfont(name)
        #self.figure.text(pt.x, pt.y, text, transform=self.figure.transFigure, fontdict={'fontname': "Helvetica Neue LT Std", "fontsize": 20})
        fprops = self._get_font(weight=weight, size=size, stretch=stretch)
        self.figure.text(pt.x, pt.y, text, transform=self.figure.transFigure,
                         fontproperties=fprops, fontsize=size, **kwargs)
        plt.draw()
    def draw_line(self, frm, to, **kwargs):
        frm = self.convert_to_figure_coord(frm)
        to = self.convert_to_figure_coord(to)
        l2d = plt.matplotlib.lines.Line2D([frm.x, to.x], [frm.y, to.y], **kwargs)
        self.figure.add_artist(l2d)
    def draw_marker(self, pos, **kwargs):
        pos = self.convert_to_figure_coord(pos)
        l2d = plt.matplotlib.lines.Line2D([pos.x], [pos.y], **kwargs)
        self.figure.add_artist(l2d)
    @pns.accepts(pns.Self, Point, pns.List(LegendItem), pns.Maybe(pns.Natural1))
    def add_legend(self, pos_tl, els, fontsize=None):
        if fontsize is None:
            fontsize = self.fontsize
        pos_tl = self.convert_to_figure_coord(pos_tl)
        assert len(els) >= 1
        # Get the text height
        fprops = self._get_font()
        t = plt.matplotlib.textpath.TextPath((0,0), "M", size=fontsize, prop=fprops)
        bb = t.get_extents().inverse_transformed(self.figure.transFigure)
        Msize = Point(bb.width, bb.height)
        print(Msize)
        self.add_unit("Msize", Vector(bb.width, bb.height, "figure"))
        # All params are in units of M width or height
        padding_top = Height(1.5, "Msize") # Space on top of figure
        padding_sep = Width(1.2, "Msize") # Separation between legend line and text
        padding_left = Width(1.5, "Msize") # Space on left of lines
        line_spacing = Height(2.2, "Msize") # Number of M heights per line height
        sym_width = Width(2, "Msize") # Width of each legend line (or symbol)
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
            self.add_text(els[i].text,
                          top_left + sym_width + padding_sep + y_offset,
                          horizontalalignment="left", size=fontsize)
            pt1 = top_left + y_offset
            pt2 = top_left + sym_width + y_offset
            # Draw the line
            params_nomarker = els[i].params.copy()
            params_nomarker['markersize'] = 0
            self.draw_line(pt1, pt2, **params_nomarker)
            # Draw the marker.  We need this in an if statement due to
            # a bug in matplotlib.
            params_noline = els[i].params.copy()
            params_noline['linestyle'] = 'None'
            self.draw_marker((pt1+pt2)/2, **params_noline)
    def fix_fonts(self):
        fprops = self._get_font()
        for ax in self.figure.axes:
            for label in ax.get_xticklabels():
                label.set_fontproperties(fprops)
            for label in ax.get_yticklabels():
                label.set_fontproperties(fprops)
            ax.set_xlabel(ax.get_xlabel(), fontproperties=fprops)
            ax.set_ylabel(ax.get_ylabel(), fontproperties=fprops)
            ax.set_title(ax.get_title(), fontproperties=fprops)
            if ax.legend_:
                for t in ax.legend_.texts:
                    t.set_fontproperties(fprops)
        # Get Helvetica for math as well
        self.localRc['mathtext.fontset'] = 'custom'
        # TODO these should refer to bold/it/etc versions of the font
        self.localRc['mathtext.rm'] = fprops.get_fontconfig_pattern()
        self.localRc['mathtext.bf'] = fprops.get_fontconfig_pattern()
        self.localRc['mathtext.it'] = fprops.get_fontconfig_pattern()
        self.localRc['mathtext.cal'] = fprops.get_fontconfig_pattern()
        self.localRc['mathtext.tt'] = fprops.get_fontconfig_pattern()
        self.localRc['mathtext.sf'] = fprops.get_fontconfig_pattern()
    def _grid_space(self, frm, to, spacing, count):
        dist = to-frm
        figsize = (dist-(count-1)*spacing)/count
        pos = []
        for i in range(0, count):
            base = frm+i*(figsize+spacing)
            pos.append((base, base+figsize))
        return pos
    @pns.accepts(pns.Self, pns.List(pns.Maybe(pns.String)), pns.Natural1, Point, Point, pns.Maybe(Width), pns.Maybe(Height), pns.Maybe(Vector), pns.Maybe(Width), pns.Maybe(Height), pns.Maybe(Vector))
    @pns.requires("int(spacing_x is not None) + int(size_x is not None) + int(spacing is not None) + int(size is not None)") # Exactly one of spacing_x, size_x, spacing, or size must be specified
    @pns.requires("int(spacing_y is not None) + int(size_y is not None) + int(spacing is not None) + int(size is not None)") # Exactly one of spacing_y, size_y, spacing, or size must be specified
    def add_grid(self, names, nrows, pos_ll, pos_ur, spacing_x=None, spacing_y=None, spacing=None, size_x=None, size_y=None, size=None):
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
            print("Spacing", spacing_x)
        if size_y is not None:
            size_y = self.convert_to_figure_length(size_y)
            if nrows > 1:
                spacing_y = ((pt_ur - pt_ll).height() - size_y * nrows)/(nrows-1)
            elif nrows == 1:
                spacing_y = size_y*0
            print("Spacing", spacing_y)
        spacing_x = self.convert_to_figure_length(spacing_x)
        spacing_y = self.convert_to_figure_length(spacing_y)
        posx = self._grid_space(pt_ll.x, pt_ur.x, spacing_x.l, ncols)
        posy = list(reversed(self._grid_space(pt_ll.y, pt_ur.y, spacing_y.l, nrows)))
        for i in range(0, len(names)):
            x = i % ncols
            y = i // ncols
            if names[i] is not None:
                self.add_axis(names[i], Point(posx[x][0], posy[y][0], "figure"), Point(posx[x][1], posy[y][1], "figure"))
    @pns.accepts(pns.Self, pns.String)
    def save(self, filename, *args, **kwargs):
        filetypes = ['png', 'pdf']
        filetype = next(ft for ft in filetypes if filename.endswith("."+ft))
        with plt.rc_context(rc=self.localRc):
            self.figure.savefig(filename, *args, **kwargs)
        if filetype == "png":
            with PIL.Image.open(filename) as img:
                img.convert('RGBA')
                for image in self.images:
                    with PIL.Image.open(image[0]) as subimg:
                        subimg.convert('RGBA')
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
                page.insertImage(rect, filename=image[0], keep_proportion=False)
            pdf.saveIncr()
            pdf.close()
    def add_image(self, filename, pos, height=None, width=None, horizontalalignment="center", verticalalignment="center"):
        pos_ll = self.convert_to_figure_coord(pos)
        assert height is not None or width is not None, "Either height or width must be given"
        with PIL.Image.open(filename) as img:
            imwidth = img.size[0]
            imheight = img.size[1]
        if width is None:
            height = self.convert_to_figure_length(height)
            width = Width(height.l * (imwidth/imheight), "figure")
        elif height is None:
            width = self.convert_to_figure_length(width)
            height = Height(width.l * (imheight/imwidth), "figure")
        else:
            height = self.convert_to_figure_length(height)
            width = self.convert_to_figure_length(width)
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
        filetypes = ["png", "jpg", "jpeg", "gif"]
        assert any(ft for ft in filetypes if filename.endswith("."+ft))
        self.images.append((filename, pos_ll, pos_ur))
    def show(self):
        tmp = tempfile.mkstemp('.png')[1]
        self.tmpfiles.append(tmp)
        self.save(tmp)
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
