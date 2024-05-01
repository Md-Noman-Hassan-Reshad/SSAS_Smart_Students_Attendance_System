import cv2
import cvzone
import numpy as np
import face_recognition as fr
import os
from datetime import datetime
import time
import pyttsx3


def speak(audio, voice_id=1, rate=170, volume=1.0):
    try:
        engine = pyttsx3.init("sapi5")
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[voice_id].id)
        engine.setProperty("rate", rate)
        engine.setProperty("volume", volume)
        engine.say(audio)
        engine.runAndWait()
    except Exception as e:
        print(f"Error occurred during speech synthesis: {e}")


img_path = "Attendance_Images"
std_images = []
std_names = []
std_list = os.listdir(img_path)
# print(std_list)

for std in std_list:
    current_img = cv2.imread(f"{img_path}/{std}")
    std_images.append(current_img)
    std_names.append(os.path.splitext(std)[0])

print(std_names)


def find_encodings(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list


def mark_attendance(name):
    # Extracting student ID, semester, and name from the provided name string.
    std_id = name[:6]
    sem = name[7:10]
    std_name = name[11:]

    now = datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    time_str = now.strftime(f"%I:%M:%S %p")

    csv_path = "Attendance_CSV"

    csv_files = {
        "1st": f"{csv_path}/1st_{date_str}_attendance.csv",
        "2nd": f"{csv_path}/2nd_{date_str}_attendance.csv",
        "3rd": f"{csv_path}/3rd_{date_str}_attendance.csv",
        "4th": f"{csv_path}/4th_{date_str}_attendance.csv",
        "5th": f"{csv_path}/5th_{date_str}_attendance.csv",
        "6th": f"{csv_path}/6th_{date_str}_attendance.csv",
        "7th": f"{csv_path}/7th_{date_str}_attendance.csv",
        "8th": f"{csv_path}/8th_{date_str}_attendance.csv"
    }

    # Check if a CSV file already exists for the given semester and date combination
    if sem in csv_files and os.path.exists(csv_files[sem]):
        csv_file_path = csv_files[sem]
    else:
        csv_file_path = f"{csv_path}/{sem}_{date_str}_attendance.csv"
        with open(csv_file_path, "w") as new_f:
            new_f.write("Id,Sem,Date,Time,Name")

    # Write data to the selected CSV file
    with open(csv_file_path, "r+") as f:
        std_data_list = f.readlines()
        name_list = [line.split(",")[0] for line in std_data_list]
        # print(name)

        if std_id not in name_list:
            f.writelines(f"\n{std_id},{sem},{date_str},{time_str},{std_name}")
            # speak(f"Done. Id {std_id} has been marked in {sem} semester!")
            print(f"Done. Id {std_id} has been marked in {sem} semester!")
            # time.sleep(1)
            print("Monitoring (Press 'q' for exit window)...")
        else:
            # speak(f"Exist. Id {std_id} already marked up in {sem} semester!")
            print(f"Exist. Id {std_id} already marked up in {sem} semester!")
            # time.sleep(1)
            print("Monitoring (Press 'q' for exit window)...")


encode_list_known = find_encodings(std_images)

print(f"Encoding completed for #{len(encode_list_known)}")
time.sleep(0.7)
print("Monitoring (Press 'q' for exit window)...")

cap = cv2.VideoCapture(4)

if not cap.isOpened():
    print("Error: Unable to open camera.")

while True:
    success, img = cap.read()

    # A "factor of 4" means multiplying by 4
    # "factor of 4" refers to the reduction of dimensions by a quarter(one - fourth) of their original values.
    # Resize the frame to 1/4 of its original size.
    img_sm = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_sm = cv2.cvtColor(img_sm, cv2.COLOR_BGR2RGB)

    faces_cur_frame = fr.face_locations(img_sm)
    encodes_cur_frame = fr.face_encodings(img_sm, faces_cur_frame)

    # Iterate through each face found in the current frame.
    for encode_face, face_loc in zip(encodes_cur_frame, faces_cur_frame):
        matches = fr.compare_faces(encode_list_known, encode_face)
        face_dst = fr.face_distance(encode_list_known, encode_face)
        # print("matches", matches)
        # print("face_dst", face_dst)

        match_index = np.argmin(face_dst)
        # print("match_index", match_index)

        if matches[match_index]:
            name = std_names[match_index]
            y1, x2, y2, x1 = face_loc
            # Scale up the coordinates to match the original image.
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = x1, y1, x2 - x1, y2 - y1
            cvzone.cornerRect(img, bbox, 25, 2)
            cvzone.putTextRect(img, str(name[:6]),
                               (x1 + 6, y1 - 9), scale=1.1, thickness=1, offset=7)

            mark_attendance(name)
        else:
            name = "Unknown"
            y1, x2, y2, x1 = face_loc
            # Scale up the coordinates to match the original image.
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = x1, y1, x2 - x1, y2 - y1
            cvzone.cornerRect(img, bbox, 25, 2)
            cvzone.putTextRect(img, name,
                               (x1 + 6, y1 - 9), scale=1.1, thickness=1, offset=7)
            print(f"ID not found, {name}")

    cv2.imshow("SSAS", img)
    # cv2.imshow("Resized Image", img_sm)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
