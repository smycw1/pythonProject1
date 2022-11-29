from csv import reader
# Input the data.csv by using numpy
import numpy as np
filename = '/Users/vchao/Downloads/0097 assignment/input.csv'
with open(filename, 'rt') as raw_data:
    data = np.loadtxt(raw_data, delimiter=',')
#input data
data_x = data[:, 1] #select x column
data_y = data[:, 2] #select y column

# create a list with all input points.

i = 1
list_data = [data_x[0], data_y[0]]
while i < 100:
    list_data.append([data_x[i], data_y[i]])
    i += 1

# Input the polygon vertex point
polygon_filename = '/Users/vchao/Downloads/0097 assignment/polygon.csv'
with open(polygon_filename, 'rt') as raw_data:
    polygon_data = np.loadtxt(raw_data, delimiter=',')

# select the x,y column in polygon_data
polygon_data_x = polygon_data[:, 1]
polygon_data_y = polygon_data[:, 2]

# create geometry class
class Geometry:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name


# create point class
class Point(Geometry):
    def __init__(self, name, x, y):
        super().__init__(name)
        self.__x = x
        self.__y = y
    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y


# create line class with another two function 'get_point': In order to pick the endpoint of the line
class Line(Geometry):
    def __init__(self, name, point_1, point_2):
        super().__init__(name)
        self.__point_1 = point_1
        self.__point_2 = point_2

    def get_point_1(self):
        return self.__point_1

    def get_point_2(self):
        return self.__point_2


from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')


# create a plot class in order to plot the points and the polygon
class Plotter:
    def __init__(self):
            plt.figure()

    def add_polygon(self, xs, ys):
            plt.fill(xs, ys, 'lightgray', label='Polygon')

    def add_point(self, x, y, kind=None):
        if kind == 'outside':
                plt.plot(x, y, 'ro', label='Outside')
        elif kind == 'boundary':
                plt.plot(x, y, 'bo', label='Boundary')
        elif kind == 'inside':
                plt.plot(x, y, 'go', label='Inside')
        else:
                plt.plot(x, y, 'ko', label='Unclassified')



# add-MBR is to plot the minimum rectangle of the polygon
    def add_MBR(self, x_max, x_min, y_max, y_min):
            plt.plot([x_min, x_max, x_max, x_min, x_min], [y_min, y_min, y_max, y_max, y_min])


    def show(self):
            handles, labels = plt.gca().get_legend_handles_labels()
            by_label = OrderedDict(zip(labels, handles))
            plt.legend(by_label.values(), by_label.keys())
            plt.show()

list_point = []
list_polygon = []
list_unclassified = []
# make each input point as in point class
for i in range(100) :
    A = Point(data[i,0],data[i,1],data[i,2])
    list_point.append(A)
    # make each vertex of input polygon in point class
for i in range(20):
    B = Point(polygon_data[i, 0], polygon_data[i, 1],polygon_data[i, 2])
    list_polygon.append(B)
# calculate the max and min value of the polygon vertex coordinate
x_max = max(polygon_data_x)
x_min = min(polygon_data_x)
y_max = max(polygon_data_y)
y_min = min(polygon_data_y)


    # plot the figure with input points, polygon, and Minimum boundary rectangle
plotter = Plotter()
plotter.add_polygon(polygon_data_x, polygon_data_y)
plotter.add_MBR(x_max, x_min, y_max, y_min)

    # following are specific step to plot each point with classification by using minimum boundary rectangle method.
kind = 'k'
for i in range(len(data)):
    if data[i, 1] > x_max or data[i, 1] < x_min:
        kind = 'outside'
        print(data[i, 0], 'outside')
        plotter.add_point(data[i, 1], data[i, 2], kind)

    elif data[i, 2] > y_max or data[i, 2] < y_min:
        kind = 'outside'
        plotter.add_point(data[i, 1], data[i, 2], kind)
        print(data[i, 0], 'outside')
    else:
        kind = 'unclassified'
        print(data[i, 0], 'unclassified')
        plotter.add_point(data[i, 1], data[i, 2], kind)
        list_unclassified.append([data[i, 0], data[i, 1], data[i, 2]])
plotter.show


class Polygon(Geometry):
    def __init__(self, name, points):
        super().__init__(name)
        self.__points = points

    def get_points(self):
        return self.__points

    def lines(self):
        res = []
        points = self.get_points()
        for point_b in points[1:]:
            res.append(Line(point_a.get_name() + '-' + point_b.get_name(), point_a, point_b))
            point_a = point_b
        res.appennd(Line(point_a.get_name() + '-' + points[0].get_name(), point_a, points[0]))
        return res

    def count(self, test_point, polygon_vertex):
        plotter = Plotter()
        kind = ''
        polygon_vertex = tuple(polygon_vertex[:])+(polygon_vertex[0],)
        for l in range(len(test_point)-1):
            count_number = 0
            for k in range(len(polygon_vertex)-1):
                fp = (polygon_vertex[k + 1][1] - polygon_vertex[k][1]) * (test_point[l][2] - polygon_vertex[k][2]) - (test_point[l][1] - polygon_vertex[k][1]) * (polygon_vertex[k + 1][2] - polygon_vertex[k][2])
                if fp == 0 and (test_point[l][2] <= polygon_vertex[k + 1][2] or test_point[l][2] <= polygon_vertex[k][2]) and (test_point[l][2] >= polygon_vertex[k + 1][2] or test_point[l][2] >= polygon_vertex[k][2]) and (test_point[l][1] <= polygon_vertex[k + 1][1] or test_point[l][1] <= polygon_vertex[k][1]) and(test_point[l][1] >= polygon_vertex[k + 1][1] or test_point[l][1] >= polygon_vertex[k][1]):
                    kind = 'boundary'
                    print(test_point[l][0], 'boundary')
                    plotter.add_point(test_point[l][1], test_point[l][2], kind)
                    count_number = -1
                    break
                elif((polygon_vertex[k][2] <= test_point[l][2] < polygon_vertex[k + 1][2])
                     or (polygon_vertex[k][2] > test_point[l][2] >= polygon_vertex[k + 1][2])):
                    kt = (test_point[l][2] - polygon_vertex[k][2]) / float((polygon_vertex[k + 1][2] - polygon_vertex[k][2]))
                    if test_point[l][1] < polygon_vertex[k][1]+kt * (polygon_vertex[k + 1][1] - polygon_vertex[k][1]):
                        count_number += 1
            if count_number % 2 == 0:
                print(test_point[l][0], 'outside')
                kind = 'outside'
                plotter.add_point(test_point[l][1], test_point[l][2], kind)
            if count_number == -1:
                kind = 'boundary'
                plotter.add_point(test_point[l][1], test_point[l][2], kind)
            elif count_number % 2 == 1:
                print(test_point[l][0], 'inside')
                kind = 'inside'
                plotter.add_point(test_point[l][1], test_point[l][2], kind)

RCA = Polygon('A', polygon_data)
RCA.count(list_point, polygon_data)

plotter.add_polygon(polygon_data_x, polygon_data_y)
plotter.add_MBR(x_max, x_min, y_max, y_min)
plotter.show()























