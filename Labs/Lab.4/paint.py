
import math

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]
    
    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]
    
    def v_line(self, x, y, w, **kargs):
        for i in range(x,x+w):
            self.set_pixel(i,y, **kargs)

    def h_line(self, x, y, h, **kargs):
        for i in range(y,y+h):
            self.set_pixel(x,i, **kargs)
            
    def line(self, x1, y1, x2, y2, **kargs):
        slope = (y2-y1) / (x2-x1)
        for y in range(y1,y2):
            x = int(slope * y)
            self.set_pixel(x,y, **kargs)
            
    def display(self):
        print("\n".join(["".join(row) for row in self.data]))


class shape:
    def __init__(self, name=""):
        self.name = name

    def paint(self, canvas):
        raise NotImplementedError


class rectangle(shape):
    def __init__(self, length, width, x, y, name=""):
        shape.__init__(self, name)

        self.__length = length
        self.__width = width
        self.__x = x
        self.__y = y

    def __repr__(self):
        return "rectangle(" +            repr(self.__length) + "," +            repr(self.__width) + "," +            repr(self.__x) + "," +            repr(self.__y) + "," +            repr(self.name) + ")"
        
    def paint(self, canvas):
        canvas.h_line(self.__x, self.__y, self.__width)
        canvas.h_line(self.__x + self.__length, self.__y, self.__width)

        canvas.v_line(self.__x, self.__y, self.__length)
        canvas.v_line(self.__x, self.__y + self.__width, self.__length)


class circle(shape):
    def __init__(self, radius, x, y, name=""):
        shape.__init__(self, name)

        self.__radius = radius
        self.__x = x
        self.__y = y

    def __repr__(self):
        return "circle(" +            repr(self.__radius) + "," +            repr(self.__x) + "," +            repr(self.__y) + "," +            repr(self.name) + ")"

    def perimeter_points(self):
        points = []

        for i in range(16):
            angle = 2 * math.pi * i / 16

            x_point = self.__x + self.__radius * math.cos(angle)
            y_point = self.__y + self.__radius * math.sin(angle)

            points.append((x_point, y_point))

        return points

    def paint(self, canvas):
        points = self.perimeter_points()

        for point in points:
            canvas.set_pixel(int(point[0]), int(point[1]))


class triangle(shape):
    def __init__(self, base, height, side2, side3, x, y, name=""):
        shape.__init__(self, name)

        self.__base = base
        self.__height = height
        self.__side2 = side2
        self.__side3 = side3
        self.__x = x
        self.__y = y

    def __repr__(self):
        return "triangle(" +            repr(self.__base) + "," +            repr(self.__height) + "," +            repr(self.__side2) + "," +            repr(self.__side3) + "," +            repr(self.__x) + "," +            repr(self.__y) + "," +            repr(self.name) + ")"

    def perimeter_points(self):
        points = []

        points.append((self.__x, self.__y))
        points.append((self.__x + self.__base, self.__y))
        points.append((self.__x, self.__y + self.__height))

        return points

    def paint(self, canvas):
        points = self.perimeter_points()

        for point in points:
            canvas.set_pixel(int(point[0]), int(point[1]))


class CompoundShape(shape):
    def __init__(self, shapes, name=""):
        shape.__init__(self, name)
        self.shapes = shapes

    def paint(self, canvas):
        for shape in self.shapes:
            shape.paint(canvas)


class RasterDrawing:
    def __init__(self, shapes=None):
        self.shapes = dict()
        self.shape_names = list()

        if shapes != None:
            for shape in shapes:
                self.add_shape(shape)

    def add_shape(self, shape):
        if shape.name == "":
            shape.name = self.assign_name()

        self.shapes[shape.name] = shape
        self.shape_names.append(shape.name)

    def paint(self, canvas):
        for shape_name in self.shape_names:
            self.shapes[shape_name].paint(canvas)

    def update(self, canvas):
        canvas.clear_canvas()
        self.paint(canvas)

    def assign_name(self):
        name_base = "shape"
        name = name_base + "_0"

        i = 1

        while name in self.shapes:
            name = name_base + "_" + str(i)
            i += 1

        return name

    def __repr__(self):
        shapes_list = []

        for shape_name in self.shape_names:
            shapes_list.append(self.shapes[shape_name])

        return "RasterDrawing(" + repr(shapes_list) + ")"

    def save(self, filename):
        f = open(filename, "w")
        f.write(self.__repr__())
        f.close()


def load_drawing(filename):
    f = open(filename, "r")
    drawing = eval(f.read())
    f.close()

    return drawing
            
