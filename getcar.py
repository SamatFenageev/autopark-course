from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import datetime

con = sqlite3.connect("autopark.db")
cur = con.cursor()

class GetCar(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+220")
        self.title("Вернуть Автомобиль")
        self.resizable(False, False)

        query2 = """SELECT * FROM users WHERE id IN 
                    (SELECT DISTINCT user_id FROM issuance WHERE return_date='')
                    """
        members = cur.execute(query2).fetchall()
        member_list = []
        for member in members:
            member_list.append(str(member[0]) + " - " + member[1])


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
        heading = Label(self.topFrame, text='Вернуть Автомобиль', font='arial 22 bold', fg='#003f88', bg='white')
        heading.place(x=290, y=60)

        ######################### вводы и лейблы #########################
        if members:
            # сотруд
            self.member_name = StringVar()
            self.lbl_phone = Label(self.bottomFrame, text="ID Сотрудинка: ", font='arial 15 bold', fg='white',
                                   bg='#fcc324')
            self.lbl_phone.place(x=40, y=40)
            self.combo_member = ttk.Combobox(self.bottomFrame, textvariable=self.member_name, postcommand = self.findUserByCar)
            self.combo_member['values'] = member_list
            self.combo_member.place(x=210, y=45)

            # машина
            self.car_name = StringVar()
            self.lbl_name = Label(self.bottomFrame, text="Автомобиль: ", font='arial 15 bold', fg='white', bg='#fcc324')
            self.lbl_name.place(x=40, y=80)
            self.combo_name = ttk.Combobox(self.bottomFrame, textvariable = self.car_name, postcommand = self.findCarByUser)
            self.combo_name.place(x = 210, y = 85)


            # кнопка
            button = Button(self.bottomFrame, text='Вернуть Автомобиль', command = self.returnCar)
            button.place(x=220, y=120)
        else:
            self.lbl_noissueance = Label(self.bottomFrame, text="Все Автомобили в Автопарке\nВозвращать нечего", font='arial 25 bold', fg='white',
                                  bg='#fcc324')
            self.lbl_noissueance.place(x=130, y=80)

    def findCarByUser(self):
        cars_list = [""]
        if self.member_name.get():
            query = f"""
                    SELECT id, number, brand FROM cars WHERE id IN (SELECT car_id FROM issuance WHERE 
                    user_id = {self.member_name.get()[0]} AND return_date = '')
                    """
            cars = cur.execute(query).fetchall()
            for car in cars:
                cars_list.append(str(car[0]) + " - " + car[1] + " - " + car[2])
        else:
            query = """SELECT * FROM cars WHERE id IN
                    (SELECT car_id FROM issuance WHERE return_date = '')
            """

            cars = cur.execute(query).fetchall()
            for car in cars:
                cars_list.append(str(car[0]) + " - " + car[1] + " - " + car[2])
        self.combo_name['values'] = cars_list

    def findUserByCar(self):
        users_list = [""]
        if self.car_name.get():
            query = f"""
                    SELECT user_id FROM issuance WHERE car_id = {self.car_name.get()[0]}
                    AND return_date = ''
                    """
            user_id = cur.execute(query).fetchone()[0]
            query2 = f"""
                        SELECT * FROM users WHERE id = {user_id}
                        """
            user = cur.execute(query2).fetchone()
            users_list.append(str(user[0]) + " - " + user[1])
        else:
            query = """SELECT * FROM users WHERE id IN
                        (SELECT user_id FROM issuance WHERE return_date = '')
                    """
            users = cur.execute(query).fetchall()
            for user in users:
                users_list.append(str(user[0]) + " - " + user[1])
        self.combo_member['values'] = users_list
    def returnCar(self):
        car_name = self.car_name.get()
        self.car_id = car_name.split('-')[0]

        self.user_id = self.member_name.get()[0]


        if self.car_id and self.user_id:
            try:
                query = f"""
                        UPDATE issuance SET return_date = '{str(datetime.date.today())}'
                        WHERE id IN (SELECT id FROM issuance 
                        WHERE return_date = '' AND user_id = {self.user_id} AND  car_id = {self.car_id}) 
                        """
                cur.execute(query)
                query2 = f"""
                            UPDATE cars SET status = 0
                        WHERE id = {self.car_id}
                            """
                cur.execute(query2)
                messagebox.showinfo("Успешно!", "Успешно добавлено в Базу Данных!")
                con.commit()
            except Exception as e:
                print(e)
                messagebox.showerror("Ошибка", "Не получилось добавить в Базу Данных")

        else:
            messagebox.showerror("Ошибка", "Нельзя оставлять поля пустыми")