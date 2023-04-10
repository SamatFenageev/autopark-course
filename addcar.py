from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

con = sqlite3.connect('autopark.db')
cur = con.cursor()

class AddCar(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Добавить Автомобиль")
        self.resizable(False, False)


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
        top_image_lbl.place(x = 120, y = 10)
        heading = Label(self.topFrame, text = 'Добавить Автомобиль', font = 'arial 22 bold', fg = '#003f88', bg = 'white')
        heading.place(x = 290, y = 60)


        ######################### Ввод и его лейблы#########################
        self.lbl_number = Label(self.bottomFrame, text = "Номер", font = 'arial 15 bold', fg = 'white', bg = '#fcc324')
        self.lbl_number.place(x=40, y=40)
        self.ent_number = Entry(self.bottomFrame, width = 31, bd = 4)
        self.ent_number.insert(0, 'Введите номер автомобиля')
        self.ent_number.place(x=300, y=45)
        #бренд
        self.lbl_brand = Label(self.bottomFrame, text="Бренд", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_brand.place(x=40, y=80)
        self.ent_brand = Entry(self.bottomFrame, width=31, bd=4)
        self.ent_brand.insert(0, 'Введите Бренд')
        self.ent_brand.place(x=300, y=85)
        #пробег
        self.lbl_mileage = Label(self.bottomFrame, text="Пробег", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_mileage.place(x=40, y=120)
        self.ent_mileage = Entry(self.bottomFrame, width=31, bd=4)
        self.ent_mileage.insert(0, 'Введите пробег')
        self.ent_mileage.place(x=300, y=125)
        #к-во мест
        self.lbl_seats = Label(self.bottomFrame, text="Количество мест", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_seats.place(x=40, y=160)
        self.ent_seats = Entry(self.bottomFrame, width=31, bd=4)
        self.ent_seats.insert(0, 'Введите Количество мест')
        self.ent_seats.place(x=300, y=165)
        #тип
        self.car_type = StringVar()
        self.lbl_type = Label(self.bottomFrame, text="Тип автомобиля", font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_type.place(x=40, y=200)
        self.ent_type = ttk.Combobox(self.bottomFrame, textvariable=self.car_type)
        self.ent_type['values'] = ["Легковой", "Грузовой"]
        self.ent_type.place(x=300, y=205)

        # кнопка
        button = Button(self.bottomFrame, text = 'Добавить Автомобиль', command = self.addCar)
        button.place(x = 270, y = 280)

    def addCar(self):
        number = self.ent_number.get()
        brand = self.ent_brand.get()
        mileage = self.ent_mileage.get()
        seats = self.ent_seats.get()
        car_type = self.car_type.get()
        try:
            mileage = int(mileage)
            seats = int(seats)
        except:
            messagebox.showerror("Ошибка", "Не получилось добавить в Базу Данных", icon='warning')
        if mileage < 0:
            messagebox.showerror("Ошибка", "Пробег не может быть отрицательным")
        elif number and brand and mileage and seats and car_type:
            try:
                query = f"""INSERT INTO cars 
                    (number, brand, mileage,seats,type) VALUES ('{number}',
                    '{brand}', {int(mileage)}, {int(seats)}, '{car_type}')
                     """
                cur.execute(query)
                con.commit()
                messagebox.showinfo('Успешно', 'Успешно добавлено в Базу Данных', icon='info')

            except Exception as e:
                print(e)
                messagebox.showerror("Ошибка", "Не получилось добавить в Базу Данных", icon='warning')
        else:
            messagebox.showerror("Ошибка", "Поле не может быть пустым", icon='warning')