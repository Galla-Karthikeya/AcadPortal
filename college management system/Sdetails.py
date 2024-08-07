from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import pymysql
import Student_db
import student_faculty
import studentselection

def connect_database():
    global mycursor, conn
    try:
        conn = pymysql.connect(host='localhost', user='root', password='Vaishu@2003')
        mycursor = conn.cursor()
    except Exception as e:
        messagebox.showerror(title='Error', message=f'Connection is not Established: {e}')
        return
    mycursor.execute('USE Collage')

def on_enter(event, entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, END)

def on_leave(event, entry, default_text):
    if entry.get() == '':
        entry.insert(0, default_text)

def update_student_name(student_id, new_name):
    try:
        connect_database()
        query = "UPDATE Student_login SET S_name = %s WHERE S_id = %s"
        values = (new_name, student_id)
        mycursor.execute(query, values)
        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        mycursor.close()
        conn.close()

def enter():
    if name_entry.get() == 'FirstName LastName' or sem_entry.get() == 'Ex: 7':
        messagebox.showerror(title = 'Error', message='All Fields are Required')
    else:
        if cgpa_entry.get() == '':
            student_faculty.insert_students(current_user, name_entry.get(), 0, sem_entry.get())
        else:
            student_faculty.insert_students(current_user, name_entry.get(), cgpa_entry.get(), sem_entry.get())
        update_student_name(current_user, name_entry.get())
        details_window.destroy()
        print(current_user)
        studentselection.open_details(current_user)



def open_details(username):
    global current_user, name_entry, cgpa_entry, sem_entry, details_window
    current_user = username
    print(f"This is the username: {username}")
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

    headinglabel = Label(details_window, text='Enter your Details here!!', font=('Open Sans', 25, 'bold'), fg='DarkSlateGray', bd=0, bg='white')
    headinglabel.place(x=90, y=80)

    name_label = Label(details_window, text="Your Name", font=('Open Sans', 15), fg='DarkSlateGray', bd=1, bg='white')
    name_label.place(x=90, y=150)
    name_entry = Entry(details_window, width=25, bg='white', font=('Microsoft Yahei UI Light', 11), bd=0)
    name_entry.place(x=90, y=180)
    name_entry.insert(0, "FirstName LastName")
    name_entry.bind('<FocusIn>', lambda event: on_enter(event, name_entry, 'FirstName LastName'))
    name_entry.bind('<FocusOut>', lambda event: on_leave(event, name_entry, 'FirstName LastName'))
    frame = Frame(details_window, width=255, bg='black', height=1)
    frame.place(x=90, y=205)

    cgpa_label = Label(details_window, text="CGPA", font=('Open Sans', 14), fg='DarkSlateGray', bg='white')
    cgpa_label.place(x=90, y=225)
    cgpa_entry = Entry(details_window, width=25, bg='white', font=('Microsoft Yahei UI Light', 11), bd=0)
    cgpa_entry.place(x=90, y=255)
    cgpa_entry.insert(0, "Ex: 8.7")
    cgpa_entry.bind('<FocusIn>', lambda event: on_enter(event, cgpa_entry, 'Ex: 8.7'))
    cgpa_entry.bind('<FocusOut>', lambda event: on_leave(event, cgpa_entry, 'Ex: 8.7'))
    frame = Frame(details_window, width=255, bg='black', height=1)
    frame.place(x=90, y=278)

    sem_label = Label(details_window, text="Semester", font=('Open Sans', 14), fg='DarkSlateGray', bg='white')
    sem_label.place(x=90, y=300)
    sem_entry = Entry(details_window, width=25, bg='white', font=('Microsoft Yahei UI Light', 12), bd=0)
    sem_entry.place(x=90, y=330)
    sem_entry.insert(0, "Ex: 7")
    sem_entry.bind('<FocusIn>', lambda event: on_enter(event, sem_entry, 'Ex: 7'))
    sem_entry.bind('<FocusOut>', lambda event: on_leave(event, sem_entry, 'Ex: 7'))
    frame = Frame(details_window, width=255, bg='black', height=1)
    frame.place(x=90, y=353)

    enterbutton = Button(details_window, text="Go To Home Page", font=('Open Sans', 15), fg='white', bg='DarkSlateGray', command = enter)
    enterbutton.place(x=120, y=380)

    details_window.mainloop()

# if __name__ == "__main__":
#     open_details('S001')
