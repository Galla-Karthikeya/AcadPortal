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
        CREATE TABLE student_login (
            S_id varchar(100) Not Null,
            S_name VARCHAR(100) Null,
            Password varchar(100),
            Email_id VARCHAR(100),
            PRIMARY KEY (S_id, Email_id)
        );
        '''
        mycursor.execute(query)
        print('Done with the student_login table creation')
    except:
        # messagebox.showerror(title = 'Error', message=str(e))
        mycursor.execute('Use Collage')
        query = '''
                CREATE TABLE if not exists student_login (
                    S_id varchar(100),
                    S_name VARCHAR(100),
                    Password varchar(100),
                    Email_id VARCHAR(100),
                    PRIMARY KEY (S_id, Email_id)
                );
                '''
        mycursor.execute(query)
        print('Done with the student_login table creation')


# def student_login(value):
#     if(value == 'S001'):
#         return 'Alice Johnson'
#     elif(value == 'S002'):
#         return 'Bob Smith'
#     elif(value == 'S003'):
#         return 'Carol White'
#     elif(value == 'S004'):
#         return 'David Brown'
#     elif (value == 'S005'):
#         return 'Eve Black'
#     else:
#         messagebox.showerror(title='Error', message='student_login Id is Not Present')

def search(sub_name, classes):
    query = 'select * from student_login where Sub_name = %s and Class = %s'
    mycursor.execute(query, args=(sub_name, classes))
    record = mycursor.fetchone()
    print(record)
    if(record != None):
        print('Already the Subject and ClassRoom was Selected')
        return False
    else:
        return True


def insert_data(id, password, email, name):
    # result = search(sub_name, classes)
    # if(result):
    #     query = 'insert into student_login(S_id, S_name, Password, Email_Id) values(%s, %s, %s, %s)'
    #     mycursor.execute(query, args=(id, name, password, email))
    #     messagebox.showinfo(title='Sucess', message='Record has Created Sucessfully')
    #     conn.commit()
    # else:
    #     messagebox.showerror(title = 'Error', message='Already The Subject and the ClassRoom was Selected')
    query = 'insert into student_login(S_id, S_name, Password, Email_Id) values(%s, %s, %s, %s)'
    mycursor.execute(query, args=(id, name, password, email))
    print(mycursor.fetchone())
    messagebox.showinfo(title='Sucess', message='Record has Created Sucessfully')
    conn.commit()

def login_db(user, password):
    query = 'select * from student_login where S_id = %s and Password = %s'
    mycursor.execute(query, args= (user, password))
    record = mycursor.fetchone()
    if(record):
        messagebox.showinfo(title='Sucess', message='Login Sucessfull')
        return True
    else:
        messagebox.showerror(title = 'Error', message= 'Incorrect Credentials')
        return False






# printing student_login name:
def student_name(id):
    connect_database()
    query = 'select S_name from student_login where S_id = %s'
    mycursor.execute(query, args = (id))
    result = mycursor.fetchone()
    print(id)
    print(result[0])
    return result[0]

def student_email(mail):
    connect_database()
    query = 'select Email_id  from student_login where S_id = %s'
    mycursor.execute(query, args = (mail))
    result = mycursor.fetchone()
    print(result[0])
    return result[0]


def students_import(id):
    query = 'select S_id, S_name, Email_id from student_login where S_id = %s'
    mycursor.execute(query, args=(id))
    result = mycursor.fetchall()
    if(result):
        id, name, email = result
        return id, name, email
    else:
        return None
