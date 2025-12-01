from CircleMozaicCreator import CircleMozaicCreator
import cv2
import tkinter as tk
from tkinter import filedialog


def getFilePath():
    root = tk.Tk()
    root.withdraw()

    filePath = filedialog.askopenfilename(title="Select a File")

    return filePath


filePath = getFilePath()

inputImg = cv2.cvtColor(cv2.imread(filePath, cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2GRAY)
inputShape = inputImg.shape
width, height = inputImg.shape[0], inputImg.shape[1]

# blow it up (gets better results but not necessary)
#inputImg = cv2.resize(inputImg, (width*2,height*2))

editor = CircleMozaicCreator(10)
editor.render(inputImg)
editor.preview()
editor.save("outputImage.png")

#outputImg = cv2.resize(outputImg, (width,height))

cv2.imshow("Output", outputImg)
cv2.waitKey(0)

# clean up any window objs

cv2.destroyAllWindows()
