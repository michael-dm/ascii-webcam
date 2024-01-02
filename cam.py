import cv2 as cv
import numpy as np
import os
import sys
import platform
from pynput.keyboard import Key, Listener
from pynput.keyboard import Key

def on_press(key):
    finish(key)

def on_release(key):
    pass

listener = Listener(on_press=on_press, on_release=on_release)

def finish(key):
    if key == Key.esc:
        listener.stop()
        os._exit(0)

def main():
    vc = None

    if platform.system() == 'Windows':
        vc = cv.VideoCapture(0, cv.CAP_DSHOW)
    elif platform.system() == 'Linux':
        vc = cv.VideoCapture(0)

    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False

    if rval:
        listener.start()

    while rval:
        rval, frame = vc.read()
        print(toASCII(frame))

    vc.release()  # Release the video capture when done
    cv.destroyAllWindows()  # Close any OpenCV windows

    sys.exit()

def toASCII(frame, cols=120, rows=35):
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    height, width = frame.shape
    cell_width = width / cols
    cell_height = height / rows
    if cols > width or rows > height:
        raise ValueError('Too many cols or rows.')
    result = ""
    for i in range(rows):
        for j in range(cols):
            gray = np.mean(
                frame[int(i * cell_height):min(int((i + 1) * cell_height), height),
                int(j * cell_width):min(int((j + 1) * cell_width), width)]
            )
            result += grayToChar(gray)
        result += '\n'
    return result

def grayToChar(gray):
    CHAR_LIST = " .',;:clodxkO0KXNWM"  # Replace by " .',;:clodxkO0KXNWM" for more precision.
    num_chars = len(CHAR_LIST)
    return CHAR_LIST[
        min(
            int(gray * num_chars / 255),
            num_chars - 1
        )
    ]

if __name__ == '__main__':
    main()
