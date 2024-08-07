from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import Student_db
import Student_home
import student_faculty
import studentselection

# Global variable to store the username
current_user = None

# Functionality part
def on_enter(event, userentry):
    if userentry.get() == 'UserName':
        userentry.delete(0, END)

def on_entry_out(event, userentry):
    if userentry.get() == '':
        userentry.insert(0, 'UserName')

def on_focus_in(event, passentry):
    if passentry.get() == 'Password':
        passentry.delete(0, END)

def on_focus_out(event, passentry):
    if passentry.get() == '':
        passentry.insert(0, 'Password')

def login():
    global current_user
    if userentry.get() == '' or passentry.get() == '':
        messagebox.showerror(title='Error', message='All Fields are Required')
    else:
        Student_db.connect_database()
        if Student_db.login_db(userentry.get(), passentry.get()):
            current_user = userentry.get()
            print(current_user)
            login_window.destroy()
            Student_home.homes(current_user)

def signin():
    login_window.destroy()
    import SSignin

# def gotosubjects():
#     studentselection.open_details(current_user)


# global userentry, passentry, login_window
login_window = Tk()
login_window.title('Login Page')
login_window.geometry('900x540+100+100')
login_window.resizable(0, 0)
login_window.config(bg='white')

img = Image.open(r'Images\4529183.jpg')
img_fix = ImageTk.PhotoImage(image=img, size=(300, 300))
imglabel = Label(login_window, image=img_fix, bd=0, bg='white')
imglabel.place(x=450, y=100)

headinglabel = Label(login_window, text='Student Login', font=('Open Sans', 30, 'bold'), fg='DarkSlateGray', bd=0, bg='white')
headinglabel.place(x=90, y=80)

userlabel = Label(login_window, text='Student ID', fg='DarkSlateGray', font=('Microsoft Yahei UI Light', 15, 'bold'), anchor='center', width=20)
userlabel.place(x=90, y=180)
userentry = Entry(login_window, width=25, bg='white', fg='#132E38', font=('Microsoft Yahei UI Light', 12), foreground='black')
userentry.grid(padx=90, pady=(210, 0), ipadx=9, ipady=2)
userentry.insert(0, 'UserName')
userentry.bind('<FocusIn>', lambda event: on_enter(event, userentry))
userentry.bind('<FocusOut>', lambda event: on_entry_out(event, userentry))

passlabel = Label(login_window, text='Password', fg='DarkSlateGray', font=('Microsoft Yahei UI Light', 15, 'bold'), anchor='center', width=20)
passlabel.place(x=90, y=275)
passentry = Entry(login_window, width=25, bg='white', fg='#132E38', font=('Microsoft Yahei UI Light', 12), foreground='black')
passentry.grid(padx=90, pady=(70, 0), ipadx=9, ipady=2)
passentry.insert(0, 'Password')
passentry.bind('<FocusIn>', lambda event: on_focus_in(event, passentry))
passentry.bind('<FocusOut>', lambda event: on_focus_out(event, passentry))

signinbutton = Button(login_window, text='Sign In', width=10, height=1, font=('Microsoft Yahei UI Light', 10, 'bold'), fg='#132E38', bg='white', bd=0, cursor='hand2', activebackground='white', activeforeground='orange', command=signin)
signinbutton.place(x=65, y=345)

forgotbutton = Button(login_window, text='Forgot Password', width=15, height=1, font=('Microsoft Yahei UI Light', 10, 'bold'), fg='#132E38', bg='white', bd=0, cursor='hand2', activebackground='white', activeforeground='orange')
forgotbutton.place(x=215, y=345)

# select_subject_button = Button(login_window, text='Sign In', width=10, height=1, font=('Microsoft Yahei UI Light', 10, 'bold'), fg='#132E38', bg='white', bd=0, cursor='hand2', activebackground='white', activeforeground='orange', command=gotosubjects)
# select_subject_button.place(x=65, y=380)

loginbutton = Button(login_window, text='Login', width=26, height=1, font=('Microsoft Yahei UI Light', 10, 'bold'), bg='#132E38', fg='white', command=login)
loginbutton.place(x=90, y=420)

login_window.mainloop()
