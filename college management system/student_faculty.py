import pymysql
from tkinter import messagebox
conn = None
mycursor = None

def connect_database():
    global mycursor, conn
    try:
        conn = pymysql.connect(host='localhost', user='root', password='karthi')
        mycursor = conn.cursor()

        # Create database if it doesn't exist
        mycursor.execute('CREATE DATABASE IF NOT EXISTS Collage')
        mycursor.execute('USE Collage')
        print('COllage Database is using')

        # Create tables if they don't exist
        create_faculties_table = '''
        CREATE TABLE IF NOT EXISTS faculties (
            faculty_id VARCHAR(10) NOT NULL,
            faculty_name VARCHAR(100),
            faculty_email VARCHAR(255),
            faculty_qual varchar(255),
            faculty_dept varchar(255), 
            PRIMARY KEY (faculty_id)
        );
        '''
        mycursor.execute(create_faculties_table)

        create_students_table = '''
        CREATE TABLE IF NOT EXISTS students (
            student_id VARCHAR(10) NOT NULL,
            student_name VARCHAR(100),
            cgpa DECIMAL(3, 1),
            semester VARCHAR(100),
            PRIMARY KEY (student_id)
        );
        '''
        mycursor.execute(create_students_table)

        create_studentselections_table = '''
        CREATE TABLE IF NOT EXISTS studentselections (
            student_id VARCHAR(10) NOT NULL,
            subject_code VARCHAR(10) NOT NULL,
            faculty_id VARCHAR(10) NOT NULL,
            PRIMARY KEY (student_id, subject_code, faculty_id)
        );
        '''
        mycursor.execute(create_studentselections_table)

        create_facultyassignments = '''
                CREATE TABLE IF NOT EXISTS FacultyAssignments (
                    faculty_id VARCHAR(10) NOT NULL,
                    faculty_name VARCHAR(100),
                    subject_code VARCHAR(10) NOT NULL,
                    subject_name VARCHAR(100),
                    class_number INT NOT NULL,
                    PRIMARY KEY (faculty_id, subject_code)
                );
                '''
        mycursor.execute(create_facultyassignments)

        print('Database and tables initialized successfully.')

    except pymysql.Error as e:
        messagebox.showerror(title='Error', message=f"Database Error: {e}")
        conn.rollback()  # Rollback any transaction if something went wrong
        return False

    return True
# def import_name(found_name):
#     global name
#     name = found_name

def insert_students(id, name, cgpa, semester):
    if cgpa == 'Ex: 8.7' or cgpa == '':  # Check if CGPA is the default text or empty
        cgpa = None
    query = 'insert into students(student_id, student_name, cgpa, semester) values (%s, %s, %s, %s)'
    try:
        mycursor.execute(query, args=(id, name, cgpa, semester))
        conn.commit()
        messagebox.showinfo(title="Success", message="Record inserted successfully")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Failed to insert record: {e}")
        conn.rollback()

def insert_faculties(id, name, email, qual, dept):
    query = 'insert into faculties(faculty_id, faculty_name, faculty_email, faculty_qual, faculty_dept) values (%s, %s, %s, %s, %s)'
    mycursor.execute(query, args = (id, name, email, qual, dept))
    print('Sucessfully created in faculties also')
    conn.commit()



# Faculty name, subject nokithe class room ravali
def student_details(subcode, facultyid):
    query = '''
    SELECT 
        S.student_id,
        S.student_name,
        S.semester,
        S.cgpa
    FROM 
        StudentSelections SS
    JOIN 
        Students S ON SS.student_id = S.student_id
    WHERE 
        SS.subject_code = %s
        AND SS.faculty_id = %s;
    '''
    mycursor.execute(query, args = (subcode, facultyid))
    print((subcode,facultyid))
    result = mycursor.fetchall()
    print(result)
    print('result is fetched sucessfully')
    if(result):
        print('There is something in the result')
        return result
    else:
        print('Student Data is none')
        return None


# Faculty I'd/name, subject batti student details kavali
def classfound(fname, subject):
    print(f"I need to find the class room for faculty: {fname} for subject: {subject}")
    connect_database()
    query = '''
    SELECT
        FA.class_number
    FROM
        FacultyAssignments FA
    WHERE
        FA.subject_name = %s AND FA.faculty_name = %s;
    '''
    mycursor.execute(query, (subject, fname))
    result = mycursor.fetchall()
    print(result)
    if(result):
        return result[0]
    else:
        print('No Data Found')
        return ''

# def classfound(fname, subject):
#     if not conn or not mycursor:
#         messagebox.showerror(title='Error', message='Database connection not established.')
#         return None
#
#     try:
#         query = '''
#         SELECT FA.class_number
#         FROM FacultyAssignments FA
#         WHERE FA.subject_name = %s AND FA.faculty_name = %s;
#         '''
#         mycursor.execute(query, (subject, fname))
#         result = mycursor.fetchone()
#
#         if result:
#             return result[0]
#         else:
#             print('No Data Found')
#             return ''
#
#     except pymysql.Error as e:
#         messagebox.showerror(title='Error', message=f"Database Error: {e}")
#         return None


# Subject names and alloted faculty and classroom print avvali
def student_tree(id):
    query = '''
    SELECT 
        SS.subject_code,
        SJ.subject_name,
        FA.faculty_id,
        F.faculty_name,
        FA.class_number
    FROM 
        StudentSelections SS
    JOIN 
        Subjects SJ ON SS.subject_code = SJ.subject_code
    JOIN 
        FacultyAssignments FA ON SS.faculty_id = FA.faculty_id AND SS.subject_code = FA.subject_code
    JOIN 
        Faculties F ON FA.faculty_id = F.faculty_id
    WHERE 
        SS.student_id = %s;
    '''
    mycursor.execute(query, args=(id))
    record = mycursor.fetchall()
    print(record)
    return record



# List of subjects the faculty is selecting
def subjects(fname):
    connect_database()
    query = '''
        SELECT
            s.subject_code,
            s.subject_name
        FROM
            facultyassignments fa
        JOIN
            faculties f ON fa.faculty_id = f.faculty_id
        JOIN
            subjects s ON fa.subject_code = s.subject_code
        WHERE
            f.faculty_name = %s
        ORDER BY
            s.subject_code;
        '''
    mycursor.execute(query, args = (fname))
    print(f'{fname} from the subject table')
    rows = mycursor.fetchall()
    # print(rows)
    return rows


def subcode(subname):
    query = 'select subject_code from subjects where subject_name = %s'
    mycursor.execute(query, args = (subname))
    result = mycursor.fetchone()
    print(subname, result)
    if(result):
        return result
    else:
        print('No Subject Name')
        return None

def showalls(identry):
    query = '''
    SELECT DISTINCT 
        S.student_id,
        S.student_name,
        S.semester,
        S.cgpa
    FROM 
        StudentSelections SS
    JOIN 
        Students S ON SS.student_id = S.student_id
    WHERE 
        SS.faculty_id = %s;
    '''
    mycursor.execute(query, args = (identry))
    print(identry)
    record = mycursor.fetchall()
    print(record)
    return record


def faculty_dept(id):
    connect_database()
    query = 'select Faculty_dept from faculties where faculty_id = %s'
    mycursor.execute(query, args = (id))
    result = mycursor.fetchone()
    print(result[0])
    return result[0]

def student_cgpa(cgpa):
    connect_database()
    print("need to find the cgpa for this id")
    query = 'select cgpa from students where student_id = %s'
    mycursor.execute(query, args = (cgpa))
    result = mycursor.fetchone()
    if result[0]:
        print(result[0])
        return result[0]
    else:
        print(result[0])
        return None


connect_database()

