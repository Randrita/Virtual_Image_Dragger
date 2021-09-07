import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os

cap = cv2.VideoCapture(0)
#increasing the canvas size
cap.set(3, 1280)
cap.set(4, 720)

#detectionCon is used to add some accuracy strength 
detector = HandDetector(detectionCon=0.8)


class DragImg():
    def __init__(self, path, posOrigin, imgType):

        self.posOrigin = posOrigin
        self.imgType = imgType
        self.path = path

        if self.imgType == 'png':
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)

        # self.img = cv2.resize(self.img, (0,0),None,0.4,0.4)

        self.size = self.img.shape[:2]

    def update(self, cursor):
        ox, oy = self.posOrigin
        h, w = self.size

        # Check if in region
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2

#time to read the images to place it over our canvas
path = "ImagesPNG"
myList = os.listdir(path)
print(myList)

listImg = []
for x, pathImg in enumerate(myList):
    if 'png' in pathImg:
        imgType = 'png'
    else:
        imgType = 'jpg'
    listImg.append(DragImg(f'{path}/{pathImg}', [50 + x * 300, 50], imgType))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    #to find all landmarks

    if hands:
        lmList = hands[0]['lmList']
        # Check if clicked
        #check if its in a region or not
        #idea is to locate the image region now
        #cursor[0] will return x and cursor[1] will return y
        #we have to find the distance between index and middle finger and depends on the threshold we will then move the image
 
        length, info, img = detector.findDistance(lmList[8], lmList[12], img)
        #print(length)
        #to check if its clicked by assigning a minimum threshold value
        if length < 60:
            cursor = lmList[8]
            for imgObject in listImg:
                imgObject.update(cursor)

    try:
        #for PNG
        #to find height and width

        for imgObject in listImg:

            # Draw for JPG image
            h, w = imgObject.size
            ox, oy = imgObject.posOrigin
            if imgObject.imgType == "png":
                # Draw for PNG Images
                img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])
            else:
                img[oy:oy + h, ox:ox + w] = imgObject.img

    except:
        pass
    
    #Display the resulting frame
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord('q'):
        break