from CircleMozaicCreator import CircleMozaicCreator
import cv2

cap = cv2.VideoCapture(0)
editor = CircleMozaicCreator(10)
while True:
    ret, frame = cap.read()

    inputImg = cv2.flip(frame, 1)
    outputImg = editor.render(inputImg)

    cv2.imshow("Camera Feed", outputImg)

    if cv2.waitKey(1) == ord("q"):
        break

# clean up the camera and window objs
cap.release()
cv2.destroyAllWindows()