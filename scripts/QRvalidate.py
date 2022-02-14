import sys
import os
import math
import cv2
import re
import imutils
import numpy as np
from pyzbar.pyzbar import decode
import simplejson as json
import base64


def readBase64img(base64_string):
    decoded_data = base64.b64decode(base64_string)
    np_data = np.frombuffer(decoded_data,np.uint8)
    return cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)

obj = json.loads(input())
img64 = obj['img64']

list_text = [] # initial variable for text extraction with image
img = readBase64img(img64) # read image file 
img = imutils.resize(img, height=1024) # resize image
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # Convert to HSV color-space
msk = cv2.inRange(hsv, np.array([0, 0, 155]), np.array([255, 255, 255])) # Get binary mask

  # --------------------------- Extract features ---------------------------
krn = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2)) # create rectangle kernel size 3x3 
dlt = cv2.erode(msk, krn, iterations=5) # spread black [1] pixel to close white [0] space
dlt = cv2.bitwise_not(dlt) # invert black [1] to white [0]
dlt = cv2.cvtColor(dlt, cv2.COLOR_GRAY2BGR) # convert Binary to RGB
res = cv2.bitwise_and(img, dlt) # combine mask with image (select only white [0] space in mask)
  # ------------------------------------------------------------------------
  
gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY) # convert Binary to RGB
contours,hierarchy = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) # find contour (frame of close area)

lines = {} 
json_obj = {}
  
QR = []
  # ----------------- Find QRcode -----------------
for contour in contours:
    (x, y, w, h) = cv2.boundingRect(contour)
    if( w/h < 1.3 and w/h > 0.7 ):
      im = img[y:y+h, x:x+w] # crop image
      QR = decode(im)
      if( len(QR) > 0) :
        json_obj["QRcode"] = QR[0].data.decode().lower()
        json_obj["REF"] = QR[0].data.decode().lower()[25:].split('5102th')[0]
        json_obj["position"] = [x, y, w, h]
  # -----------------------------------------------
  
print('JSON:%s' % (json.dumps(json_obj)))