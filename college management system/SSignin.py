from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import ttk
import pymysql
import Sdetails

import Student_db


#functionality part

def on_email(event, emailentry):
    if(emailentry.get() == '   Email ID'):
        emailentry.delete(0, END)
def on_enter(event, userentry):
    if(userentry.get() == '   Student ID'):
        userentry.delete(0, END)

def on_pass(event, passentry):
    if(passentry.get() == '   Password'):
        passentry.delete(0, END)

def on_cpass(event, cpassentry):
    if(cpassentry.get() == '   Confirm Password'):
        cpassentry.delete(0, END)

global name
def signin():
    if (emailentry.get() == '' or
        userentry.get() == '' or
        passentry.get() == '' or
        cpassentry.get() == '' or
        emailentry.get() == '   Email ID' or
        userentry.get() == '   Student ID' or
        passentry.get() == '   Password' or
        cpassentry.get() == '   Confirm Password'):
        print('Null Values Present')
        messagebox.showerror(title='Error', message='All Fields are Required')
        print('All Fields are required')
    elif passentry.get() != cpassentry.get():
        print('Passwords mismatch')
        messagebox.showerror(title='Error', message='Passwords are mismatched')
        print('Passwords are mismatched')
    else:
        Student_db.connect_database()
        # stuname = Student_db.student_login(userentry.get())
        stuname = ''
        # print(stuname)
        Student_db.insert_data(userentry.get(), cpassentry.get(), emailentry.get(), stuname)
        # details.open_details(name)
        name = userentry.get()
        signin_window.destroy()
        Sdetails.open_details(name)  # Ensure `open_details` is defined in `details` module

signin_window = Tk()
signin_window.title('SignIn Page')
signin_window.geometry('900x540+100+100')
signin_window.resizable(0, 0)
signin_window.config(bg='white')

img = Image.open(r'Images\5208993.jpg')
img_fix = ImageTk.PhotoImage(image=img)
imglabel = Label(signin_window, image=img_fix, bd=0, bg='white')
imglabel.place(x = 450, y = 100)

headinglabel = Label(signin_window, text='Student Sign In', font=('Open Sans', 30, 'bold'), fg='DarkSlateGray', bd=0, bg = 'white')
headinglabel.place(x = 80, y = 80)

emaillabel = Label(signin_window, text='Email ID', bg='#132E38', fg='white', font=('Microsoft Yahei UI Light', 15, 'bold'), anchor='center', width=11, height=1)
emaillabel.place(x = 60, y = 180)
emailentry = Entry(signin_window, width=20,bg='white', fg='#132E38', font=('Microsoft Yahei UI Light', 12), foreground='black')
emailentry.grid(padx = 178, pady = (180, 0), ipady = 5)
emailentry.insert(0, '   Email ID')
emailentry.bind('<FocusIn>', lambda event: on_email(event, emailentry))

userlabel = Label(signin_window, text='Student ID', bg='#132E38', fg='white', font=('Microsoft Yahei UI Light', 15, 'bold'), anchor='center', width=11, height=1)
userlabel.place(x = 60, y = 240)
userentry = Entry(signin_window, width=20,bg='white', fg='#132E38', font=('Microsoft Yahei UI Light', 12), foreground='black')
userentry.grid(padx = 178, pady = (25, 0), ipady = 5)
userentry.insert(0, '   Student ID')
userentry.bind('<FocusIn>', lambda event: on_enter(event, userentry))

passlabel = Label(signin_window, text='Password', bg='#132E38', fg='white', font=('Microsoft Yahei UI Light', 15, 'bold'), anchor='center', width=11, height=1)
passlabel.place(x = 60, y = 300)
passentry = Entry(signin_window, width=20,bg='white', fg='#132E38', font=('Microsoft Yahei UI Light', 12), foreground='black')
passentry.grid(padx = 198, pady = (25, 0), ipady = 5)
passentry.insert(0, '   Password')
passentry.bind('<FocusIn>', lambda event: on_pass(event, passentry))

cpasslabel = Label(signin_window, text='Password', bg='#132E38', fg='white', font=('Microsoft Yahei UI Light', 15, 'bold'), anchor='center', width=11, height=1)
cpasslabel.place(x = 60, y = 360)
cpassentry = Entry(signin_window, width=20,bg='white', fg='#132E38', font=('Microsoft Yahei UI Light', 12), foreground='black')
cpassentry.grid(padx = 198, pady = (25, 0), ipady = 5)
cpassentry.insert(0, '   Confirm Password')
cpassentry.bind('<FocusIn>', lambda event: on_cpass(event, cpassentry))


signinbutton = Button(signin_window, text='Sign In', width=26, height=1, font=('Microsoft Yahei UI Light', 12, 'bold'), bg='#132E38', fg='white', cursor = 'hand2', command=signin)
signinbutton.place(x = 90, y = 430)

signin_window.mainloop()