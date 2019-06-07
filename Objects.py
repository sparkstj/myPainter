from PIL import Image, ImageDraw
class Objects:
    obList = [[]]
    xyList = [[]]
    missionList = []
    ObjectId = -1
    brushColor = "#000000"
    image = Image.new("RGB",(500,150),(255,255,255))