from tkinter import *
import time
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import sqlite3
import pandas
import os

# Lấy vai trò từ login.py
current_role = os.getenv('USER_ROLE', 'User')

# Kết nối SQLite
def get_connection():
    conn = sqlite3.connect('student.db')
    return conn

# Tạo bảng nếu chưa tồn tại
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gioitinh TEXT,
            sdt TEXT,
            email TEXT,
            diachi TEXT,
            ngaysinh TEXT,
            date TEXT,
            time TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_table()



def iexit():
    result = messagebox.askyesno('Xác nhận', 'Bạn có muốn thoát không?')
    if result:
        root.destroy()

def export_data():
    if not studentTable.get_children():
        messagebox.showwarning("Cảnh báo", "Không có dữ liệu để xuất!")
        return

    url = filedialog.asksaveasfilename(
        defaultextension='.csv',
        filetypes=[('CSV files', '*.csv'), ('Excel files', '*.xlsx'), ('All files', '*.*')],
        title="Lưu dữ liệu sinh viên"
    )
    if not url:
        return

    data = []
    for child in studentTable.get_children():
        values = studentTable.item(child)['values']
        data.append(values)

    columns = ['ID', 'Tên', 'Giới tính', 'Số điện thoại', 'Email', 'Địa chỉ', 'Ngày sinh', 'Ngày nhập', 'Giờ nhập']

    df = pandas.DataFrame(data, columns=columns)
    if url.endswith('.xlsx'):
        df.to_excel(url, index=False)
        messagebox.showinfo('Thành công', f'Dữ liệu đã lưu thành file Excel:\n{url}')
    else:
        df.to_csv(url, index=False, encoding='utf-8-sig')
        messagebox.showinfo('Thành công', f'Dữ liệu đã lưu thành file CSV:\n{url}')

def topLevel_data(title, button_text, command):
    global idEntry, phoneEntry, nameEntry, emailEntry, ngaysinhEntry, diachiEntry, gioitinhEntry, screen
    screen = Toplevel(root)
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)

    row = 0
    if title == 'Cập nhật sinh viên' or title == 'Thêm sinh viên':
        if title == 'Cập nhật sinh viên':
            Label(screen, text='ID', font=('times new roman', 20, 'bold')).grid(row=row, column=0, padx=30, pady=15, sticky=W)
            idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24, state='readonly', bg='#f0f0f0')
            idEntry.grid(row=row, column=1, pady=15, padx=10)
            row += 1
        else:
            idEntry = None

        Label(screen, text='Tên', font=('times new roman', 20, 'bold')).grid(row=row, column=0, padx=30, pady=15, sticky=W)
        nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
        nameEntry.grid(row=row, column=1, pady=15, padx=10)
        row += 1

        Label(screen, text='Giới tính', font=('times new roman', 20, 'bold')).grid(row=row, column=0, padx=30, pady=15, sticky=W)
        gioitinhEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
        gioitinhEntry.grid(row=row, column=1, pady=15, padx=10)
        row += 1

        Label(screen, text='Số điện thoại', font=('times new roman', 20, 'bold')).grid(row=row, column=0, padx=30, pady=15, sticky=W)
        phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
        phoneEntry.grid(row=row, column=1, pady=15, padx=10)
        row += 1

        Label(screen, text='Email', font=('times new roman', 20, 'bold')).grid(row=row, column=0, padx=30, pady=15, sticky=W)
        emailEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
        emailEntry.grid(row=row, column=1, pady=15, padx=10)
        row += 1

        Label(screen, text='Địa chỉ', font=('times new roman', 20, 'bold')).grid(row=row, column=0, padx=30, pady=15, sticky=W)
        diachiEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
        diachiEntry.grid(row=row, column=1, pady=15, padx=10)
        row += 1

        Label(screen, text='Ngày sinh', font=('times new roman', 20, 'bold')).grid(row=row, column=0, padx=30, pady=15, sticky=W)
        ngaysinhEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
        ngaysinhEntry.grid(row=row, column=1, pady=15, padx=10)
        row += 1

        ttk.Button(screen, text=button_text, command=command).grid(row=row, columnspan=2, pady=20)


    if title == 'Cập nhật sinh viên':
        selected = studentTable.focus()
        if not selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn một sinh viên để cập nhật!")
            screen.destroy()
            return
        values = studentTable.item(selected)['values']
        idEntry.config(state='normal')
        idEntry.insert(0, values[0])
        idEntry.config(state='readonly')
        nameEntry.insert(0, values[1])
        gioitinhEntry.insert(0, values[2])
        phoneEntry.insert(0, values[3])
        emailEntry.insert(0, values[4])
        diachiEntry.insert(0, values[5])
        ngaysinhEntry.insert(0, values[6])

def add_data():
    if not all([nameEntry.get().strip(), gioitinhEntry.get().strip(), phoneEntry.get().strip(),
                emailEntry.get().strip(), diachiEntry.get().strip(), ngaysinhEntry.get().strip()]):
        messagebox.showerror('Error', 'Hãy điền đầy đủ thông tin!')
        return

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO student (name, gioitinh, sdt, email, diachi, ngaysinh, date, time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nameEntry.get(), gioitinhEntry.get(), phoneEntry.get(), emailEntry.get(),
              diachiEntry.get(), ngaysinhEntry.get(), date, currenttime))
        conn.commit()
        messagebox.showinfo("Thành công", "Thêm sinh viên thành công!")
        clear_entries()
        show_student()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể thêm: {e}")
    finally:
        conn.close()

def clear_entries():
    for entry in [nameEntry, gioitinhEntry, phoneEntry, emailEntry, diachiEntry, ngaysinhEntry]:
        entry.delete(0, END)

def update_data():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE student SET name=?, gioitinh=?, sdt=?, email=?, diachi=?, ngaysinh=?, date=?, time=?
            WHERE id=?
        ''', (nameEntry.get(), gioitinhEntry.get(), phoneEntry.get(), emailEntry.get(),
              diachiEntry.get(), ngaysinhEntry.get(), date, currenttime, idEntry.get()))
        conn.commit()
        messagebox.showinfo("Thành công", "Cập nhật thành công!")
        screen.destroy()
        show_student()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể cập nhật: {e}")
    finally:
        conn.close()

def delete_student():
    selected = studentTable.focus()
    if not selected:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên để xóa!")
        return
    values = studentTable.item(selected)['values']
    if messagebox.askyesno("Xác nhận", f"Xóa sinh viên ID {values[0]} - {values[1]}?"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student WHERE id=?", (values[0],))
        conn.commit()
        conn.close()
        show_student()

def show_student():
    for item in studentTable.get_children():
        studentTable.delete(item)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student")
    rows = cursor.fetchall()
    for row in rows:
        studentTable.insert('', END, values=row)
    conn.close()

def search_data():
    conditions = []
    params = []

    fields = {
        "id": idEntry.get().strip(),
        "name": nameEntry.get().strip(),
        "email": emailEntry.get().strip(),
        "sdt": phoneEntry.get().strip(),
        "ngaysinh": ngaysinhEntry.get().strip(),
        "gioitinh": gioitinhEntry.get().strip(),
        "diachi": diachiEntry.get().strip()
    }

    for field, value in fields.items():
        if value:
            conditions.append(f"{field} LIKE ?")
            params.append(f"%{value}%")

    if not conditions:
        show_student()
        return

    query = "SELECT * FROM student WHERE " + " OR ".join(conditions)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for row in rows:
        studentTable.insert('', END, values=row)
    conn.close()

# GIAO DIỆN
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1174x680+50+20')
root.resizable(False, False)
root.title('Student Management System')


def clock():
    global date, currenttime
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000, clock)

datetimeLabel = Label(root, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=5, y=5)
clock()

s = 'Student Management System'
sliderLabel = Label(root, text=s, font=('times new roman', 28, 'bold'), width=30)
sliderLabel.place(x=200, y=0)


leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)

logo_image = PhotoImage(file='students.png')
Label(leftFrame, image=logo_image).grid(row=0, column=0, pady=10)

# Các nút
addstudentButton = ttk.Button(leftFrame, text='Thêm học sinh', width=25,
                             command=lambda: topLevel_data('Thêm sinh viên', 'Thêm', add_data))
addstudentButton.grid(row=1, column=0, pady=15)

searchstudentButton = ttk.Button(leftFrame, text='Tìm kiếm', width=25,
                                command=lambda: topLevel_data('Tìm sinh viên', 'Tìm', search_data))
searchstudentButton.grid(row=2, column=0, pady=15)

deletestudentButton = ttk.Button(leftFrame, text='Xóa', width=25, command=delete_student)
deletestudentButton.grid(row=3, column=0, pady=15)

updatestudentButton = ttk.Button(leftFrame, text='Cập nhật', width=25,
                                command=lambda: topLevel_data('Cập nhật sinh viên', 'Cập nhật', update_data))
updatestudentButton.grid(row=4, column=0, pady=15)

showstudentButton = ttk.Button(leftFrame, text='Xem danh sách', width=25, command=show_student)
showstudentButton.grid(row=5, column=0, pady=15)

exportstudentButton = ttk.Button(leftFrame, text='Xuất dữ liệu', width=25, command=export_data)
exportstudentButton.grid(row=6, column=0, pady=15)

exitButton = ttk.Button(leftFrame, text='Thoát', width=25, command=iexit)
exitButton.grid(row=7, column=0, pady=15)

# Bảng dữ liệu
rightFrame = Frame(root)
rightFrame.place(x=350, y=80, width=800, height=600)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame, columns=('Id','Name','Gioi tinh','Sdt','Email','Dia chi','Ngay sinh','Time','Date'),
                           xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)
studentTable.pack(fill=BOTH, expand=1)

# Heading
studentTable.heading('Id', text='ID')
studentTable.heading('Name', text='Tên')
studentTable.heading('Gioi tinh', text='Giới tính')
studentTable.heading('Sdt', text='Số điện thoại')
studentTable.heading('Email', text='Email')
studentTable.heading('Dia chi', text='Địa chỉ')
studentTable.heading('Ngay sinh', text='Ngày sinh')
studentTable.heading('Date', text='Ngày nhập')
studentTable.heading('Time', text='Giờ nhập')

# Style
style = ttk.Style()
style.configure('Treeview', rowheight=35, font=('arial', 11))
style.configure('Treeview.Heading', font=('arial', 12, 'bold'))

studentTable.config(show='headings')

# Áp dụng phân quyền ngay khi khởi động
if current_role == 'User':
    addstudentButton.config(state=DISABLED)
    updatestudentButton.config(state=DISABLED)
    deletestudentButton.config(state=DISABLED)
    messagebox.showinfo("Thông báo", "Bạn đang đăng nhập với quyền USER.\nChỉ được xem, tìm kiếm và xuất dữ liệu.")

# Hiển thị dữ liệu lần đầu
show_student()

root.mainloop()