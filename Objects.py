from PIL import Image, ImageDraw
class Objects:
    obList = [[]]
    xyList = [[]]
    missionList = []
    idList = []
    ObjectId = -1
    brushColor = "#000000"
    width = 500
    height = 150
    image = Image.new("RGB",(500,150),(255,255,255))