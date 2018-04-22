from time import sleep
import numpy as np
import cv2
import sys
import time
import pdb

class ParkingSpace:
    def __init__(self, parkingDictionary):
        pointCoordinateKeysToCheck = ["topLeft", "topRight", "bottomRight", "bottomLeft"]
        coordinateKeysToCheck = ["x1", "x2", "y1", "y2"]
        # This checks if the data.json follows an 8 point system
        is8Point = all(key in parkingDictionary for key in pointCoordinateKeysToCheck)
        isCoordinates = all(key in parkingDictionary for key in coordinateKeysToCheck)
        # If it follows an 8 point coordinate system, then the coordinates get set regularly
        if (is8Point):
            self.topLeft = parkingDictionary["topLeft"]
            self.topRight = parkingDictionary["topRight"]
            self.bottomRight = parkingDictionary["bottomRight"]
            self.bottomLeft = parkingDictionary["bottomLeft"]
        # If not, then the coordinates get set programatically
        elif (isCoordinates):
            self.topLeft = (parkingDictionary["x1"], parkingDictionary["y1"])
            self.topRight = (parkingDictionary["x2"], parkingDictionary["y1"])
            self.bottomRight = (parkingDictionary["x2"], parkingDictionary["y2"])
            self.bottomLeft = (parkingDictionary["x1"], parkingDictionary["y2"])
        else:
            print "Error, data is not submitted properly."

        self.lot = parkingDictionary["lot"]
        self.row = parkingDictionary["row"]
        self.spot = parkingDictionary["spot"]

        self.width = abs(self.topLeft[0] - self.topRight[0])
        self.height = abs(self.topLeft[1] - self.bottomLeft[1])

        self.ptsArray = np.array([[self.topLeft[0],self.topLeft[1]], [self.topRight[0],self.topRight[1]], [self.bottomRight[0],self.bottomRight[1]], [self.bottomLeft[0],self.bottomLeft[1]]], np.int32)
        self.ptsArray = self.ptsArray.reshape((-1,1,2))

        self.isSpotTaken = False

    def createRectangleOnImage(self, imageToDrawTo, color=None):
        if color is None:
            color = 255
        cv2.rectangle(imageToDrawTo,(self.x1,self.y1),(self.x2,self.y2),(color,0,0),3)
    
    def createPolygonOnImage(self, imageToDrawTo, color=None):
        if color is None:
            color = 255
        cv2.polylines(imageToDrawTo,[self.ptsArray],True, (color, 0, 0), 3)
    
    def fillRectangleOnImage(self, imageToDrawTo, valueToDraw):
        for x in range(self.x1, self.x2):
            for y in range(self.y1, self.y2):
                imageToDrawTo[y,x] = valueToDraw
    
    def drawMaskOnImage(self, imageToDrawTo):
        cv2.polylines(imageToDrawTo, [self.ptsArray], True, (0, 255, 255))
        cv2.fillPoly(imageToDrawTo, [self.ptsArray], (0, 255, 255))

    def fillPolygonOnImage(self, imageToDrawTo, valueToDraw):
        # pts = np.array([[self.x1,self.y1], [self.x2,self.y1], [self.x2,self.y2], [self.x1,self.y2]], np.int32)
        # pts = np.array([[self.topLeft[0],self.topLeft[1]], [self.topRight[0],self.topRight[1]], [self.bottomRight[0],self.bottomRight[1]], [self.bottomLeft[0],self.bottomLeft[1]]], np.int32)
        # pts = pts.reshape((-1,1,2))
        cv2.polylines(imageToDrawTo,[self.ptsArray],True, valueToDraw)
        cv2.fillPoly(imageToDrawTo, [self.ptsArray], valueToDraw)

    def getAverage(self, imageToGetAverageOf):
        totalLightValue = 0

        # pdb.set_trace()

        for x in range(self.x1, self.x2):
            for y in range(self.y1, self.y2):
                totalLightValue += imageToGetAverageOf[y,x]
        
        return totalLightValue / (self.width * self.height)               
    
    def getPolygonAverage(self, imageToGetAverageOf, imageMask):
        # Refactor this to 8 Point system
        totalLightValue = 0
        yellowPixel = 0
        highestX = max(self.topLeft[0], self.bottomLeft[0], self.bottomRight[0], self.topRight[0])
        lowestX = min(self.topLeft[0], self.bottomLeft[0], self.bottomRight[0], self.topRight[0])

        highestY = max(self.topLeft[1], self.bottomLeft[1], self.bottomRight[1], self.topRight[1])
        lowestY = min(self.topLeft[1], self.bottomLeft[1], self.bottomRight[1], self.topRight[1])

        for x in range(lowestX, highestX):
            for y in range(lowestY, highestY):
                yellowPixel += 1
                if imageMask[y,x][1] == 255 and imageMask[y,x][2] == 255:
                    totalLightValue += imageToGetAverageOf[y,x]
        
        return totalLightValue / yellowPixel

    def isSingleSpotTaken(self, greyedImage, sensitivityLightValue, x = None):
       # TODO:
       # 1) Feed in only greyscaled image
        # average = self.getAverage(greyedImage)
        polygonAverage = self.getPolygonAverage(greyedImage, x)
        # print "This is the average: ", average
        print "This is the polygonAverage: ", polygonAverage
        self.fillPolygonOnImage(greyedImage, polygonAverage)
        # self.fillRectangleOnImage(greyedImage, average)

        if (sensitivityLightValue > polygonAverage):
            print "This spot is taken."
            return True
        else:
            print "This spot is not taken."
            return False
        pass
