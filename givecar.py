from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import datetime

con = sqlite3.connect("autopark.db")
cur = con.cursor()
class GiveCar(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+220")
        self.title("Выдать Автомобиль")
        self.resizable(False, False)

        query = "SELECT * FROM users"
        members = cur.execute(query).fetchall()
        member_list = []
        for member in members:
            member_list.append(str(member[0]) + " - " + member[1])
        query2 = "SELECT * FROM cars WHERE status = 0"
        cars = cur.execute(query2).fetchall()
        cars_list = []
        for car in cars:
            cars_list.append(str(car[0]) + " - " + car[1] + " - " + car[2])

        ################### Рамки #########################

        # верхняя рамка
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)

        # нижняя рамка
        self.bottomFrame = Frame(self, height=600, bg='#fcc324')
        self.bottomFrame.pack(fill=X)

        # заголовок, изображение
        self.top_image = PhotoImage(file='icons/add_book.png')
        top_image_lbl = Label(self.topFrame, image=self.top_image, bg='white')
        top_image_lbl.place(x=120, y=10)
        heading = Label(self.topFrame, text='Выдать Автомобиль', font='arial 22 bold', fg='#003f88', bg='white')
        heading.place(x=290, y=60)

        ######################### вводы и лейблы #########################
        # авто
        self.car_name = StringVar()
        self.lbl_name = Label(self.bottomFrame, text="Автомобиль: ", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_name.place(x=40, y=40)
        self.combo_name = ttk.Combobox(self.bottomFrame, textvariable = self.car_name)
        self.combo_name['values'] = cars_list
        self.combo_name.place(x = 180, y = 45)
        # сотрудник
        self.member_name = StringVar()
        self.lbl_phone = Label(self.bottomFrame, text="ID Сотрудника: ", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_phone.place(x=40, y=80)
        self.combo_member = ttk.Combobox(self.bottomFrame, textvariable=self.member_name)
        self.combo_member['values'] = member_list
        self.combo_member.place(x=210, y=85)
        # причина выдачи
        self.issue = IntVar()
        self.lbl_issue = Label(self.bottomFrame, text="Причина выдачи: ", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_issue.place(x=40, y=120)

        rb1 = Radiobutton(self.bottomFrame, text='Тех Обслуживание', var=self.issue, value=1, bg='#fcc324')
        rb2 = Radiobutton(self.bottomFrame, text='Ремонт', var=self.issue, value=2, bg='#fcc324')
        rb3 = Radiobutton(self.bottomFrame, text='Личное Пользование', var=self.issue, value=3, bg='#fcc324')
        rb1.place(x= 220, y=125)
        rb2.place(x=220, y=145)
        rb3.place(x=220, y=165)

        #self.ent_search = Entry(searchBar, width=30, bd=10)
        #self.ent_search.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

        # кнопка
        button = Button(self.bottomFrame, text='Выдать Автомобиль', command = self.giveCar)
        button.place(x=220, y=200)

    def giveCar(self):
        car_name = self.car_name.get()
        self.car_id = car_name.split('-')[0]
        self.member_id = self.member_name.get()[0]


        if self.car_id and self.member_id:
            try:
                value = self.issue.get()
                if value == 1:
                    issue = 'Тех Обслуживание'
                elif value == 2:
                    issue = 'Ремонт'
                else:
                    issue = 'Личное Пользование'
                #добавляем выдачу
                query = f"""INSERT INTO issuance (car_id, user_id, issue, issuance_date) VALUES({self.car_id},
                        {self.member_id}, '{issue}', '{str(datetime.date.today())}')"""
                cur.execute(query)
                query = f"""UPDATE cars SET status = 1, 
                 last_exam = '{datetime.date.today()}' 
                 WHERE id = {self.car_id}"""
                cur.execute(query)


                messagebox.showinfo("Успешно!", "Успешно добавлено в Базу Данных!")
                con.commit()
            except Exception as e:
                print(e)
                messagebox.showerror("Ошибка", "Не получилось добавить в Базу Данных")
        else:
            messagebox.showerror("Ошибка", "Нельзя оставлять поля пустыми")