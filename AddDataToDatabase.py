import mysql.connector

db_connection = mysql.connector.connect(
    host="localhost",
    user="Mona",
    password="123456",
    database="face_recognition_attendance"
)
db_cursor = db_connection.cursor()
'''
data = {
    "01":
        {
            "name": "Narendra Modi",
            "major": "Economics",
            "starting_year": 2014,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-11-11 00:54:34"
        },
    "02":
        {
            "name": "Donald Trump",
            "major": "Economics",
            "starting_year": 2017,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2024-11-11 00:54:34"
        },
    "03":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 8,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2024-11-11 00:54:34"
        },
    "04":
        {
            "name": "Monalisha Sahoo",
            "major": "Computer Science",
            "starting_year": 2021,
            "total_attendance": 11,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2024-11-11 00:54:34"
        },
    "05":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2024-11-11 00:54:34"
        }

}

for key, value in data.items():
    db_cursor.execute("""
           # INSERT INTO face_recognition_attendance.students (id, name, major, starting_year, total_attendance, standing, year, last_attendance_time) 
            #VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                      (key,
                       value["name"],
                       value["major"],
                       value["starting_year"],
                       value["total_attendance"],
                       value["standing"],
                       value["year"],
                       value["last_attendance_time"]))
'''
db_cursor.execute('''Select * from face_recognition_attendance.student1''')
db_connection.commit()
db_cursor.close()
db_connection.close()
