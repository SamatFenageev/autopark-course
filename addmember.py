from tkinter import *
from tkinter import messagebox

import sqlite3

con = sqlite3.connect('autopark.db')
cur = con.cursor()

class AddMember(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Добавить Сотрудника")
        self.resizable(False, False)


        ################### Рамки #########################

        #верхняя рамка
        self.topFrame = Frame(self, height = 150, bg = 'white')
        self.topFrame.pack(fill=X)

        #нижняя рамка
        self.bottomFrame = Frame(self, height = 600, bg = '#fcc324')
        self.bottomFrame.pack(fill=X)

        #заголовок, изображение
        self.top_image = PhotoImage(file = 'icons/add_member.png')
        top_image_lbl = Label(self.topFrame, image = self.top_image, bg = 'white')
        top_image_lbl.place(x = 120, y = 10)
        heading = Label(self.topFrame, text = '  Добавить сотрудника', font = 'arial 22 bold', fg = '#003f88', bg = 'white')
        heading.place(x = 290, y = 60)


        ######################### вводы и лейблы #########################
        #ФИО
        self.lbl_name = Label(self.bottomFrame, text = "ФИО", font = 'arial 15 bold', fg = 'white', bg = '#fcc324')
        self.lbl_name.place(x=40, y=40)
        self.ent_name = Entry(self.bottomFrame, width = 30, bd = 4)
        self.ent_name.insert(0, 'Введите сотрудника')
        self.ent_name.place(x=150, y=45)
        # пасспорт
        self.lbl_passport = Label(self.bottomFrame, text="Паспорт", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_passport.place(x=40, y=80)
        self.ent_passport = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_passport.insert(0, 'Введите серию и номер паспорта')
        self.ent_passport.place(x=150, y=85)
        # телефон
        self.lbl_phone = Label(self.bottomFrame, text="Телефон", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_phone.place(x=40, y=120)
        self.ent_phone = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_phone.insert(0, 'Введите телефон')
        self.ent_phone.place(x=150, y=125)
        # отдел
        self.lbl_department = Label(self.bottomFrame, text="Отдел", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_department.place(x=40, y=160)
        self.ent_department = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_department.insert(0, 'Введите отел')
        self.ent_department.place(x=150, y=165)

        # кнопка
        button = Button(self.bottomFrame, text = 'Добавить сотрудника', command = self.addMember)
        button.place(x = 200, y = 200)

    def addMember(self):
        member = self.ent_name.get()
        phone = self.ent_phone.get()
        department = self.ent_department.get()
        passport = self.ent_passport.get()

        if member and phone and department and passport:
            try:
                query = f"INSERT INTO users (username, passport, phone, department) VALUES('{member}', {passport}, '{phone}', '{department}')"

                cur.execute(query)
                con.commit()
                messagebox.showinfo('Успешно', 'Успешно добавлено в БД', icon='info')

            except Exception as e:
                print(e)
                messagebox.showerror("Ошибка", "Не получилось добавить в БД", icon='warning')
        else:
            messagebox.showerror("Ошибка", "Поле не может быть пустым", icon='warning')

