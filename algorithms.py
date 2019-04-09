
def resetCanvas(width, height):
    '''clean the current canvas, reset canvas width and height, 
    width, height: int, 100 <= width, height <= 1000
    '''

def saveCanvas(name):
    '''save current canvas as name.bmp, 
    name: string
    '''

def setColor(R,G,B):
    '''set brush color, 
    0 <= R, G, B <= 255
    '''

def drawLine(id, p1, p2, algorithm):
    ''' id: unique identity for each primitive
     p1, p2: float tuples, denote the startpoint and endpoint coordinates
     algorithm: string, denotes drawing algorithm, eg:DDA or bresenham
     '''

def drawPolygon(id, n, vertices, algorithm):
    ''' id: unique identity for each primitive
    n: number of vertices
    vertices: list of float tuples, denotes the polygon vertices
    algorithm: string, denotes drawing algorithm
    '''

def drawEllipse(id, center, r):
    ''' id: unique identity for each primitive
    center: float tuple, denotes the center's coordinate
    r: float tuple, (major semi-axis, minor semi-axis)
    '''

def drawCurve(id, n, points, algorithm):
    ''' id: unique identity for each primitive
    n: int, number of points observed on the curve
    points: list of float tuples, denotes n observed points coordinate
    algorithm: string, denotes drawing algorithm
    '''

def translate(id, d):
    ''' id: unique identity for each primitive
    d: float tuple, denotes the translation vector
    '''

def rotate(id, center, r):
    ''' id: unique identity for each primitive
    center = (x, y): float tuple, denotes the rotation center coordinate
    r: float, the angle of clockwise rotation
    '''

def scale(id, center, s);
    ''' id: unique identity for each primitive
    center = (x,y): float tuple, denotes the coordinate of scaling center
    s: float, denotes scale of scaling
    '''

def clip(id, p1, p2, algorithm):
    ''' id: unique identity for each primitive
    p1, p2: float tuples, denote up-left and down-right coordinate of target window
    algorithm: string, denotes the clipping algorithm.
    '''
