from cv2 import cv2
import numpy as np

def main():
  vc = cv2.VideoCapture(0,cv2.CAP_DSHOW)

  if vc.isOpened():
    rval, frame = vc.read()
  else:
    rval = False

  while rval:
    rval, frame = vc.read()
    print(toASCII(frame))

    key = cv2.waitKey(50) # 50ms pause -> ~20fps
    # Press echap to end
    if key == 27:
      break

def toASCII(frame, cols = 120, rows = 35):

  frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  height, width = frame.shape
  cell_width = width / cols
  cell_height = height / rows
  if cols > width or rows > height:
    raise ValueError('Too many cols or rows.')
  result = ""
  for i in range(rows):
    for j in range(cols):
      gray = np.mean(
        frame[int(i * cell_height):min(int((i + 1) * cell_height), height), int(j * cell_width):min(int((j + 1) * cell_width), width)]
      )
      result += grayToChar(gray)
    result += '\n'
  return result

def grayToChar(gray):
  CHAR_LIST = ' .:-=+*#%@'
  num_chars = len(CHAR_LIST)
  return CHAR_LIST[
    min(
      int(gray * num_chars / 255),
      num_chars - 1
    )
  ]
  
if __name__ == '__main__':
    main()
