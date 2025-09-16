import sys
import numpy as np
from manim import *
#manim -pqp ./Projects/FBDtest.py FBD "./Projects/FBDarrows.txt"

# change config for numberplane
# default values for x-axis and y-axis range are [-7.11, 7,11] and [-4,4], respectively
# this is, in my professional opinion, very dumb, so let's change that to [-10,10] for both
config.frame_x_radius = 10.0
config.frame_y_radius = 10.0

# find the order of magnitude of some inserted value
def orderMagnitude(n):
    if n == 0:
        return 0
    return 10 ** int(np.floor(np.log10(abs(n))))

# scale the vectors and return the scales
def scaleArrows(arr):
    # find the max value for each coordinate
    xMax = np.max(arr[:,0])
    yMax = np.max(arr[:,1])

    # find the order of magnitude for the max
    xMag = orderMagnitude(xMax)
    yMag = orderMagnitude(yMax)

    # prevents the scaling of values if the max value is a factor of 10 (10, 100, 1000, ...)
    if xMag == xMax:
        xMag /= 10
    if yMag == yMax:
        yMag /= 10

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if j == 0:
                arr[i][j] = arr[i][j]/xMag
            elif j == 1:
                arr[i][j] = arr[i][j]/yMag
            else:
                continue

    return xMag,yMag

# find the magnitude of a vector with 3 dimensions
def pythag(vec,decimal = 2):
    return np.round(np.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2),decimal)

# determine where to place text for arrows
def textPlacement(vec):
    if vec[0] < 0:
        #return LEFT
        return np.array([0.,1.,0.])
    else:
        return RIGHT



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

    arrows.append(currArrow)

#get the number of arrows to be displayed
if (len(arrows)) != numArrows:
    print(f"Actual number of arrows does not match with the first line of {filePath}")
    sys.exit()

# convert the list of arrows into a numpy array
arrows = np.array(arrows, dtype=float)

# scale the arrows and return the scale
xScale, yScale = scaleArrows(arrows)


# can change the name of the class to anything
class FBD(Scene):
    def construct(self):
        # set up coordinate plane
        dot = Dot(ORIGIN)
        numberplane = NumberPlane(x_length=5, y_length=5, background_line_style={"stroke_opacity": 0.0})
        self.add(numberplane, dot)

        # add all the arrows to the diagram
        for i in range(numArrows):
            currArrow = arrows[i]
            
            F = Arrow(ORIGIN, currArrow, buff=0)
            self.add(F)

            # scale the arrow back up
            currArrow[0] = currArrow[0]*xScale
            currArrow[1] = currArrow[1]*yScale

            # get magnitude of vector
            arrowMag = pythag(currArrow)

            self.add(MathTex(f"F_{{{i}}} = {arrowMag} \, N", font_size=32).next_to(F.get_end(), textPlacement(currArrow)))
