from tkinter import *
import time
import ttkthemes
from tkinter import ttk,messagebox, filedialog
import pymysql
import pandas

#phan ham

def iexit():
    result=messagebox.askyesno('Xác nhận','Bạn có muốn thoát không')
    if result:
        root.destroy()
    else:
        pass

def export_data():
    if not studentTable.get_children():  # Kiểm tra có dữ liệu không
        messagebox.showwarning("Cảnh báo", "Không có dữ liệu để xuất!")
        return

    url = filedialog.asksaveasfilename(
        defaultextension='.csv',
        filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
        title="Lưu file CSV"
    )
    if not url:
        return  # Người dùng hủy

    # Lấy dữ liệu từ bảng
    indexing = studentTable.get_children()
    newlist = []
    for index in indexing:
        content = studentTable.item(index)
        datalist = content['values']
        newlist.append(datalist)

    # Định nghĩa đúng 9 cột theo thứ tự từ database
    columns = [
        'ID',           # 1 - id
        'Tên',          # 2 - name
        'Giới tính',    # 3 - gioitinh
        'Số điện thoại',# 4 - sdt
        'Email',        # 5 - email
        'Địa chỉ',      # 6 - diachi
        'Ngày sinh',    # 7 - ngaysinh
        'Giờ nhập',

    ]

    # Tạo DataFrame và xuất file
    table = pandas.DataFrame(newlist, columns=columns)
    table.to_csv(url, index=False, encoding='utf-8-sig')  # utf-8-sig để hiển thị tiếng Việt đúng
    messagebox.showinfo('Thành công', f'Dữ liệu đã được lưu vào:\n{url}')

def topLevel_data(title,button_text,command):
    global idEntry,phoneEntry,nameEntry,emailEntry,ngaysinhEntry,diachiEntry,gioitinhEntry,screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(width=0, height=0)

    idLabel = Label(screen, text='ID', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(screen, text='Tên', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    ngaysinhLabel = Label(screen, text='Ngày sinh', font=('times new roman', 20, 'bold'))
    ngaysinhLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    ngaysinhEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    ngaysinhEntry.grid(row=2, column=1, pady=15, padx=10)

    phoneLabel = Label(screen, text='Số điện thoại', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=3, column=1, pady=15, padx=10)

    emailLabel = Label(screen, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=4, column=1, pady=15, padx=10)

    diachiLabel = Label(screen, text='Địa chỉ', font=('times new roman', 20, 'bold'))
    diachiLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    diachiEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    diachiEntry.grid(row=5, column=1, pady=15, padx=10)

    gioitinhLabel = Label(screen, text='giới tính', font=('times new roman', 20, 'bold'))
    gioitinhLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    gioitinhEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    gioitinhEntry.grid(row=6, column=1, pady=15, padx=1)

    update_student_button = ttk.Button(screen, text=button_text, command=command)
    update_student_button.grid(row=7, columnspan=2, pady=15)

    if title == 'Cập nhật sinh viên':
        indexing = studentTable.focus()
        if not indexing:  # Kiểm tra có chọn dòng nào không
            messagebox.showerror("Lỗi", "Vui lòng chọn một sinh viên trong bảng để cập nhật!")
            screen.destroy()
            return

        content = studentTable.item(indexing)
        listdata = content['values']  # ← Lấy toàn bộ tuple, KHÔNG lấy [0]

        idEntry.insert(0, listdata[0])          # ID
        nameEntry.insert(0, listdata[1])        # Tên
        gioitinhEntry.insert(0, listdata[2])    # Giới tính
        phoneEntry.insert(0, listdata[3])       # SĐT
        emailEntry.insert(0, listdata[4])       # Email
        diachiEntry.insert(0, listdata[5])      # Địa chỉ
        ngaysinhEntry.insert(0, listdata[6])    # Ngày sinh


def update_data():
    query = '''UPDATE student 
               SET name=%s, sdt=%s, email=%s, gioitinh=%s, diachi=%s, ngaysinh=%s, date=%s, time=%s 
               WHERE id=%s'''

    mycursor.execute(query, (
        nameEntry.get(),
        phoneEntry.get(),
        emailEntry.get(),
        gioitinhEntry.get(),
        diachiEntry.get(),
        ngaysinhEntry.get(),
        date,
        currenttime,
        idEntry.get()
    ))
    con.commit()
    messagebox.showinfo('Success', f'Id {idEntry.get()} đã được cập nhật thành công!', parent=screen)
    screen.destroy()
    show_student()


def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def delete_student():
    indexing=studentTable.focus()
    print(indexing)
    content=studentTable.item(indexing)
    content_id=content['values'][0]
    query='delete from student where id=%s'
    mycursor.execute(query,(content_id,))
    con.commit()
    messagebox.showinfo('Đã xóa', f'Id {content_id} đã được xóa')
    query='select * from student '
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('',END,values=data)



def search_data():
    # Lấy giá trị từ các ô nhập (có thể để trống)
    id_search = idEntry.get().strip()
    name_search = nameEntry.get().strip()
    email_search = emailEntry.get().strip()
    phone_search = phoneEntry.get().strip()
    ngaysinh_search = ngaysinhEntry.get().strip()
    gioitinh_search = gioitinhEntry.get().strip()
    diachi_search = diachiEntry.get().strip()

    # Tạo điều kiện WHERE động chỉ với các trường có giá trị
    conditions = []
    params = []

    if id_search:
        conditions.append("id = %s")
        params.append(id_search)
    if name_search:
        conditions.append("name LIKE %s")
        params.append(f"%{name_search}%")
    if email_search:
        conditions.append("email LIKE %s")
        params.append(f"%{email_search}%")
    if phone_search:
        conditions.append("sdt LIKE %s")
        params.append(f"%{phone_search}%")
    if ngaysinh_search:
        conditions.append("ngaysinh LIKE %s")
        params.append(f"%{ngaysinh_search}%")
    if gioitinh_search:
        conditions.append("gioitinh LIKE %s")
        params.append(f"%{gioitinh_search}%")
    if diachi_search:
        conditions.append("diachi LIKE %s")
        params.append(f"%{diachi_search}%")

    # Nếu không nhập gì → báo lỗi hoặc hiển thị toàn bộ
    if not conditions:
        messagebox.showinfo("Thông báo", "Vui lòng nhập ít nhất một thông tin để tìm kiếm!")
        show_student()  # Hiển thị lại toàn bộ danh sách
        return

    # Tạo query
    query = "SELECT * FROM student WHERE " + " OR ".join(conditions)

    try:
        mycursor.execute(query, params)
        fetched_data = mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        if fetched_data:
            for data in fetched_data:
                studentTable.insert('', END, values=data)
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy sinh viên nào phù hợp!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {e}")


def add_data():
    global mycursor,con
    if (idEntry.get()=="" or nameEntry.get()=="" or ngaysinhEntry.get() == "" or phoneEntry.get() == "" or
            emailEntry.get() == "" or diachiEntry.get() == "" or gioitinhEntry.get() == ""):
        messagebox.showerror('Error', 'Hãy điền tất cả các trường!', parent=screen)

    else:
        try:
            query='insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(idEntry.get(),nameEntry.get(),ngaysinhEntry.get(),phoneEntry.get(),emailEntry.get()
                                                ,diachiEntry.get(),gioitinhEntry.get(),date,currenttime))
            con.commit()
            result=messagebox.askyesno('Xác nhận','Thêm thành công. Bạn có muốn thêm tiếp không? ',parent=screen)
            if result:
                idEntry.delete(0,'end')
                nameEntry.delete(0, 'end')
                phoneEntry.delete(0, 'end')
                ngaysinhEntry.delete(0, 'end')
                gioitinhEntry.delete(0, 'end')
                diachiEntry.delete(0, 'end')
                emailEntry.delete(0, 'end')
            else:
                pass
        except:
                messagebox.showerror('Error','Id đã tồn tại', parent=screen)
                return

        query='select *from student'
        mycursor.execute(query)
        fetched_data=mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for data in fetched_data:
            studentTable.insert('', END, values=data)


def connect_database():
    global mycursor, con

    # TẠO CỬA SỔ TRƯỚC
    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Kết nối Database')
    connectWindow.resizable(False, False)

    Label(connectWindow, text='Hostname', font=('arial', 18, 'bold')).grid(row=0, column=0, padx=30, pady=15)
    hostEntry = Entry(connectWindow, font=('roman', 18, 'bold'), bd=2)
    hostEntry.grid(row=0, column=1, padx=40, pady=15)
    hostEntry.insert(0, 'localhost')

    Label(connectWindow, text='Username', font=('arial', 18, 'bold')).grid(row=1, column=0, padx=30, pady=15)
    userEntry = Entry(connectWindow, font=('roman', 18, 'bold'), bd=2)
    userEntry.grid(row=1, column=1, padx=40, pady=15)
    userEntry.insert(0, 'root')

    Label(connectWindow, text='Password', font=('arial', 18, 'bold')).grid(row=2, column=0, padx=30, pady=15)
    passEntry = Entry(connectWindow, font=('roman', 18, 'bold'), bd=2, show='*')
    passEntry.grid(row=2, column=1, padx=40, pady=15)
    passEntry.insert(0, '123456')  # Thay bằng pass của bạn nếu khác

    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(
                host=hostEntry.get(),
                user=userEntry.get(),
                password=passEntry.get()
            )
            mycursor = con.cursor()

            # Tạo DB và bảng với đầy đủ cột date, time
            mycursor.execute("CREATE DATABASE IF NOT EXISTS quanlihocsinh")
            mycursor.execute("USE quanlihocsinh")
            mycursor.execute('''
                CREATE TABLE IF NOT EXISTS student (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50),
                    gioitinh VARCHAR(20),
                    sdt VARCHAR(15),
                    email VARCHAR(50),
                    diachi VARCHAR(100),
                    ngaysinh VARCHAR(50),
                    date VARCHAR(50),
                    time VARCHAR(50)
                )
            ''')
            con.commit()
            messagebox.showinfo('Thành công', 'Kết nối database thành công!')

            connectWindow.destroy()

            # Bật nút sau kết nối
            addstudentButton.config(state=NORMAL)
            searchstudentButton.config(state=NORMAL)
            updatestudentButton.config(state=NORMAL)
            deletestudentButton.config(state=NORMAL)
            showstudentButton.config(state=NORMAL)
            exportstudentButton.config(state=NORMAL)

        except Exception as e:
            messagebox.showerror('Lỗi kết nối', f'Không thể kết nối!\n{e}')

    # Nút Connect
    Button(connectWindow, text='Connect', font=('arial', 14, 'bold'), bg='blue', fg='white', command=connect).grid(row=3, columnspan=2, pady=20)

def clock():
    global date,currenttime
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000, clock)

count=0
text=''
def slider():
    global text,count
    if count==len(s):
        count=0
        text=''
    text=text+s[count]
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(300,slider)

#Gui
root =ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1174x680+50+20')
root.resizable(width=0, height=0)
root.title('Student Management System')

datetimeLabel=Label(root,text='Date',font=('times new roman',18,'bold'))
datetimeLabel.place(x=5,y=5)
clock()

s='Student Management System'
sliderLabel=Label(root,text=s,font=('times new roman',20,'bold'),width=30)
sliderLabel.place(x=200,y=0)
slider()

connectButton=ttk.Button(root,text='Connect database',command=connect_database)
connectButton.place(x=980,y=0)

leftFrame=Frame(root)
leftFrame.place(x=50,y=80,width=300,height=600)

logo_image=PhotoImage(file='students.png')
logo_Label=Label(leftFrame,image=logo_image)
logo_Label.grid(row=0,column=0,padx=0,pady=0)

addstudentButton=ttk.Button(leftFrame,text='Thêm học sinh',width=25,command=lambda :topLevel_data('Thêm sinh viên','Thêm sinh viên',add_data))
addstudentButton.grid(row=1,column=0,pady=20)

searchstudentButton=ttk.Button(leftFrame,text='Tìm kiếm',width=25,command=lambda :topLevel_data('Tìm sinh viên','Tìm',search_data))
searchstudentButton.grid(row=2,column=0,pady=20)

deletestudentButton=ttk.Button(leftFrame,text='Xóa',width=25,command=delete_student)
deletestudentButton.grid(row=3,column=0,pady=20)

updatestudentButton=ttk.Button(leftFrame,text='Cập nhật',width=25,command=lambda :topLevel_data('Cập nhật sinh viên','Cập nhật',update_data))
updatestudentButton.grid(row=4,column=0,pady=20)

showstudentButton=ttk.Button(leftFrame,text='Xem danh sách học sinh',width=25,command=show_student)
showstudentButton.grid(row=5,column=0,pady=20)

exportstudentButton=ttk.Button(leftFrame,text='Xuất dữ liệu',width=25,command=export_data)
exportstudentButton.grid(row=6,column=0,pady=20)

exitButton=ttk.Button(leftFrame,text='Thoát',width=25,command=iexit)
exitButton.grid(row=7,column=0,pady=20)

rightFrame=Frame(root)
rightFrame.place(x=350,y=80,width=800,height=600)

scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)


studentTable=ttk.Treeview(rightFrame,columns=('Id','Name','Gioi tinh','Sdt','Email','Dia chi','Ngay sinh','Added Time','Added Date'),
                          xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

studentTable.pack(fill=BOTH,expand=1)

studentTable.heading('Id',text='ID')
studentTable.heading('Name',text='Tên')
studentTable.heading('Ngay sinh',text='Ngày sinh')
studentTable.heading('Gioi tinh',text='Giới tính')
studentTable.heading('Sdt',text='Số điện thoại')
studentTable.heading('Email',text='Email')
studentTable.heading('Dia chi',text='Địa chỉ')
studentTable.heading('Added Date',text='Ngày nhập')
studentTable.heading('Added Time',text='Giờ nhập')

studentTable.column('Id',width=50,anchor=CENTER)
studentTable.column('Name',width=300,anchor=CENTER)
studentTable.column('Gioi tinh',width=100,anchor=CENTER)
studentTable.column('Sdt',width=200,anchor=CENTER)
studentTable.column('Email',width=300,anchor=CENTER)
studentTable.column('Dia chi',width=400,anchor=CENTER)
studentTable.column('Added Date',width=100,anchor=CENTER)
studentTable.column('Added Time',width=100,anchor=CENTER)

style=ttk.Style()

style.configure('Treeview',rowheight=30,font=('arial',12,'bold'),foreground='red4',background='white',fieldbackground='white')
style.configure('Treeview.Heading',font=('arial',14,'bold'),foreground='red4',background='white')


studentTable.config(show='headings')

root.mainloop()