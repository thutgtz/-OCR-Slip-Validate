import sys
import os
import math
import cv2
import re
import imutils
import numpy as np
import easyocr
from matplotlib import pyplot as plt
from pyzbar.pyzbar import decode
import simplejson as json
import base64
from PIL import ImageFont, ImageDraw, Image

reader = easyocr.Reader(['th','en']) # config easyocr able to read thai & eng 

def readBase64img(base64_string):
    decoded_data = base64.b64decode(base64_string)
    np_data = np.frombuffer(decoded_data,np.uint8)
    return cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)

obj = json.loads(input())

img64 = obj['img64']
data = obj['data']

months = ['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.']
regex = {
    "name" : "(นาย|นาง|นางสาว|น.ส.).*", # get all text after นาย|นาง|นางสาว|น.ส.
    "date" : "([0-9]{1,2})([ ]+)?(%s)([ ]+)?([0-9]{2,4})" % ('|'.join(months)), # match string look like "01 ม.ค. 2565"
    "time" : "([0-9]{1,2})([:][0-9][0-9])", # match string look like "09:30"
    "reference" : "([0-9A-Za-z]){14,}", # match continuous string that have only ( a-z, A-Z, 0-9 ) more than 14
    "money" : "([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)([.][0-9][0-9])" # match string look money format with 2 decimal
}

def lcs(X, Y):
  m = len(X)
  n = len(Y)
  L = [[0 for x in range(n+1)] for x in range(m+1)]
  for i in range(m+1):
    for j in range(n+1):
      if i == 0 or j == 0:
        L[i][j] = 0
      elif X[i-1] == Y[j-1]:
        L[i][j] = L[i-1][j-1] + 1
      else:
        L[i][j] = max(L[i-1][j], L[i][j-1])
  index = L[m][n]
  lcs = [""] * (index+1)
  lcs[index] = ""
  i = m
  j = n
  text = ''
  count = 0
  while i > 0 and j > 0:
    if X[i-1] == Y[j-1]:
      lcs[index-1] = X[i-1]
      text = X[i-1] + text
      i-=1
      j-=1
      index-=1
    elif L[i-1][j] > L[i][j-1]:
      i-=1 ; count += 1
      text = '_' + text
    else:
      j-=1
  
  if len(X)-len(text) > 0:
    count += len(X)-len(text)
    text = ''.join(['_']* (len(X)-len(text)) ) + text
  return text, ((len(text)-count)/len(text))


class Text:
  def __init__(self, text, pos):
    self.text = text
    self.position = pos


def OCR(img64):
  list_text = [] # initial variable for text extraction with image
  img = readBase64img(img64) # read image file 
  img = imutils.resize(img, height=1024) # resize image
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # Convert to HSV color-space
  msk = cv2.inRange(hsv, np.array([0, 0, 155]), np.array([255, 255, 255])) # Get binary mask

  # --------------------------- Extract features ---------------------------
  krn = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3)) # create rectangle kernel size 3x3 
  dlt = cv2.erode(msk, krn, iterations=5) # spread black [1] pixel to close white [0] space
  dlt = cv2.bitwise_not(dlt) # invert black [1] to white [0]
  dlt = cv2.cvtColor(dlt, cv2.COLOR_GRAY2BGR) # convert Binary to RGB
  res = cv2.bitwise_and(img, dlt) # combine mask with image (select only white [0] space in mask)
  # ------------------------------------------------------------------------
  
  gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY) # convert Binary to RGB
  contours,hierarchy = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) # find contour (frame of close area)

  lines = {} 
  desired_list = []

  # ----------------- Find QRcode -----------------
  for contour in contours:
    (x, y, w, h) = cv2.boundingRect(contour)
    desired_list.append([x, y, w, h])
    if( w/h < 1.3 and w/h > 0.7 ):
      im = img[y:y+h, x:x+w] # crop image
      QR = decode(im)
      if( len(QR) > 0) :
        data["reference"] = QR[0].data.decode().lower()
  # -----------------------------------------------

  # ----------------- Bounding Line -----------------
  horizontal_list = [desired_list[0]]
  for a, b in zip(desired_list[:-1], desired_list[1:]):
    if abs( (a[1]) - (b[1]) ) < 25: continue
    else : horizontal_list += [b]
  # -------------------------------------------------

  # ----------------- Bounding contour keep in line -----------------
  for contour in reversed(contours):
    min_abs = math.inf ; round_y = 0
    (x, y, w, h) = cv2.boundingRect(contour)
    for (X, Y, W, H) in horizontal_list :
      if(abs(y - Y) < min_abs) :
        min_abs = abs(y - Y)
        round_y = Y

    if lines.get(str(round_y)) is not None : 
      lines[str(round_y)].append((x, y, w, h))
      lines[str(round_y)].sort(key=lambda x: int(x[0]))
    else : lines[str(round_y)] = [(x, y, w, h)]
  # -----------------------------------------------------------------

  result = {} 
  text_lines = []
  for key in lines:
    text = [] ; position = [math.inf,math.inf,0,0]
    for line in lines[key]:
      (x, y, w, h) = line 
      position = [ min(position[0],x), min(position[1],y), max(position[2],x+w), max(position[3],y+h) ] # bounding frame
      if w> 10:
        im = img[y:y+h, x:x+w] # crop image
        im = imutils.resize(im, height=36) # resize image height to 36 pixel
        read_text = reader.readtext(im,paragraph="False",detail=0) # OCR read text from croped image
        if len(read_text) > 0 : text.append(read_text[0])
    text_line = ' '.join(text) # text in line format
    text_lines.append(text_line)
    for keyword in regex:
      tmp = re.search(regex[keyword], text_line)
      if tmp != None : 
        tmp_text = tmp.group(0)
        if keyword == 'date':
          month = re.search('(%s)' % ('|'.join(months)),tmp_text).group(0)
          day,year =tmp_text.split(month)
          if len(year) == 2: year = '25'+year
          tmp_text = '%s-%s-%s' % (int(year.strip())-543,'%02d' % (months.index(month.strip())+1),'%02d' % (int(day.strip())))
        result[keyword] = Text(tmp_text,position)

  # ------------------------------ result-----------------------------------
  json_obj = {}
  new_img = img.copy() 
  height, width,_ = new_img.shape
  blank_image = np.zeros((height,width+640,3), np.uint8)
  blank_image[0:new_img.shape[0], 0:new_img.shape[1]] = new_img
  cv2_im_rgb = cv2.cvtColor(blank_image, cv2.COLOR_BGR2RGB)
  pil_im = Image.fromarray(cv2_im_rgb)
  draw = ImageDraw.Draw(pil_im)
  font_path = os.path.join(os.path.dirname(__file__),"./font/THSarabunNew.ttf")
  font_20 = ImageFont.truetype(font_path, 20)
  font_30 = ImageFont.truetype(font_path, 30)
  font_50 = ImageFont.truetype(font_path, 50)
  line = 50 ; i = 0 ; total_per = 0
  for x in result:
    json_obj[x] = result[x].text
    cv2.rectangle(new_img, (result[x].position[0], result[x].position[1]), (result[x].position[2], result[x].position[3]), (255,0,0), 2)
    if data.get(x) is not None :
      text,per = lcs(data[x],result[x].text)
      draw.text(( width+50 , line ), x, font=font_30, fill='green') ; line += 30
      draw.text(( width+50 , line ), "ข้อมูลจริง     : " + data[x], font=font_20, fill='green') ; line += 20
      draw.text(( width+50 , line ), "ข้อมูลที่ได้    : " + result[x].text, font=font_20, fill='green') ; line += 20
      draw.text(( width+50 , line ), "เปรียบเทียบ : " + text, font=font_20, fill='green') ; line += 20
      draw.text(( width+50 , line ), "เปอร์เซ็นถูก  : " + str(round(per*100,2))+'%', font=font_20, fill='green') ; line += 30
      i += 1 ; total_per += per*100
  draw.text(( width+50 , line ), str(round(total_per/i, 2))+'%', font=font_50, fill='green') ;
  blank_image = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

  for x in result:
    json_obj[x] = result[x].text
    cv2.rectangle(blank_image, (result[x].position[0], result[x].position[1]), (result[x].position[2], result[x].position[3]), (255,0,0), 2)
  
  retval, buffer = cv2.imencode('.jpg', blank_image)
  json_obj['image'] = base64.b64encode(buffer)
  json_obj['text_line'] = text_lines
  json_obj['percent'] = round(total_per/i, 2)
  if data.get('reference') is not None :  json_obj['reference'] = data['reference']
  return json.dumps(json_obj)
  # ------------------------------ END -----------------------------------

print('JSON:%s' % (OCR(img64)))