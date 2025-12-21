from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import subprocess  # Dùng để chạy sms.py một cách an toàn hơn
import os

# Biến toàn cục để lưu vai trò người dùng


def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'Please enter your username and password')
    elif usernameEntry.get() == 'Dong' and passwordEntry.get() == '1234':
        messagebox.showinfo('Success', f'Logged in successfully')
        window.destroy()  # Đóng cửa sổ login
        import sms        # Hoặc dùng subprocess như hướng dẫn trước
    else:
        messagebox.showerror('Error', 'Please enter correct username and password')


window = Tk()
window.geometry('1280x700+0+0')
window.title('Login System of Student Management System')
window.resizable(False, False)

backgroundImage = ImageTk.PhotoImage(file='bg.jpg')
bgLabel = Label(window, image=backgroundImage)
bgLabel.place(x=0, y=0)

loginFrame = Frame(window, bg='white')
loginFrame.place(x=400, y=150)

logoImage = PhotoImage(file='logo.png')
logoLabel = Label(loginFrame, image=logoImage, bg='white')
logoLabel.grid(row=0, column=0, columnspan=2, pady=10)

# Username
usernameImage = PhotoImage(file='user.png')
usernameLabel = Label(loginFrame, image=usernameImage, text='Username', compound=LEFT,
                      font=('times new roman', 20, 'bold'), bg='white')
usernameLabel.grid(row=1, column=0, pady=10, padx=20)

usernameEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'), bd=5, fg='royalblue')
usernameEntry.grid(row=1, column=1, pady=10, padx=20)

# Password
passwordImage = PhotoImage(file='password.png')
passwordLabel = Label(loginFrame, image=passwordImage, text='Password', compound=LEFT,
                      font=('times new roman', 20, 'bold'), bg='white')
passwordLabel.grid(row=2, column=0, pady=10, padx=20)

passwordEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'), bd=5, fg='royalblue', show='*')
passwordEntry.grid(row=2, column=1, pady=10, padx=20)

# Thêm phần chọn vai trò (Admin / User)
role_var = StringVar(value="User")  # Mặc định là User

roleFrame = Frame(loginFrame, bg='white')
roleFrame.grid(row=3, column=0, columnspan=2, pady=15)

Label(roleFrame, text="Select Role:", font=('times new roman', 16, 'bold'), bg='white').pack(side=LEFT, padx=10)

Radiobutton(roleFrame, text="Admin", variable=role_var, value="Admin", font=('times new roman', 14), bg='white').pack(
    side=LEFT, padx=10)
Radiobutton(roleFrame, text="User", variable=role_var, value="User", font=('times new roman', 14), bg='white').pack(
    side=LEFT, padx=10)

# Login button
loginButton = Button(loginFrame, text='Login', font=('times new roman', 14, 'bold'), width=15,
                     fg='white', bg='cornflowerblue', activebackground='cornflowerblue',
                     activeforeground='white', cursor='hand2', command=login)
loginButton.grid(row=4, column=1, pady=20)

window.mainloop()