import os
import cv2
from datetime import datetime
import time
from colorama import init, Fore
import pyttsx3

# def message_animate_dots(message):
#     init(autoreset=True)  # Initialize colorama
#     print(message, end="", flush=True)
#     while True:
#         # Add dots one after another
#         for _ in range(4):
#             print(Fore.GREEN + ".", end="", flush=True)  # Print a yellow dot
#             time.sleep(0.3)
#         # Remove dots
#         print("\b" * 4, end="", flush=True)
#         time.sleep(0.5)
#
#
# message_animate_dots("Monitoring")

name = "662220-8th-Bill Gates"
std_id = name[:6]
sem = name[7:10]
std_name = name[11:]

now = datetime.now()
date_str = now.strftime("%d-%m-%Y")
time_str = now.strftime("%I:%M:%S %p")

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
    print("data written current file")
else:
    csv_file_path = f"{csv_path}/{sem}_{date_str}_attendance.csv"
    with open(csv_file_path, "w") as new_f:
        new_f.write("Id, Sem, Date, Time, Name")
        print("data written in new file")

# Write data to the selected CSV file
with open(csv_file_path, "r+") as f:
    std_data_list = f.readlines()
    name_list = [line.split(", ")[0] for line in std_data_list]

    if std_id not in name_list:
        f.writelines(f"\n{std_id}, {sem}, {date_str}, {time_str}, {std_name}")
        print(f"Done. ID {std_id} has been marked in {sem} semester!")
        print("Monitoring (Press 'q' to exit)...")
    else:
        print(f"Exist. ID {std_id} already marked in {sem} semester!")
        print("Monitoring (Press 'q' to exit)...")

# def speak(audio, voice_id=1, rate=170, volume=1.0):
#     try:
#         engine = pyttsx3.init("sapi5")
#         voices = engine.getProperty("voices")
#         engine.setProperty("voice", voices[voice_id].id)
#         engine.setProperty("rate", rate)
#         engine.setProperty("volume", volume)
#         engine.say(audio)
#         engine.runAndWait()
#     except Exception as e:
#         print(f"Error occurred during speech synthesis: {e}")
#
#
# speak("hello there")
