from CircleMozaicCreator import CircleMozaicCreator
import cv2

cap = cv2.VideoCapture(0)
editor = CircleMozaicCreator(25)
while True:
    ret, frame = cap.read()

    inputImg = cv2.flip(frame, 1)

    dims = inputImg.shape
    height, width = dims[0], dims[1]

    inputImg = cv2.resize(inputImg, (1000,1000))

    outputImg = editor.render(inputImg)

    outputImg = cv2.resize(outputImg, (width, height))

    cv2.imshow("Camera Feed", outputImg)

    if cv2.waitKey(1) == ord("q"):
        break

# clean up the camera and window objs
cap.release()
cv2.destroyAllWindows()
