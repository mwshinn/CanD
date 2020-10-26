import paranoid as pns
import math

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
        """Add together a point and a vector.

        `other` should be a Vector, otherwise this function will throw an error.

        Returns a Point
        """
        if isinstance(other, Vector):
            if self.coordinate == other.coordinate and self.coordinate != "various":
                return Point(self.x + other.x, self.y + other.y, self.coordinate)
            else:
                return BinopPoint(self, '+', other)
        raise ValueError(f"Invalid addition between {self!r} and {other!r}.")
    @pns.accepts(pns.Self, Metric)
    def __sub__(self, other):
        """Find the vector which connects two points.

        `other` should be a Point, otherwise this function will throw an error.

        Returns a Vector.
        """
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
        raise ValueError(f"Invalid subtraction between {self!r} and {other!r}.")
    def __eq__(self, other):
        """Determine if two Point objects are equal.  

        `other` should be another Point object.

        Returns True or False.
        """
        return (self.x == other.x) and (self.y == other.y) and (self.coordinate == other.coordinate)
    def __iter__(self):
        yield self.x
        yield self.y
    def __rshift__(self, other):
        """Take the x coordinate of this point and the y coordinate of another point.

        `other` should be a Point, otherwise this function will throw an error.

        Returns a Point.
        """
        if not isinstance(other, Point):
            raise ValueError(f"Invalid meet >> operation between {self!r} and {other!r}.")
        if self.coordinate == other.coordinate:
            return Point(self.x, other.y, self.coordinate)
        else:
            return BinopPoint(self, '>>', other)
    def __lshift__(self, other):
        """Take the y coordinate of this point and the x coordinate of another point.

        `other` should be a Point, otherwise this function will throw an error.

        Returns a Point.
        """
        return other >> self
    def __or__(self, other):
        """Return the point in the center of the two given points

        `other` should be a Point, otherwise this function will throw an error.

        Returns a Point.
        """
        if not isinstance(other, Point):
            raise ValueError(f"Invalid mean | operation between {self!r} and {other!r}.")
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
        """Add a vector to a Point or another Vector.

        If `other` is a Point, return a Point.  If `other` is a Vector, return a Vector.
        """
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
        """Vector subtraction.

        `other` should be a Vector.  

        Return a Vector.

        Subtracting a vector is equivalent to adding the negative of the vector.
        """
        if self.coordinate == other.coordinate:
            return Vector(self.x - other.x, self.y - other.y, self.coordinate)
        else:
            return BinopVector(self, '-', other)
    @pns.accepts(pns.Self, pns.Number)
    def __mul__(self, other):
        """Multiply a vector by a scalar.

        `other` should be a scalar by which to multiply each component of the vector.

        Return a Vector.
        """
        return Vector(self.x * other, self.y * other, self.coordinate)
    @pns.accepts(pns.Self, pns.Number)
    def __rmul__(self, other):
        self.__mul__.__doc__
        return self * other
    @pns.accepts(pns.Self)
    def __neg__(self):
        """Take the negative of a vector.

        This is equivalent to rotating the vector by 180 degrees, or
        to multiplying each component by -1.

        Return a Vector.
        """
        return -1* self
    @pns.accepts(pns.Self, pns.Number)
    @pns.requires("other != 0")
    def __truediv__(self, other):
        """Divide a vector by a scalar.

        `other` should be a non-zero scalar by which to divide each component of the vector.

        Return a Vector.
        """
        return Vector(self.x / other, self.y / other, self.coordinate)
    @pns.accepts(pns.Self, pns.Self)
    def __rshift__(self, other):
        """Take the x coordinate of this vector and the y coordinate of another vector.

        `other` should be a Vector, otherwise this function will throw an error.

        Returns a Vector.
        """
        if not isinstance(other, Vector):
            raise ValueError(f"Invalid meet >> operation between {repr(self)} and {repr(other)}.")
        if self.coordinate == other.coordinate:
            return Vector(self.x, other.y, self.coordinate)
        else:
            return BinopVector(self, '>>', other)
    @pns.accepts(pns.Self, pns.Self)
    def __lshift__(self, other):
        """Take the y coordinate of this vector and the x coordinate of another vector.

        `other` should be a Vector, otherwise this function will throw an error.

        Returns a Vector.
        """
        return other >> self
    @pns.accepts(pns.Self, pns.Number)
    def __matmul__(self, other):
        """Rotate the vector by some amount, specified in degrees.

        `other` should be a scalar, in units of degrees.

        Returns a Vector.
        """
        if self.coordinate == "absolute":
            c = math.cos(math.radians(other))
            s = math.sin(math.radians(other))
            return Vector(self.x * c - self.y * s ,
                          self.x * s + self.y * c,
                          self.coordinate)
        else:
            return BinopVector(self, '@', other)
    @pns.accepts(pns.Self, pns.Number)
    def __rmatmul__(self, other):
        self.__matmul__.__doc__
        return self @ other
    @pns.accepts(pns.Self)
    def width(self):
        """Returns a Width object representing the x component of the Vector."""
        return Width(self.x, self.coordinate)
    @pns.accepts(pns.Self)
    def height(self):
        """Returns a Height object representing the y component of the Vector."""
        return Height(self.y, self.coordinate)
    @pns.accepts(pns.Self)
    def flipx(self):
        """Returns a Vector reflected across the y-axis."""
        return Vector(-self.x, self.y, self.coordinate)
    @pns.accepts(pns.Self)
    def flipy(self):
        """Returns a Vector reflected across the x-axis."""
        return Vector(self.x, -self.y, self.coordinate)
    @pns.accepts(pns.Self, pns.Self)
    def __eq__(self, other):
        """Determine if two Vector objects are equal.  

        `other` should be another Vector object.

        Returns True or False.
        """
        return (self.x == other.x) and (self.y == other.y) and (self.coordinate == other.coordinate)
    def __iter__(self):
        yield self.x
        yield self.y
    @classmethod
    def _generate(cls):
        yield Height(.3)
        yield Width(.5)

def Width(x, coordinate="default"):
    """A vector with a 0 in the y coordinate.

    Returns a Vector with `x` in the x coordinate and 0 in the y
    coordinate, within the coordinate system `coordinate`.

    This is included for backward compatibility.
    """
    return Vector(x, 0, coordinate)

def Height(y, coordinate="default"):
    """A vector with a 0 in the x coordinate.

    Returns a Vector with 0 in the x coordinate and `y` in the y
    coordinate, within the coordinate system `coordinate`.

    This is included for backward compatibility.
    """
    return Vector(0, y, coordinate)

@pns.paranoidclass
class MetaBinop:
    coordinate = "various"
    op_table = {'+': lambda lhs,rhs : lhs + rhs,
                '-': lambda lhs,rhs : lhs - rhs,
                '*': lambda lhs,rhs : lhs * rhs,
                '/': lambda lhs,rhs : lhs / rhs,
                '>>': lambda lhs,rhs : lhs >> rhs,
                '|': lambda lhs,rhs : lhs | rhs,
                '@': lambda lhs,rhs : lhs @ rhs}
    @pns.accepts(pns.Unchecked, pns.Or(Metric, pns.Number), pns.Set(['+', '-', '*', '/', '>>', '|', '@']), pns.Or(Metric, pns.Number))
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
    @pns.accepts(pns.Self, pns.Number)
    def __matmul__(self, rhs):
        return BinopVector(self, '@', rhs)
    def __rmatmul__(self, rhs):
        rhs @ self
    def width(self):
        """Returns a BinopVector object representing the x component of the Vector."""
        # Handle cases where we use a scalar instead of a vector
        return ((Point(0, 0, "absolute") + self) >> Point(0, 0, "absolute")) - Point(0, 0, "absolute")
    def height(self):
        """Returns a BionpVector object representing the y component of the Vector."""
        return ((Point(0, 0, "absolute") + self) << Point(0, 0, "absolute")) - Point(0, 0, "absolute")
    def flipx(self):
        return (-self) >> self
    def flipy(self):
        return self >> (-self)
    @classmethod
    def _generate(cls):
        yield cls(Point(0, 1), '+', Point(3, 2, "absolute"))
        yield cls(Point(-.2, .2), '-', cls(Point(0, -1, "absolute"), '+', Width(2, "otherunit")))
