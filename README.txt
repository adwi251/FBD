Assumptions:
    If an instance of the Vec class is created using the (magnitude,angle) convention, it is assumed that the angle is measured in relation to the 
    +x-axis.


Classes:
    Vec
    @properties
        vec: A numpy array of shape (3,) which represents a vector in coordinate form (x,y,z)

        magnitude: Equavalent to sqrt(x^2 + y^2 + z^2)

        angle: The orientation of the vector with respect to the +x-axis. The angles should only have positive values

        quadrant: The quadrant of the coordinate plane that the vectors lie in. The quadrants are defined as follows:
                    I: [0 degrees, 90 degrees) 
                    II: [90 deg, 180 deg)
                    III: [180 deg, 270 deg)
                    IV: [270 deg, 0/360 deg)

    @methods
        # Initializes the vec, magnitude, and angle properties described above. The listed parameters are not required to initialize an instance. This is
          to allow for the initialization of vectors in component form (x,y,z) or (magnitude,angle) form. Depending on which convention is used, The
          location of the vector in terms of quadrants will be set accordingly. See above explanation of the quadrant property
        __init__(vec, magnitude, angle)
    
    VecCollec
    @properties
        arr: A list containing instances of the Vec class

        numVecs: The number of Vecs stored in the arr property

        xScale: The values of the vectors coordinates are scaled down to fit on the canvas. This holds the scale of the x-components

        yScale: See above explanation for xScale. This holds the scale of the y-components

    @methods
        # Initializes the arr and numVecs properties. Calculates the scaling needed for x and y-components and sets the values of their respective
          properties accordingly
        __init__(arr)