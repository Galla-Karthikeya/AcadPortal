from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import pymysql

def ask_question():
    response = messagebox.askyesno("Confirmation", "Do you want to add more subjects?")
    if response:
        print("User clicked Yes")
    else:
        print("User clicked No")
        details_window.destroy()
        import FLogin



def connect_database():
    global mycursor, conn
    try:
        conn = pymysql.connect(host='localhost', user='root', password='karthi')
        mycursor = conn.cursor()
    except Exception as e:
        messagebox.showerror(title='Error', message=f'Connection is not Established: {e}')
        return
    mycursor.execute('USE Collage')


def fetch_faculty_name(faculty_id):
    try:
        connect_database()
        query = "SELECT faculty_name FROM faculties WHERE faculty_id = %s"
        mycursor.execute(query, (faculty_id,))
        result = mycursor.fetchone()
        print(f"Name: {result}")
        return result[0] if result else "Unknown"
    except Exception as e:
        messagebox.showerror(title='Error', message=f'Error fetching faculty name: {e}')
        return "Unknown"
    finally:
        mycursor.close()
        conn.close()


def fetch_subject_code(subject_name):
    try:
        connect_database()
        query = "SELECT subject_code FROM subjects WHERE subject_name = %s"
        mycursor.execute(query, (subject_name,))
        result = mycursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        messagebox.showerror(title='Error', message=f'Error fetching subject code: {e}')
        return None
    finally:
        mycursor.close()
        conn.close()


def check_faculty_assignment(faculty_name, subject_name, classroom):
    try:
        connect_database()
        query = "SELECT * FROM facultyassignments WHERE faculty_name = %s AND subject_name = %s AND class_number = %s"
        mycursor.execute(query, (faculty_name, subject_name, classroom))
        result = mycursor.fetchone()
        return result is not None
    except Exception as e:
        messagebox.showerror(title='Error', message=f'Error checking assignment: {e}')
        return True
    finally:
        mycursor.close()
        conn.close()


def check_faculty_subject(faculty_name, subject_name):
    try:
        connect_database()
        query = "SELECT * FROM facultyassignments WHERE faculty_name = %s AND subject_name = %s"
        mycursor.execute(query, (faculty_name, subject_name))
        result = mycursor.fetchone()
        return result is not None
    except Exception as e:
        messagebox.showerror(title='Error', message=f'Error checking assignment: {e}')
        return True
    finally:
        mycursor.close()
        conn.close()


def insert_faculty_assignment(faculty_id, faculty_name, subject_name, classroom):
    try:
        subject_code = fetch_subject_code(subject_name)
        if not subject_code:
            messagebox.showerror(title='Error', message=f'No subject code found for subject: {subject_name}')
            return

        connect_database()
        query = "INSERT INTO facultyassignments (faculty_id, faculty_name, subject_code, subject_name, class_number) VALUES (%s, %s, %s, %s, %s)"
        values = (faculty_id, faculty_name, subject_code, subject_name, classroom)
        mycursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Success", "Assignment added successfully.")
        ask_question()
    except Exception as e:
        conn.rollback()
        messagebox.showerror(title='Error', message=f'Error inserting assignment: {e}')
    finally:
        mycursor.close()
        conn.close()


def enter():
    subject_name = subjects_combobox.get()
    classroom = classroom_combobox.get()

    if subject_name == '' or classroom == '':
        messagebox.showerror(title='Error', message='All Fields are Required')
    else:
        faculty_name = faculty_name_var.get()
        faculty_id = current_user

        if check_faculty_assignment(faculty_name, subject_name, classroom):
            messagebox.showerror("Error",f"Faculty {faculty_name} already selected the subject {subject_name} in classroom {classroom}.")
        elif check_faculty_subject(faculty_name, subject_name):
            messagebox.showerror("Error", f"Faculty {faculty_name} already selected the subject {subject_name}.")
        else:
            insert_faculty_assignment(faculty_id, faculty_name, subject_name, classroom)


def open_details(username):
    global current_user, faculty_name_var, subjects_combobox, classroom_combobox, details_window
    current_user = username
    print(current_user)
    faculty_name = fetch_faculty_name(current_user)

    details_window = Tk()
    details_window.title('Faculty Assignment')
    details_window.geometry('900x540+100+100')
    details_window.resizable(0, 0)
    details_window.config(bg='white')

    # Load and place the image
    img = Image.open(r'Images\3627634.jpg')
    img = img.resize((300, 300), Image.LANCZOS)
    img_fix = ImageTk.PhotoImage(img)
    imglabel = Label(details_window, image=img_fix, bd=0, bg='white')
    imglabel.place(x=500, y=150)

    headinglabel = Label(details_window, text='Enter your Details here!!', font=('Open Sans', 25, 'bold'),
                         fg='DarkSlateGray', bd=0, bg='white')
    headinglabel.place(x=90, y=80)

    name_label = Label(details_window, text="Faculty Name", font=('Open Sans', 15), fg='DarkSlateGray', bd=1,
                       bg='white')
    name_label.place(x=90, y=150)
    faculty_name_var = StringVar(value=faculty_name)
    faculty_name_entry = Entry(details_window, textvariable=faculty_name_var, state='readonly', width=25, bg='white',
                               font=('Microsoft Yahei UI Light', 11), bd=0)
    faculty_name_entry.place(x=90, y=180)
    frame = Frame(details_window, width=255, bg='black', height=1)
    frame.place(x=90, y=205)

    subjects_label = Label(details_window, text="Subjects", font=('Open Sans', 14), fg='DarkSlateGray', bg='white')
    subjects_label.place(x=90, y=225)
    subjects_combobox = ttk.Combobox(details_window,
                                     values=["Data Structures", "Machine Learning", "Deep Learning", "CLAD",
                                             "Digital Logic Circuits"], font=('Microsoft Yahei UI Light', 11),
                                     state="readonly")
    subjects_combobox.place(x=90, y=255)

    classroom_label = Label(details_window, text="Classroom", font=('Open Sans', 14), fg='DarkSlateGray', bg='white')
    classroom_label.place(x=90, y=300)
    classroom_combobox = ttk.Combobox(details_window, values=[101, 102, 103, 104, 105],
                                      font=('Microsoft Yahei UI Light', 12), state="readonly")
    classroom_combobox.place(x=90, y=330)

    enterbutton = Button(details_window, text="Go To Home Page", font=('Open Sans', 15), fg='white', bg='DarkSlateGray',
                         command=enter)
    enterbutton.place(x=120, y=380)

    details_window.mainloop()

# open_details('F001')