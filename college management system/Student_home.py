from customtkinter import *
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk  # Ensure this import is included
import Student_db  # Make sure this import is correct
import student_faculty

def homes(id):
    global user_id
    user_id = id
    print(user_id)
    shome = ctk.CTk()
    shome.title('Home Page')
    shome.config(bg='white')
    shome.geometry('900x580+100+100')
    shome.resizable(False, False)

    # Configure grid to allocate 20% height to homeframe and 80% to the rest
    shome.grid_rowconfigure(0, weight=3)  # 20% of the height
    shome.grid_rowconfigure(1, weight=8)  # 80% of the height
    shome.grid_columnconfigure(0, weight=1)

    # Define common styling for the widgets
    label_font = ('arial', 18, 'bold')
    entry_font = ('OpenSans', 13)
    label_color = 'black'
    entry_color = 'white'

    # Create home frame (20% of height)
    homeframe = CTkFrame(shome, fg_color='DarkSlateGray')
    homeframe.grid(row=0, column=0, sticky='nsew')

    # Configure grid of homeframe to center leftframe and rightframe with a gap between them
    homeframe.grid_rowconfigure(0, weight=1)
    homeframe.grid_rowconfigure(2, weight=1)
    homeframe.grid_columnconfigure(0, weight=1)
    homeframe.grid_columnconfigure(1, weight=1)  # Add a column for spacing
    homeframe.grid_columnconfigure(2, weight=1)
    homeframe.grid_columnconfigure(3, weight=1)

    # Create left frame
    leftframe = CTkFrame(homeframe, fg_color='DarkSlateGray')
    leftframe.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')

    idlabel = CTkLabel(leftframe, text='Reg Id', font=label_font, text_color='white', bg_color='DarkSlateGray')
    idlabel.grid(row=0, column=0, padx=(5, 20), pady=5, sticky='w')
    identry = CTkEntry(leftframe, font=entry_font, width=180, fg_color=entry_color, text_color='black')
    identry.grid(row=0, column=1, padx=(0, 10), pady=0)
    identry.insert(0, user_id)
    identry.configure(state='readonly')

    namelabel = CTkLabel(leftframe, text='Name', font=label_font, text_color='white', bg_color='DarkSlateGray')
    namelabel.grid(row=1, column=0, padx=(5, 20), pady=5, sticky='w')
    nameentry = CTkEntry(leftframe, font=entry_font, width=180, fg_color=entry_color, text_color='black')
    nameentry.grid(row=1, column=1, pady=(0, 0), padx=(0, 10))
    nameentry.insert(0, Student_db.student_name(user_id))
    nameentry.configure(state='readonly')

    # Create right frame
    rightframe = CTkFrame(homeframe, fg_color='DarkSlateGray')
    rightframe.grid(row=1, column=3, padx=10, pady=5, sticky='nsew')

    emaillabel = CTkLabel(rightframe, text='Email ID', font=label_font, text_color='white', bg_color='DarkSlateGray')
    emaillabel.grid(row=0, column=0, padx=(5, 20), pady=5, sticky='w')
    emailentry = CTkEntry(rightframe, font=entry_font, width=180, fg_color=entry_color, text_color='black')
    emailentry.grid(row=0, column=1, padx=(0, 10), pady=0)
    emailentry.insert(0, Student_db.student_email(user_id))
    emailentry.configure(state='readonly')

    cgplabel = CTkLabel(rightframe, text='CGP', font=label_font, text_color='white', bg_color='DarkSlateGray')
    cgplabel.grid(row=1, column=0, padx=(5, 20), pady=5, sticky='w')
    cgpentry = CTkEntry(rightframe, font=entry_font, width=180, fg_color=entry_color, text_color='black')
    cgpentry.grid(row=1, column=1, pady=(0, 0), padx=(0, 10))

    # Check and debug CGPA value
    cgpa_value = student_faculty.student_cgpa(user_id)
    print("CGPA Value:", cgpa_value)  # Debugging line to check the value

    if cgpa_value is None:
        cgpa_value = "N/A"  # Handle None case

    cgpentry.insert(0, cgpa_value)
    cgpentry.configure(state='readonly')

    # Fetch subjects data and integrate Treeview
    faculty_data = student_faculty.student_tree(id)
    print(faculty_data)

    # Check if faculty_data is None
    if faculty_data is None:
        print("Error: No data returned from student_tree function.")
    else:
        # Placeholder for tree view or additional content (80% of height)
        contentframe = CTkFrame(shome, fg_color='white')
        contentframe.grid(row=1, column=0, sticky='nsew', pady=(30, 10))

        # Configure grid columns of contentframe to ensure tree view spans full width
        contentframe.grid_rowconfigure(0, weight=1)
        contentframe.grid_columnconfigure(0, weight=1)
        contentframe.grid_columnconfigure(1, weight=0)  # Scrollbar column

        style = ttk.Style()
        style.configure('Treeview', font=('OpenSans', 12), rowheight=30)
        style.configure('Treeview.Heading', font=('OpenSans', 14))

        # Create a Treeview widget
        tree = ttk.Treeview(contentframe, columns=('Serial Number', 'Subject Code', 'Subject Name', 'Faculty ID', 'Faculty Name', 'Class Room'), show='headings', style='Treeview')
        tree.heading('Serial Number', text='Serial Number')
        tree.heading('Subject Code', text='Subject Code')
        tree.heading('Subject Name', text='Subject Name')
        tree.heading('Faculty ID', text='Faculty ID')
        tree.heading('Faculty Name', text='Faculty Name')
        tree.heading('Class Room', text='Class Room')

        tree.column('Serial Number', anchor=tk.CENTER, width=100)
        tree.column('Subject Code', anchor=tk.CENTER, width=100)
        tree.column('Subject Name', anchor=tk.CENTER, width=150)
        tree.column('Faculty ID', anchor=tk.CENTER, width=100)
        tree.column('Faculty Name', anchor=tk.CENTER, width=150)
        tree.column('Class Room', anchor=tk.CENTER, width=100)

        tree.grid(row=0, column=0, sticky='nsew')

        # Create a vertical scrollbar
        scrollbar = ttk.Scrollbar(contentframe, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Link the scrollbar with the Treeview
        tree.config(yscrollcommand=scrollbar.set)

        # Insert data into the Treeview
        for idx, row in enumerate(faculty_data, start=1):
            tree.insert('', 'end', values=(idx, *row))

    shome.mainloop()

# homes('S001')
