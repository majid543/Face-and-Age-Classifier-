from deepface import DeepFace
import cv2

img = cv2.imread('new2.jpg')
result = DeepFace.analyze(img, actions=("age"))
print(result)