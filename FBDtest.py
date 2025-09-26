import sys
import numpy as np
from manim import *
#uv run manim checkhealth
#manim -pqp ./Projects/FBDtest.py FBD "./Projects/FBDarrows.txt"

# change config for numberplane
# default values for x-axis and y-axis range are [-7.11, 7,11] and [-4,4], respectively
# this is, in my professional opinion, very dumb, so let's change that to [-20,20] for both
config.frame_x_radius = 20.0
config.frame_y_radius = 20.0


# define class for collection of vectors
class VecCollec:
    # constructor for vector collection class
    def __init__(self, arr):
        self.arr = arr
        self.numVecs = len(arr)
        
        # find the max x and y values
        xMax = self.arr[0].vec[0]
        yMax = self.arr[0].vec[1]

        for i in range(1, self.numVecs):
            if abs(self.arr[i].vec[0]) > xMax:
                xMax = self.arr[i].vec[0]
            if abs(self.arr[i].vec[1]) > yMax:
                yMax = self.arr[i].vec[1]

         # find the order of magnitude for the max
        xMag = orderMagnitude(xMax)
        yMag = orderMagnitude(yMax)

        # prevents the scaling of values if the max value is a factor of 10 (10, 100, 1000, ...)
        if xMag == xMax:
            xMag /= 10
        if yMag == yMax:
            yMag /= 10

        for i in range(self.numVecs):
            for j in range(3):
                if j == 0:
                    arr[i].vec[j] = arr[i].vec[j]/xMag
                elif j == 1:
                    arr[i].vec[j] = arr[i].vec[j]/yMag
                else:
                    continue
        
        # add scale properties
        self.xScale = xMag
        self.yScale = yMag

        # 

        
# define class for vectors
class Vec:
    # constructor for vector class
    def __init__(self, vec=None, magnitude=None, angle=None):
        self.vec = np.array(vec, dtype=float)       # x,y,z-components of the vector
        self.magnitude = magnitude                  # magnitude of the vector, pythag(vec)
        self.angle = angle                          # angle of the vector w.r.t +x-axis

        # create a quadrant property to be assigned a value in the following block
        self.quadrant = None

        # check to see if magnitude is type none
        if magnitude is None:
            # find the magnitude
            self.magnitude = pythag(self.vec, decimal=5)

            # before calculating angle, check for x-values of 0
            if self.vec[0] == 0:
                if self.vec[1] > 0:
                    self.angle = 90
                elif self.vec[1] < 0:
                    self.angle = 180
                else:
                    print(f"Arrow {self.vec} is not a vector. At least one component must be nonzero")
                    sys.exit()
            # if x-component is not zero
            else:
                self.angle = np.atan(self.vec[1]/self.vec[0])*(180/(np.pi))

            # ADD QUADRANT
            if self.vec[0] > 0.0 and self.vec[1] >= 0.0:
                self.quadrant = 1
            elif self.vec[0] <= 0.0 and self.vec[1] > 0.0:
                self.quadrant = 2
            elif self.vec[0] < 0.0 and self.vec[1] <= 0.0:
                self.quadrant = 3
            else:
                self.quadrant = 4

            # use the quadrant to modify the angle property
            if self.quadrant == 2 or self.quadrant == 3:
                self.angle += 180
            elif self.quadrant == 4:
                self.angle += 360
        # if magnitude is not none, populate the vec value instead
        else:
            # NOTE: this assumes that z = 0
            self.vec = np.array(self.magnitude*[np.cos(self.angle), np.sin(self.angle), 0], dtype=float)

            # assume angle measurement is in relation to +x-axis and is in degrees
            if (self.angle >= 0.0) and (self.angle < 90.0):
                self.quadrant = 1
            elif (self.angle >= 90.0) and (self.angle < 180.0):
                self.quadrant = 2
            elif (self.angle >= 180.0) and (self.angle < 270.0):
                self.quadrant = 3
            else:
                self.quadrant = 4



# find the order of magnitude of some inserted value
def orderMagnitude(n):
    if n == 0:
        return 0
    return 10 ** int(np.floor(np.log10(abs(n))))

# find the magnitude of a vector with 3 dimensions
def pythag(vec,decimal = 2):
    return np.round(np.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2),decimal)


# read in arguments
filePath = sys.argv[-1]
with open(filePath, "r") as f:
    lines = f.read().splitlines()

# first line is the number of arrows
# NOTE: idk if this is is needed, I'm just keeping it in case
numArrows = int(lines[0])

# add the rest of the arrows to a list
arrows = []
for line in lines[1:]:
    currArrow = eval(line)
    # verify that there are at least two elements of the arrow list (corresponding to the x and y coords)
    if len(currArrow) < 2:
        print(f"Arrow {line} missing at least one of coordinate points")
        sys.exit()
    # if the current arrow only has two coords, add a zero to the end to work with the Arrow() class
    elif len(currArrow) == 2:
        currArrow.append(0)

    # if the arrow passed all the tests, add it to the vector class and append it to the arrows array
    currArrow = Vec(vec=currArrow)
    arrows.append(currArrow)

# add the arrows to the VecCollec class
arrows = VecCollec(arr=arrows)

#get the number of arrows to be displayed
if (arrows.numVecs) != numArrows:
    print(f"Actual number of arrows does not match with the first line of {filePath}")
    sys.exit()


# can change the name of the class to anything
class FBD(Scene):
    def construct(self):
        # set up coordinate plane
        dot = Dot(ORIGIN)
        numberplane = NumberPlane(x_length=8, y_length=8, background_line_style={"stroke_opacity": 0.0})
        self.add(numberplane, dot)

        # add all the arrows to the diagram
        for i in range(numArrows):
            # pull current arrow from VecCollec instance
            currArrow = (arrows.arr[i])
            
            # create arrow mobject from instance of Vec and add it to the scene
            F = Arrow(ORIGIN, currArrow.vec, stroke_width=10, buff=0, max_stroke_width_to_length_ratio=10)
            self.add(F)

            self.add(MathTex(f"F_{{{i}}} = {round(currArrow.magnitude,2)} \, N", font_size=48).next_to(F.get_end(), RIGHT))
