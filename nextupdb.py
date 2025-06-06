import sqlite3

def startDb():
    conn = sqlite3.connect('nextup.db')
    cursor = conn.cursor()

    startDbCommands = ["""
                        CREATE TABLE IF NOT EXISTS `students` (
                            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                            `name` TEXT,
                            `surname` TEXT
                        );
                        """,
                        """
                        CREATE TABLE IF NOT EXISTS `subjects` (
                            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                            `name` TEXT,
                            `teacher` TEXT
                        );
                        """,
                        """
                        CREATE TABLE IF NOT EXISTS `lists` (
                            `student` INTEGER,
                            `subject` INTEGER,
                            `position` INTEGER NOT NULL,

                            PRIMARY KEY (`student`, `subject`),
                            FOREIGN KEY (`student`) REFERENCES `students` (`id`),
                            FOREIGN KEY (`subject`) REFERENCES `subjects` (`id`)
                        );
                        """
                    ]

    for command in startDbCommands:
        cursor.execute(command)
    conn.close()
    

def getStudents():
    conn = sqlite3.connect('nextup.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    results = cursor.fetchall()

    conn.close()

    return results

def addStudent(name, surname):
    conn = sqlite3.connect('nextup.db')
    cursor = conn.cursor()

    cursor.execute(f'''INSERT INTO students VALUES (null, "{name}", "{surname}")''')

    conn.commit()

    conn.close()

def removeStudent(name, surname):
    conn = sqlite3.connect('nextup.db')
    cursor = conn.cursor()

    cursor.execute(f'''DELETE FROM students WHERE name = "{name}" AND surname = "{surname}"''')

    conn.commit()

    conn.close()

def getSubjects():
    conn = sqlite3.connect('nextup.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM subjects")

    results = cursor.fetchall()

    conn.close()

    return results

def addSubject(name, teacher):
    conn = sqlite3.connect('nextup.db')
    cursor = conn.cursor()

    cursor.execute(f'''INSERT INTO subjects VALUES (null, "{name}", "{teacher}")''')

    conn.commit()

    conn.close()

def removeSubject(name, teacher):
    conn = sqlite3.connect('nextup.db')
    cursor = conn.cursor()

    cursor.execute(f'''DELETE FROM subjects WHERE name = "{name}" AND teacher = "{teacher}"''')

    conn.commit()

    conn.close()

def getDraws():
    conn = sqlite3.connect('nextup.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM lists")

    results = cursor.fetchall()

    conn.close()

    return results

def setStudDrawn(studentId, subjectId, position):
    conn = sqlite3.connect('nextup.db')
    cursor = conn.cursor()

    cursor.execute(f'''INSERT INTO lists VALUES ({studentId}, {subjectId}, {position})''')

    conn.commit()

    conn.close()

def removeDrawn(studentId, subjectId):
    conn = sqlite3.connect('nextup.db')
    cursor = conn.cursor()

    cursor.execute(f'''DELETE FROM lists WHERE student = "{studentId}" AND subject = "{subjectId}"''')

    conn.commit()

    conn.close()