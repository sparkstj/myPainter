from PIL import Image, ImageDraw
class Objects:
    obList = [[]]
    xyList = [[]]
    missionList = []
    ObjectId = -1
    brushColor = "#000000"
    width = 1120
    height = 400
    image = Image.new("RGB",(width,height),(255,255,255))