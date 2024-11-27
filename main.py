import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import mysql.connector
from datetime import datetime

# Connect to MySQL Database
db_connection = mysql.connector.connect(
    host="localhost",
    user="Mona",
    password="123456",
    database="face_recognition_attendance"
)
db_cursor = db_connection.cursor()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread(r'./Resources/background.png')

# Importing the mode images into a list.
folderModePath = r'./Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# Load the encoding file
print("Loading Encode File..")
file = open("EncodeFile.p", 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File Loaded..")

modeType = 1
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()

    if not success:
        print("Failed to capture image")
        break  # Exit the loop if the image capture fails

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]

                if counter == 0:
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter == 1:
                db_cursor.execute(f"SELECT * FROM student1 WHERE id = {id}")
                studentInfo = db_cursor.fetchone()
                print(studentInfo)
            total_attendance = studentInfo[5]
            student_name = studentInfo[2]
            student_major = studentInfo[2]
            student_standing = studentInfo[1]
            student_year = studentInfo[7]
            starting_year = studentInfo[4]
            if modeType != 3:
                if 10 < counter <= 20:
                    modeType = 2
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    # Draw text on the background image
                    cv2.putText(imgBackground, str(total_attendance), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

                    cv2.putText(imgBackground, str(student_major), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
                    cv2.putText(imgBackground, str(student_standing), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
                    cv2.putText(imgBackground, str(student_year), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
                    cv2.putText(imgBackground, str(starting_year), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

                    (w, h), _ = cv2.getTextSize(student_name, cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (534 - w) // 2
                    cv2.putText(imgBackground, str(student_name), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
                datatimeobject = studentInfo[8]  # No need to use strptime

                # Calculate the elapsed time in seconds
                secondsElapsed = (datetime.now() - datatimeobject).total_seconds()

                # Print the elapsed time
                # print(f"Seconds elapsed since {datatimeobject}: {secondsElapsed}")
                if secondsElapsed > 30:
                    current_time = datetime.now()
                    student_id = id
                    # Prepare the update query
                    update_query = """
                                            UPDATE face_recognition_attendance.student1
                                            SET total_attendance = total_attendance + 1,
                                                last_attendance_time = %s
                                            WHERE student_id = %s
                                        """

                    db_cursor.execute(update_query, (current_time, student_id))  # Use 'id' instead of 'student_id'
                    db_connection.commit()
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            counter += 1  # Increment counter after processing

            if counter >= 20:
                counter = 0
                modeType = 0
                studentInfo = []
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType=0
        counter=0
    cv2.imshow("Face Attendance", imgBackground)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
db_cursor.close()
db_connection.close()