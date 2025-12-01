from CircleMozaicCreator import CircleMozaicCreator
import cv2
import random
import tkinter as tk
from tkinter import filedialog


def getFilePath():
    root = tk.Tk()
    root.withdraw()

    filePath = filedialog.askopenfilename(title="Select a File")

    return filePath


filePath = getFilePath()
cap = cv2.VideoCapture(filePath)

# input from the camera really has to match the outputed saved file
fps = cap.get(cv2.CAP_PROP_FPS)
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")        # defines the .mp4 codec
out = cv2.VideoWriter(f"newVid_{random.randint(1000,9999)}.mp4", fourcc, fps, (frameWidth, frameHeight), isColor=False)

editor = CircleMozaicCreator(10)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    inputImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    outputImg = editor.render(inputImg)

    out.write(outputImg)

    if cv2.waitKey(1) == ord("q"):
        break
print("Done!")

# clean up the camera, recording and window objs
cap.release()
out.release()
cv2.destroyAllWindows()