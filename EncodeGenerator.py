import os
import cv2
import face_recognition
import pickle
import mysql.connector

db_connection = mysql.connector.connect(
    host="localhost",
    user="Mona",
    password="123456",
    database="face_recognition_attendance"
)
db_cursor = db_connection.cursor()

# Importing the student images.
folderPath = 'Images'
PathList = os.listdir(folderPath)
# print(PathList)
imgList = []
studentIds = []
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentIds.append(os.path.splitext(path)[0])
    # print(path)
    # print(os.path.splitext(path)[0])
    # print(studentIds)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print("Encoding Started..")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown,studentIds]
print("Encoding Complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")

# Insert student data into MySQL database here
for student_id in studentIds:
    db_cursor.execute("INSERT INTO students (student_id) VALUES (%s)", (student_id,))
db_connection.commit()

db_cursor.close()
db_connection.close()