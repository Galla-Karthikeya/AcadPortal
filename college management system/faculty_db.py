import pymysql
from tkinter import messagebox


def connect_database():
    global mycursor, conn
    try:
        conn = pymysql.connect(host = 'localhost', user = 'root', password='karthi')
        mycursor = conn.cursor()
    except:
        messagebox.showerror(title = 'Error', message='Connection is not Established')
        return

    try:
        mycursor.execute(query = 'Create database if not exists Collage')
        mycursor.execute(query = 'Use Collage')
        query = '''
        CREATE TABLE faculty_login (
            F_id varchar(50) Not Null,
            F_name VARCHAR(100) Null,
            Password varchar(100),
            Email_id VARCHAR(100),
            PRIMARY KEY (F_id, Email_id)
        );
        '''
        mycursor.execute(query)
        print('Done with the faculty_login table creation')
    except:
        # messagebox.showerror(title = 'Error', message=str(e))
        mycursor.execute('Use Collage')


def search(sub_name, classes):
    query = 'select * from faculty_login where Sub_name = %s and Class = %s'
    mycursor.execute(query, args=(sub_name, classes))
    record = mycursor.fetchone()
    print(record)
    if(record != None):
        print('Already the Subject and ClassRoom was Selected')
        return False
    else:
        return True


def insert_data(id, name, password, email):
    query = 'select * from faculty_login where f_id = %s'
    mycursor.execute(query, args=id)
    record = mycursor.fetchone()
    if(record):
        messagebox.showerror(title='Error', message='Faculty ID already Present')
        return 1
    else:
        query = 'insert into faculty_login(F_id, F_name, Password, Email_Id) values(%s, %s, %s, %s)'
        mycursor.execute(query, args=(id, name, password, email))
        messagebox.showinfo(title='Sucess', message='Record has Created Sucessfully')
        conn.commit()
        return 0

def login_db(user, password):
    query = 'select * from faculty_login where f_id = %s and Password = %s'
    mycursor.execute(query, args= (user, password))
    record = mycursor.fetchone()
    if(record):
        messagebox.showinfo(title='Success', message='Login Successful')
        return True
    else:
        messagebox.showerror(title = 'Error', message= 'Incorrect Credentials')
        return False


def faculty_name(id):
    connect_database()
    query = 'select F_name  from faculty_login where F_id = %s'
    mycursor.execute(query, args = (id))
    result = mycursor.fetchone()
    print(result[0])
    return result[0]

def faculty_email(mail):
    connect_database()
    query = 'select Email_id from faculty_login where F_id = %s'
    mycursor.execute(query, args = (mail))
    result = mycursor.fetchone()
    print(result[0])
    return result[0]


def faculties_import(id):
    query = 'select F_id, F_name, Email_id from faculty_login where F_id = %s'
    mycursor.execute(query, args=(id))
    result = mycursor.fetchall()
    print(id)
    print(result)
    if(result):
        id, name, email = result[0]
        return id, name, email
    else:
        return None


