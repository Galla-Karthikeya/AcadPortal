from tkinter import *
from tkinter import messagebox, ttk
from PIL import ImageTk, Image
import pymysql


def connect_database():
    global mycursor, conn
    try:
        conn = pymysql.connect(host='localhost', user='root', password='karthi')
        mycursor = conn.cursor()
    except Exception as e:
        messagebox.showerror(title='Error', message=f'Connection is not Established: {e}')
        return
    mycursor.execute('USE Collage')


def fetch_student_name(student_id):
    try:
        connect_database()
        query = "SELECT student_name FROM students WHERE student_id = %s"
        mycursor.execute(query, (student_id,))
        result = mycursor.fetchone()
        return result[0] if result else "Unknown"
    except Exception as e:
        messagebox.showerror(title='Error', message=f'Error fetching student name: {e}')
        return "Unknown"
    finally:
        mycursor.close()
        conn.close()


def fetch_faculties():
    try:
        connect_database()
        query = "SELECT DISTINCT faculty_name FROM facultyassignments"
        mycursor.execute(query)
        result = mycursor.fetchall()
        return [row[0] for row in result]
    except Exception as e:
        messagebox.showerror(title='Error', message=f'Error fetching faculties: {e}')
        return []
    finally:
        mycursor.close()
        conn.close()


def fetch_subjects(faculty_name):
    try:
        connect_database()
        query = "SELECT subject_name FROM facultyassignments WHERE faculty_name = %s"
        mycursor.execute(query, (faculty_name,))
        result = mycursor.fetchall()
        return [row[0] for row in result]
    except Exception as e:
        messagebox.showerror(title='Error', message=f'Error fetching subjects: {e}')
        return []
    finally:
        mycursor.close()
        conn.close()


def fetch_class_number(faculty_name, subject_name):
    try:
        connect_database()
        query = "SELECT class_number FROM facultyassignments WHERE faculty_name = %s AND subject_name = %s"
        mycursor.execute(query, (faculty_name, subject_name))
        result = mycursor.fetchone()
        return result[0] if result else "Unknown"
    except Exception as e:
        messagebox.showerror(title='Error', message=f'Error fetching class number: {e}')
        return "Unknown"
    finally:
        mycursor.close()
        conn.close()

def fetch_faculty_id(faculty_name):
    try:
        connect_database()
        query = "SELECT faculty_id FROM facultyassignments WHERE faculty_name = %s LIMIT 1"
        mycursor.execute(query, (faculty_name,))
        result = mycursor.fetchone()
        return result[0] if result else "Unknown"
    except Exception as e:
        messagebox.showerror(title='Error', message=f'Error fetching faculty id: {e}')
        return "Unknown"
    finally:
        mycursor.close()
        conn.close()

def fetch_subject_code(faculty_name, subject_name):
    try:
        connect_database()
        query = "SELECT subject_code FROM facultyassignments WHERE faculty_name = %s AND subject_name = %s"
        mycursor.execute(query, (faculty_name, subject_name))
        result = mycursor.fetchone()
        return result[0] if result else "Unknown"
    except Exception as e:
        messagebox.showerror(title='Error', message=f'Error fetching subject code: {e}')
        return "Unknown"
    finally:
        mycursor.close()
        conn.close()

def insert_student_selection(student_id, subject_code, faculty_id):
    try:
        connect_database()
        query = "INSERT INTO studentselections (student_id, subject_code, faculty_id) VALUES (%s, %s, %s)"
        values = (student_id, subject_code, faculty_id)
        mycursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Success", "Selection added successfully.")
    except Exception as e:
        conn.rollback()
        messagebox.showerror(title='Error', message=f'Error inserting selection: {e}')
    finally:
        mycursor.close()
        conn.close()

def check_student_subject(student_id, subject_code):
    try:
        connect_database()
        query = "SELECT * FROM studentselections WHERE student_id = %s AND subject_code = %s"
        mycursor.execute(query, (student_id, subject_code))
        result = mycursor.fetchone()
        return result is not None
    except Exception as e:
        messagebox.showerror(title='Error', message=f'Error checking assignment: {e}')
        return True
    finally:
        mycursor.close()
        conn.close()

def enter():
    if faculty_combobox.get() == '' or subject_combobox.get() == '' or class_entry.get() == 'Unknown':
        messagebox.showerror(title='Error', message='All Fields are Required')
    else:
        student_id = current_user
        faculty_name = faculty_combobox.get()
        subject_name = subject_combobox.get()
        class_number = class_entry.get()

        subject_code = fetch_subject_code(faculty_name, subject_name)
        faculty_id = fetch_faculty_id(faculty_name)

        if subject_code == "Unknown" or faculty_id == "Unknown":
            messagebox.showerror(title='Error', message='Failed to retrieve subject code or faculty id.')
        else:
            if check_student_subject(student_id, subject_code):
                messagebox.showerror("Error", f"You have already selected the subject {subject_name}.")
            else:
                insert_student_selection(student_id, subject_code, faculty_id)

                response = messagebox.askyesno("Success","Assignment added successfully. Do you want to select another faculty and subject?")
                if response:
                    print("User clicked 'Yes'")
                    pass
                else:
                    print("User clicked 'No'")
                    details_window.destroy()
                    import SLogin


def on_faculty_select(event):
    faculty_name = faculty_combobox.get()
    subjects = fetch_subjects(faculty_name)
    subject_combobox['values'] = subjects


def on_subject_select(event):
    faculty_name = faculty_combobox.get()
    subject_name = subject_combobox.get()
    class_number = fetch_class_number(faculty_name, subject_name)
    class_entry.config(state=NORMAL)
    class_entry.delete(0, END)
    class_entry.insert(0, class_number)
    class_entry.config(state='readonly')


def open_details(username):
    global current_user, faculty_combobox, subject_combobox, class_entry, details_window
    current_user = username
    student_name = fetch_student_name(current_user)

    details_window = Tk()
    details_window.title('Login Page')
    details_window.geometry('900x540+100+100')
    details_window.resizable(0, 0)
    details_window.config(bg='white')

    # Load and place the image
    img = Image.open(r'Images\3627634.jpg')
    img = img.resize((300, 300), Image.LANCZOS)
    img_fix = ImageTk.PhotoImage(img)
    imglabel = Label(details_window, image=img_fix, bd=0, bg='white')
    imglabel.place(x=550, y=150)

    headinglabel = Label(details_window, text='Enter your Details here!!', font=('Open Sans', 25, 'bold'),
                         fg='DarkSlateGray', bd=0, bg='white')
    headinglabel.place(x=90, y=80)

    name_label = Label(details_window, text="Student Name", font=('Open Sans', 15), fg='DarkSlateGray', bd=1,
                       bg='white')
    name_label.place(x=90, y=150)
    name_entry = Entry(details_window, width=25, bg='white', font=('Microsoft Yahei UI Light', 11), bd=0)
    name_entry.place(x=90, y=180)
    name_entry.insert(0, student_name)
    name_entry.config(state='readonly')
    frame = Frame(details_window, width=200, bg='black', height=1)
    frame.place(x=90, y=205)

    faculty_label = Label(details_window, text="Faculty Name", font=('Open Sans', 14), fg='DarkSlateGray', bg='white')
    faculty_label.place(x=90, y=225)
    faculty_combobox = ttk.Combobox(details_window, values=fetch_faculties(), font=('Microsoft Yahei UI Light', 11),
                                    state="readonly")
    faculty_combobox.place(x=90, y=255)
    faculty_combobox.bind("<<ComboboxSelected>>", on_faculty_select)

    subject_label = Label(details_window, text="Subject Name", font=('Open Sans', 14), fg='DarkSlateGray', bg='white')
    subject_label.place(x=90, y=300)
    subject_combobox = ttk.Combobox(details_window, font=('Microsoft Yahei UI Light', 11), state="readonly")
    subject_combobox.place(x=90, y=330)
    subject_combobox.bind("<<ComboboxSelected>>", on_subject_select)

    class_label = Label(details_window, text="Class Number", font=('Open Sans', 14), fg='DarkSlateGray', bg='white')
    class_label.place(x=90, y=375)
    class_entry = Entry(details_window, width=25, bg='white', font=('Microsoft Yahei UI Light', 11), bd=0,
                        state='readonly')
    class_entry.place(x=90, y=405)
    frame = Frame(details_window, width=200, bg='black', height=1)
    frame.place(x=90, y=430)

    enterbutton = Button(details_window, text="Register", font=('Open Sans', 15), fg='white', bg='DarkSlateGray',
                         command=enter)
    enterbutton.place(x=120, y=480)

    details_window.mainloop()


# Example usage
if __name__ == "__main__":
    open_details('S003')