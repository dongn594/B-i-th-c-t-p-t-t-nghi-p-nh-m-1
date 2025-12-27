from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import os
import subprocess

# Danh sách tài khoản cố định
valid_accounts = {
    "admin": {"password": "admin123", "role": "Admin"},
    "user":  {"password": "user123",  "role": "User"}
}

def login():
    username = usernameEntry.get().strip().lower()
    password = passwordEntry.get().strip()
    selected_role = role_var.get()

    if not username or not password:
        messagebox.showerror('Lỗi', 'Vui lòng nhập đầy đủ username và password!')
        return

    if username in valid_accounts:
        account = valid_accounts[username]
        if password == account["password"]:
            if selected_role == account["role"]:
                messagebox.showinfo('Thành công', f'Đăng nhập thành công với quyền {selected_role}!')
                window.destroy()
                os.environ['USER_ROLE'] = selected_role
                subprocess.Popen(['python', 'sms.py'])
                return
            else:
                messagebox.showerror('Lỗi quyền hạn',
                                     f'Tài khoản "{username}" chỉ được phép đăng nhập với quyền {account["role"]}!')
        else:
            messagebox.showerror('Lỗi', 'Mật khẩu không đúng!')
    else:
        messagebox.showerror('Lỗi', 'Username không tồn tại!')

# ==================== GIAO DIỆN LOGIN ====================
window = Tk()
window.geometry('1280x700+0+0')
window.title('Login System - Student Management System')
window.resizable(False, False)

# Biến chọn quyền (mặc định Admin)
role_var = StringVar(window, value="Admin")

# Nền
try:
    backgroundImage = ImageTk.PhotoImage(file='bg.jpg')
    bgLabel = Label(window, image=backgroundImage)
    bgLabel.place(x=0, y=0, relwidth=1, relheight=1)
except:
    window.configure(bg='#f0f0f0')

# Frame chính giữa
loginFrame = Frame(window, bg='white', relief='groove', bd=8)
loginFrame.place(relx=0.5, rely=0.5, anchor=CENTER, width=600, height=690)

# Logo / Icon sinh viên
try:
    logoImage = PhotoImage(file='logo.png')
    Label(loginFrame, image=logoImage, bg='white').grid(row=0, column=0, columnspan=2, pady=30)
except:
    Label(loginFrame, text="🎓", font=('Arial', 100), bg='white', fg='#0066CC').grid(row=0, column=0, columnspan=2, pady=30)

# Username
try:
    user_img = PhotoImage(file='user.png')
except:
    user_img = None
Label(loginFrame, image=user_img if 'user_img' in locals() else '', text=' Username', compound=LEFT,
      font=('times new roman', 22, 'bold'), bg='white', fg='black').grid(row=1, column=0, pady=20, padx=30, sticky=W)

usernameEntry = Entry(loginFrame, font=('times new roman', 20), bd=5, fg='royalblue', justify='center', width=20)
usernameEntry.grid(row=1, column=1, pady=20, padx=20)
usernameEntry.focus()

# Password
try:
    pass_img = PhotoImage(file='password.png')
except:
    pass_img = None
Label(loginFrame, image=pass_img if 'pass_img' in locals() else '', text=' Password', compound=LEFT,
      font=('times new roman', 22, 'bold'), bg='white', fg='black').grid(row=2, column=0, pady=20, padx=30, sticky=W)

passwordEntry = Entry(loginFrame, font=('times new roman', 20), bd=5, fg='royalblue', show='*', justify='center', width=20)
passwordEntry.grid(row=2, column=1, pady=20, padx=20)

# Chọn quyền truy cập
Label(loginFrame, text="Chọn quyền truy cập:", font=('times new roman', 20, 'bold'), bg='white', fg='#0066CC')\
    .grid(row=3, column=0, columnspan=2, pady=(30, 15))

radio_frame = Frame(loginFrame, bg='white')
radio_frame.grid(row=4, column=0, columnspan=2, pady=10)

Radiobutton(radio_frame, text="  Admin  ", variable=role_var, value="Admin",
            font=('times new roman', 20, 'bold'), bg='white', fg='black',
            selectcolor='#a0d8ff', indicatoron=0, width=10, height=2, relief='raised', bd=5)\
    .grid(row=0, column=0, padx=50)

Radiobutton(radio_frame, text="  User  ", variable=role_var, value="User",
            font=('times new roman', 20, 'bold'), bg='white', fg='black',
            selectcolor='#b5e6b5', indicatoron=0, width=10, height=2, relief='raised', bd=5)\
    .grid(row=0, column=1, padx=50)

# NÚT ĐĂNG NHẬP
loginButton = Button(loginFrame, text='ĐĂNG NHẬP', font=('times new roman', 24, 'bold'), width=12, height=1,
                     fg='white', bg='#0066CC', activebackground='#0055AA',
                     activeforeground='white', cursor='hand2', relief='raised', bd=10, command=login)
loginButton.grid(row=5, column=0, columnspan=2, pady=40)

# Gợi ý tài khoản
Label(loginFrame, text="Gợi ý tài khoản:\nAdmin: admin / admin123\nUser: user / user123",
      font=('arial', 11), fg='gray', bg='white', justify=CENTER)\
    .grid(row=6, column=0, columnspan=2, pady=15)

# Nhấn Enter để đăng nhập
window.bind('<Return>', lambda event: login())

# Giữ tham chiếu ảnh để không bị garbage collected
window.backgroundImage = backgroundImage if 'backgroundImage' in locals() else None
window.logoImage = logoImage if 'logoImage' in locals() else None
window.user_img = user_img if 'user_img' in locals() else None
window.pass_img = pass_img if 'pass_img' in locals() else None

window.mainloop()