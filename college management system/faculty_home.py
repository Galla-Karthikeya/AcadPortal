from customtkinter import *
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import student_faculty
import faculty_db
from tkinter import messagebox

def showall():
    show = student_faculty.showalls(identry.get())
    if show:
        tree2.delete(*tree2.get_children())
        for item in show:
            tree2.insert('', 'end', values=(item[0], item[1], item[2], item[3]))
    else:
        print("No student data found.")

def insert_button_click(event=None):
    selected_subject = searchbox.get()
    faculty_name = nameentry.get()

    if selected_subject == 'Search By':
        classentry.delete(0, tk.END)
        classentry.insert(0, '')
    else:
        class_number = student_faculty.classfound(faculty_name, selected_subject)
        print(class_number)
        classentry.delete(0, tk.END)
        if class_number:
            print(f"Class entry is {class_number}")
            classentry.insert(0, class_number)
        else:
            print(f"Class entry is null")
            classentry.insert(0, '')

def insert_data2():
    faculty_id = identry.get()
    sub_code = student_faculty.subcode(searchbox.get())
    print(sub_code)
    data2 = student_faculty.student_details(sub_code, faculty_id)
    tree2.delete(*tree2.get_children())
    if data2:
        for item in data2:
            tree2.insert('', 'end', values=(item[0], item[1], item[2], item[3]))
    else:
        print("No student data found.")

def search():
    if searchbox.get() == 'Search By':
        messagebox.showerror(title='Error', message='Select any field in Search Box')
    elif classentry.get() == '':
        messagebox.showerror(title='Error', message='Faculty Not Selected the subject')
    else:
        insert_data2()

def homef(id):
    global user_id
    global identry, searchbox, classentry, nameentry, tree2, emailentry
    user_id = id
    shome = ctk.CTk()
    shome.title('Home Page')
    shome.config(bg='white')
    shome.geometry('900x540+100+100')
    shome.resizable(False, False)

    # Configure grid to allocate 20% height to homeframe and 80% to the rest
    shome.grid_rowconfigure(0, weight=3)  # 20% of the height
    shome.grid_rowconfigure(1, weight=8)  # 80% of the height
    shome.grid_columnconfigure(0, weight=1)

    # Define common styling for the widgets
    label_font = ('Open Sans', 18, 'bold')
    entry_font = ('Open Sans', 12)
    label_color = 'white'
    entry_color = 'DarkSlateGray'
    text_color = 'white'

    # Create home frame (20% of height)
    homeframe = CTkFrame(shome, fg_color='DarkSlateGray', border_color='white')
    homeframe.grid(row=0, column=0, sticky='nsew', pady = 10, ipady =5)

    # Configure grid of homeframe to center leftframe and rightframe with a gap between them
    homeframe.grid_rowconfigure(0, weight=1)
    homeframe.grid_rowconfigure(2, weight=1)
    homeframe.grid_columnconfigure(0, weight=1)
    homeframe.grid_columnconfigure(1, weight=1)  # Add a column for spacing
    homeframe.grid_columnconfigure(2, weight=1)
    homeframe.grid_columnconfigure(3, weight=1)
    homeframe.grid_columnconfigure(4, weight=1)  # Add another column for email entry

    # Create left frame
    leftframe = CTkFrame(homeframe, fg_color='DarkSlateGray', width=1000)
    leftframe.grid(row=1, column=3, padx=100, pady=15, sticky='nsew')

    # Reg ID and Name to the left
    idlabel = CTkLabel(leftframe, text='Faculty Id', font=label_font, text_color='white', bg_color='DarkSlateGray')
    idlabel.grid(row=0, column=0, padx=(5, 20), pady=5, sticky='w')
    identry = CTkEntry(leftframe, font=entry_font, width=180, fg_color='DarkSlateGray', text_color='white')
    identry.grid(row=0, column=1, padx=(0, 10), pady=0)
    identry.insert(0, user_id)
    identry.configure(state='readonly')

    namelabel = CTkLabel(leftframe, text='Name', font=label_font, text_color='white', bg_color='DarkSlateGray')
    namelabel.grid(row=1, column=0, padx=(5, 20), pady=5, sticky='w')
    nameentry = CTkEntry(leftframe, font=entry_font, width=180, fg_color='DarkSlateGray', text_color='white')
    nameentry.grid(row=1, column=1, pady=(0, 0), padx=(0, 10))
    nameentry.insert(0, faculty_db.faculty_name(user_id))
    nameentry.configure(state='readonly')

    # Email ID and Dept to the right
    emaillabel = CTkLabel(leftframe, text='Email ID', font=label_font, text_color='white', bg_color='DarkSlateGray')
    emaillabel.grid(row=0, column=2, padx=(50, 20), pady=5, sticky='e')
    emailentry = CTkEntry(leftframe, font=entry_font, width=180, fg_color='DarkSlateGray', text_color='white')
    emailentry.grid(row=0, column=3, padx=(0, 10), pady=0)
    emailentry.insert(0, faculty_db.faculty_email(user_id))
    emailentry.configure(state='readonly')

    deptlabel = CTkLabel(leftframe, text='Dept', font=label_font, text_color='white', bg_color='DarkSlateGray')
    deptlabel.grid(row=1, column=2, padx=(50, 20), pady=5, sticky='e')
    deptentry = CTkEntry(leftframe, font=entry_font, width=180, fg_color='DarkSlateGray', text_color='white')
    deptentry.grid(row=1, column=3, pady=(0, 0), padx=(0, 10))
    deptentry.insert(0, student_faculty.faculty_dept(user_id))
    deptentry.configure(state='readonly')

    # Placeholder for tree view (20% of height)
    contentframe = CTkFrame(shome, fg_color='white')
    contentframe.grid(row=1, column=0, sticky='nsew', pady=(10, 0))

    # Configure grid columns of contentframe
    contentframe.grid_rowconfigure(0, weight=1)
    contentframe.grid_columnconfigure(0, weight=2)  # 20% width for tree
    contentframe.grid_columnconfigure(1, weight=8)  # 80% width for rightframe

    # Create leftframe in contentframe
    leftframe_content = CTkFrame(contentframe, fg_color='white', bg_color='white', corner_radius=20)
    leftframe_content.grid(row=0, column=0, sticky='nsew', pady=10)

    # Create a Treeview widget in leftframe_content
    tree_left = ttk.Treeview(leftframe_content, columns=('Subject Code', 'Subject Name'), show='headings', height=12)
    tree_left.heading('Subject Code', text='Subject Code')
    tree_left.heading('Subject Name', text='Subject Name')

    tree_left.column('Subject Code', anchor=tk.CENTER, width=120)
    tree_left.column('Subject Name', anchor=tk.CENTER, width=180)
    tree_left.grid(row=0, column=0, sticky='nsew', pady=10)

    # Style the Treeview
    style = ttk.Style()
    style.configure('Treeview.Heading', font=('arial', 12, 'bold'), background='white', foreground='white')
    style.configure('Treeview', font=('arial', 10), rowheight=30, background='white', foreground=text_color)

    # Create a vertical scrollbar
    scrollbar_left = ttk.Scrollbar(leftframe_content, orient=tk.VERTICAL, command=tree_left.yview)
    scrollbar_left.grid(row=0, column=1, sticky='ns')

    # Link the scrollbar with the Treeview
    tree_left.config(yscrollcommand=scrollbar_left.set)

    def insert_data1():
        data = student_faculty.subjects(nameentry.get())  # Replace with your data-fetching command
        print(f'{data} from the subjects table')
        for item in data:
            tree_left.insert('', 'end', values=(item[0], item[1]))

    # Call the function to insert data
    insert_data1()

    # Create right frame (80% width)
    rightframe = CTkFrame(contentframe, bg_color='white', corner_radius=20, fg_color='DarkSlateGray')
    rightframe.grid(row=0, column=1, sticky='nsew', pady=10)

    # Grid configuration for rightframe contents
    rightframe.grid_rowconfigure(0, weight=1, minsize=50)  # Adjust the height of row 0
    rightframe.grid_columnconfigure(0, weight=1, minsize=100)  # Adjust the width of columns 0, 1, 2, 3
    rightframe.grid_columnconfigure(1, weight=1, minsize=100)
    rightframe.grid_columnconfigure(2, weight=1, minsize=100)
    rightframe.grid_columnconfigure(3, weight=1, minsize=100)

    search_options = ['Search By', 'Data Structures', 'Machine Learning', 'Deep Learning', 'CLAD',
                      'Digital Logic Circuits']
    searchbox = CTkComboBox(rightframe, values=search_options, state='readonly', command=insert_button_click, fg_color='white', text_color='DarkSlateGray')
    searchbox.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    searchbox.set('Search By')

    classentry = CTkEntry(rightframe, font=('arial', 15, 'bold'), fg_color='white', text_color='DarkSlateGrey')
    classentry.grid(row=0, column=1, padx=10, pady=10, sticky='e')
    classentry.insert(0, student_faculty.classfound(nameentry.get(), searchbox.get()))
    print(student_faculty.classfound(nameentry.get(), searchbox.get()))

    searchbutton = CTkButton(rightframe, text='Search', fg_color='DarkSlateGray', text_color='white', font=('Open Sans', 15, 'bold'), border_color='white', border_width=2, command=search)
    searchbutton.grid(row=0, column=2, padx=10, pady=10, sticky='e')

    showallbutton = CTkButton(rightframe, text='Show All', fg_color='DarkSlateGray', text_color='white', font=('Open Sans', 15, 'bold'), border_color='white', border_width=2, command=showall)
    showallbutton.grid(row=0, column=3, padx=10, pady=10, sticky='e')

    # Additional Treeview in rightframe
    tree2 = ttk.Treeview(rightframe, height=10)
    tree2.grid(row=1, column=0, columnspan=4, sticky='nsew')

    tree2['columns'] = ('Student Id', 'Student Name', 'Email ID', 'CGPA')
    tree2.heading('Student Id', text='Student ID')
    tree2.heading('Student Name', text='Student Name')
    tree2.heading('Email ID', text='Email ID')
    tree2.heading('CGPA', text='CGPA')

    tree2.config(show='headings')
    tree2.column('Student Id', anchor=tk.CENTER, width=70)
    tree2.column('Student Name', anchor=tk.CENTER, width=120)
    tree2.column('Email ID', anchor=tk.CENTER, width=140)
    tree2.column('CGPA', anchor=tk.CENTER, width=90)

    style.configure('Treeview.Heading', font=('Microsoft Yahei UI Light', 10, 'bold'), background='white', foreground='DarkSlateGray')
    style.configure('Treeview', font=('Microsoft Yahei UI Light', 10), rowheight=30, background='white', foreground='DarkSlateGray')

    scrollbar2 = ttk.Scrollbar(rightframe, orient=tk.VERTICAL, command=tree2.yview)
    scrollbar2.grid(row=1, column=4, sticky='ns')

    tree2.config(yscrollcommand=scrollbar2.set)

    shome.mainloop()


# homef('F001')
