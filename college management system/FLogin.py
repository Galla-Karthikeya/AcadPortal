from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import student_faculty
import pymysql

import faculty_db
import faculty_home



def sign():
    login_window.destroy()
    import FSignin


#functionality part
def on_enter(event, userentry):
    if(userentry.get() == 'UserName'):
        userentry.delete(0, END)

def on_pass(event, passentry):
    if(passentry.get() == 'Password'):
        passentry.delete(0, END)

def login():
    global faculty_user
    if(userentry.get() == '' or passentry.get() == ''):
        messagebox.showerror(title='Error', message='All Fields are Required')
    else:
        faculty_db.connect_database()
        if(faculty_db.login_db(userentry.get(), passentry.get())):
            faculty_user = userentry.get()
            # id, name, email = faculty_db.faculties_import(faculty_user)
            # student_faculty.insert_faculties(id, name, email)
            login_window.destroy()
            faculty_home.homef(faculty_user)



login_window = Tk()
login_window.title('Login Page')
login_window.geometry('900x540+100+100')
login_window.resizable(0, 0)
login_window.config(bg='white')

img = Image.open(r'Images\46695752.jpg')
img_fix = ImageTk.PhotoImage(image=img, size=(500, 500))
imglabel = Label(login_window, image=img_fix, bd=0, bg='white')
imglabel.place(x = 450, y = 100)

headinglabel = Label(login_window, text='Faculty Login', font=('Open Sans', 30, 'bold'), fg='DarkSlateGray', bd=0, bg = 'white')
headinglabel.place(x = 90, y = 80)

# emaillabel = Label(login_window, text='Email', bg='white', bd=0, fg='DarkSlateGray', font=('Microsoft Yahei UI Light', 15, 'bold'))
# emaillabel.place(x = 100, y = 180)
# emailentry = Entry(login_window, width=26, bg='white', bd=0, fg='#132E38', font=('Microsoft Yahei UI Light', 12), foreground='black')
# emailentry.place(x = 100, y = 214)
# frame = Frame(width=250, height=1, bg='#FF4D22')
# frame.place(x = 100, y = 240)

userlabel = Label(login_window, text='Faculty ID', fg='DarkSlateGray', font=('Microsoft Yahei UI Light', 15, 'bold'), anchor='center', width=20)
userlabel.place(x = 90, y = 180)
userentry = Entry(login_window, width=25,bg='white', fg='#132E38', font=('Microsoft Yahei UI Light', 12), foreground='black')
userentry.grid(padx = 90, pady = (210, 0), ipadx = 9, ipady = 2)
userentry.insert(0, 'UserName')
userentry.bind('<FocusIn>', lambda event: on_enter(event, userentry))

passlabel = Label(login_window, text='Password', fg='DarkSlateGray', font=('Microsoft Yahei UI Light', 15, 'bold'), anchor='center', width=20)
passlabel.place(x = 90, y = 275)
passentry = Entry(login_window, width=25,bg='white', fg='#132E38', font=('Microsoft Yahei UI Light', 12), foreground='black')
passentry.grid(padx = 90, pady = (70, 0), ipadx = 9, ipady = 2)
passentry.insert(0, 'Password')
passentry.bind('<FocusIn>', lambda event: on_pass(event, passentry))

signinbutton = Button(login_window, text='SignIn', width=10, height=1, font=('Microsoft Yahei UI Light', 10, 'bold'), fg='#132E38', bg='white', bd=0, cursor='hand2', activebackground='white', activeforeground='orange', command = sign)
signinbutton.place(x = 65, y = 345)

forgotbutton = Button(login_window, text='Forgot Password', width=15, height=1, font=('Microsoft Yahei UI Light', 10, 'bold'), fg='#132E38', bg='white', bd=0, cursor='hand2', activebackground='white', activeforeground='orange')
forgotbutton.place(x = 215, y = 345)

loginbutton = Button(login_window, text='Login', width=26, height=1, font=('Microsoft Yahei UI Light', 10, 'bold'), bg='#132E38', fg='white', cursor = 'hand2', command=login)
loginbutton.place(x = 90, y = 400)

login_window.mainloop()