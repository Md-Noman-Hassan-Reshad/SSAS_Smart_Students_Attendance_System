import cv2
import cvzone
import numpy as np
import face_recognition

img_elon = face_recognition.load_image_file("Basics_Images/elon_musk_training.jpg")
img_elon = cv2.cvtColor(img_elon, cv2.COLOR_BGR2RGB)

img_elon_test = face_recognition.load_image_file("Basics_Images/bill_gates.jpg")
img_elon_test = cv2.cvtColor(img_elon_test, cv2.COLOR_BGR2RGB)

img_elon = cv2.resize(img_elon, (500, 500))
img_elon_test = cv2.resize(img_elon_test, (500, 500))

face_loc = face_recognition.face_locations(img_elon)[0]
encode_elon = face_recognition.face_encodings(img_elon)[0]
y1, x2, y2, x1 = face_loc
print(face_loc)
bbox = x1, y1, x2 - x1, y2 - y1
cvzone.cornerRect(img_elon, bbox, 25, 2)
cvzone.putTextRect(img_elon, "662227", (x1 + 6, y1 - 9), scale=1.1, thickness=1, offset=7)

face_loc_test = face_recognition.face_locations(img_elon_test)[0]
encode_elon_test = face_recognition.face_encodings(img_elon_test)[0]
bbox = x1, y1, x2 - x1, y2 - y1
cvzone.cornerRect(img_elon_test, bbox, 25, 2)
cvzone.putTextRect(img_elon_test, "662227", (x1 + 6, y1 - 9), scale=1.1, thickness=1, offset=7)

results = face_recognition.compare_faces([encode_elon], encode_elon_test)
face_dist = face_recognition.face_distance([encode_elon], encode_elon_test)
print(results, face_dist)

color = (17, 180, 17) if results == [True] else (18, 18, 255)

cv2.putText(
    img_elon_test,
    f"{results} {round(face_dist[0], 2)}",
    (50, 50),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    color,
    2,
)

stack_images = cvzone.stackImages([img_elon, img_elon_test], 2, 0.8)

# cv2.imshow("Elon Training", img_elon)
# cv2.imshow("Elon Test", img_elon_test)
cv2.imshow("Result", stack_images)

cv2.waitKey(0)
cv2.destroyAllWindows()
