import algorithms
import re
from Objects import Objects


def cmd(f_addr):
    f = open(f_addr, "r")
    line = f.readline()
    while line:
        wordlist = re.split('\s+', line)
        if wordlist[0] == "resetCanvas":
            algorithms.resetCanvas(int(wordlist[1]),int(wordlist[2]),None)
        elif wordlist[0] == "saveCanvas":
            algorithms.saveCanvas(wordlist[1],None)
        elif wordlist[0] == "setColor":
            algorithms.setColor(int(wordlist[1]), int(wordlist[2]), int(wordlist[3]), None)
        elif wordlist[0] == "drawLine":
            p1 = int(wordlist[2]), Objects.height - int(wordlist[3])
            p2 = int(wordlist[4]), Objects.height - int(wordlist[5])
            algorithms.drawLine(int(wordlist[1]), p1, p2, wordlist[6], None, Objects.brushColor)
        elif wordlist[0] == "drawPolygon":
            param = f.readline()
            vertices = re.split("\s", param)
            vertices.pop()
            for i in range(len(vertices)):
                vertices[i] = int(vertices[i])
            for i in range(int(len(vertices)/2)):
                x = vertices.pop(0)
                y = Objects.height - vertices.pop(0)
                vertices.append((x,y))
            #vertices.append(vertices[0])
            algorithms.drawPolygon(int(wordlist[1]), vertices, wordlist[3], None, Objects.brushColor)
        elif wordlist[0] == "drawEllipse":
            center = (int(wordlist[2]), Objects.height - int(wordlist[3]))
            r = (int(wordlist[4]), int(wordlist[5]))
            algorithms.drawEllipse(int(wordlist[1]), center, r, None, wordlist[6], Objects.brushColor)
        elif wordlist[0] == "drawCurve":
            param = f.readline()
            points = re.split("\s", param)
            points.pop()
            for i in range(len(points)):
                points[i] = int(points[i])
            for i in range(int(len(points)/2)):
                x = points.pop(0)
                y = Objects.height - points.pop(0)
                points.append((x,y))
            algorithms.drawCurve(int(wordlist[1]), points, wordlist[3], None, Objects.brushColor)
        elif wordlist[0] == "translate":
            d = float(wordlist[2]), -float(wordlist[3])
            algorithms.translate(int(wordlist[1]), d, None)
        elif wordlist[0] == "rotate":
            center = int(wordlist[2]),  Objects.height - int(wordlist[3])
            algorithms.rotate(int(wordlist[1]), center, 3.14*float(wordlist[4])/180, None)
        elif wordlist[0] == "scale":
            center = int(wordlist[2]), Objects.height - int(wordlist[3])
            algorithms.scale(int(wordlist[1]), center, float(wordlist[4]), None)
        elif wordlist[0] == "clip":
            p1 = int(wordlist[2]), Objects.height - int(wordlist[5])
            p2 = int(wordlist[4]), Objects.height - int(wordlist[3])
            algorithms.clip(int(wordlist[1]), p1, p2, wordlist[6], None)
        line = f.readline()
