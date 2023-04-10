from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

con = sqlite3.connect('autopark.db')
cur = con.cursor()

class EditCar(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Изменить Данные Автомобиля")
        self.resizable(False, False)

        query2 = "SELECT * FROM cars"
        cars = cur.execute(query2).fetchall()
        cars_list = []
        for car in cars:
            cars_list.append(str(car[0]) + " - " + car[1] + " - " + car[2])

        ################### Рамки #########################

        #верхняя рамка
        self.topFrame = Frame(self, height = 150, bg = 'white')
        self.topFrame.pack(fill=X)

        #нижняя рамка
        self.bottomFrame = Frame(self, height = 600, bg = '#fcc324')
        self.bottomFrame.pack(fill=X)

        #заголовок, изображение
        self.top_image = PhotoImage(file = 'icons/add_book.png')
        top_image_lbl = Label(self.topFrame, image = self.top_image, bg = 'white')
        top_image_lbl.place(x = 50, y = 10)
        heading = Label(self.topFrame, text = 'Изменить Данные Автомобиля', font = 'arial 22 bold', fg = '#003f88', bg = 'white')
        heading.place(x = 170, y = 60)

        ######################### Ввод и его лейблы#########################
        self.car_name = StringVar()
        self.lbl_name = Label(self.bottomFrame, text="Автомобиль: ", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_name.place(x=40, y=40)
        self.combo_name = ttk.Combobox(self.bottomFrame, textvariable=self.car_name)
        self.combo_name['values'] = cars_list
        self.combo_name.place(x=180, y=45)
        #пробег
        self.lbl_mileage = Label(self.bottomFrame, text="Пробег: ", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_mileage.place(x=40, y=80)
        self.ent_mileage = Entry(self.bottomFrame, width=31, bd=4)
        self.ent_mileage.insert(0, f'Введите пробег')
        self.ent_mileage.place(x=150, y=85)

        # кнопка
        button = Button(self.bottomFrame, text = 'Изменить Данные Автомобиля', command = self.addBook)
        button.place(x = 150, y = 130)

    def addBook(self):
        query = f"""
                            SELECT mileage FROM cars WHERE id = {self.car_name.get()[0]}
                        """
        car_mileage = cur.execute(query).fetchone()[0]
        new_mileage = int(self.ent_mileage.get())
        if new_mileage < 0 or new_mileage <= car_mileage:
            messagebox.showerror("Ошибка", "Пробег не может быть отрицательным или меньше уже имеющегося")
        elif new_mileage:
            try:
                query = f"""INSERT INTO cars 
                    (mileage) VALUES ({new_mileage})
                     """
                cur.execute(query)
                con.commit()
                messagebox.showinfo('Успешно', 'Успешно добавлено в БД', icon='info')

            except Exception as e:
                print(e)
                messagebox.showerror("Ошибка", "Не получилось добавить в БД", icon='warning')
        else:
            messagebox.showerror("Ошибка", "Поле не может быть пустым", icon='warning')


