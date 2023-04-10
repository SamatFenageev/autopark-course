from tkinter import *
from tkinter import ttk
import sqlite3
import addcar, addmember, givecar, getcar, editauto
from tkinter import messagebox


con = sqlite3.connect("autopark.db")
cur = con.cursor()

class Main(object):
    def __init__(self, master):
        self.master = master
        def displayStatictics(evt):
            count_cars = cur.execute("SELECT count(id) FROM cars").fetchone()[0]
            count_members = cur.execute("SELECT count(id) FROM users").fetchone()[0]
            taken_cars = cur.execute("SELECT count(id) FROM issuance WHERE return_date = ''").fetchall()[0][0]

            self.lbl_member_count.config(text = "Всего сотрудников: " + str(count_members))
            self.lbl_cars.config(text = "Всего машин: " + str(count_cars))
            self.lbl_taken_count.config(text = 'Взятых машин: ' + str(taken_cars))
            displayCars(self)

        def displayCars(self):
            cars = cur.execute("SELECT * FROM cars").fetchall()
            count = 0
            self.list_cars.delete(0, END)
            for car in cars:
                self.list_cars.insert(count, str(car[0])+"-"+car[1] + " " + car[2])
                count += 1
            def carInfo(event):
                value = str(self.list_cars.get(self.list_cars.curselection()))
                id = value.split('-')[0]
                car = cur.execute("SELECT * FROM cars WHERE id=?", (id,))
                car_info = car.fetchall()

                self.list_details.delete(0, 'end')
                self.list_details.insert(0, "Номер машины: " + car_info[0][1])
                self.list_details.insert(1, "Марка: " + car_info[0][2])

                self.list_details.insert(2, "Пробег: " + str(car_info[0][3]))
                self.list_details.insert(3, "Количество мест: " + str(car_info[0][4]))
                self.list_details.insert(4, "Тип автомобиля: " + car_info[0][5])
                last_TO = ''
                if not car_info[0][5]:
                    last_TO = 'Тех обслуживание Не проводилось'
                else:
                    last_TO = car_info[0][6]

                self.list_details.insert(5, "Последняя Выдача: " + last_TO)
                car_user_query = f"""
                                    SELECT id,username FROM users WHERE
                                    id IN (SELECT user_id FROM issuance WHERE return_date=''
                                    AND car_id={car_info[0][0]} )
                                    """
                car_user = cur.execute(car_user_query).fetchone()
                if car_info[0][7]:
                    issue = cur.execute(
                        f"""SELECT issue FROM issuance WHERE return_date='' AND car_id={car_info[0][0]}""").fetchone()[0]
                    self.list_details.insert(6, "Статус Автомобиля: занят ")
                    self.list_details.insert(7, "Причина выдачи: " + issue)
                else:
                    self.list_details.insert(6, "Статус Автомобиля: Доступен")

            def doubleClick(evt):
                global given_id
                value = str(self.list_cars.get(self.list_cars.curselection()))
                given_id = value.split('-')[0]
                give_car = givecar.GiveCar()

            self.list_cars.bind('<<ListboxSelect>>', carInfo)
            self.tabs.bind('<<NotebookTabChanged>>', displayStatictics)
            self.list_cars.bind('<Double-Button-1>', doubleClick)

        def displayMembers(self):
            members = cur.execute("SELECT * FROM users").fetchall()
            count = 0
            self.list_members.delete(0, END)
            for member in members:
                self.list_members.insert(count, str(member[0]) + "-" + member[1])
                count += 1

            def userInfo(event):
                value = str(self.list_members.get(self.list_members.curselection()))
                id = value.split('-')[0]
                member = cur.execute("SELECT * FROM users WHERE id=?", (id,))
                member_info = member.fetchall()
                self.list_members_details.delete(0, 'end')
                self.list_members_details.insert(0, "Сотрудник: " + member_info[0][1])
                self.list_members_details.insert(1, "Пасспортные данные: " + member_info[0][2])
                self.list_members_details.insert(2, "Телефон: " + member_info[0][3])
                self.list_members_details.insert(3, "Отдел: " + str(member_info[0][4]))

            self.list_members.bind('<<ListboxSelect>>', userInfo)

        #главная часть
        mainFrame = Frame(self.master)
        mainFrame.pack()

        #верхняя часть
        topFrame = Frame(mainFrame, width = 1350, height = 70, bg = '#f8f8f8', padx = 20, relief = SUNKEN, borderwidth = 2)
        topFrame.pack(side = TOP, fill = X)

        #центральная часть
        centerFrame = Frame(mainFrame, width = 1350, relief = RIDGE, bg = '#e0f0f0', height = 680)
        centerFrame.pack(side = TOP)

        #левая в центральной
        centerLeftFrame = Frame(centerFrame, width = 900, height = 700, bg = '#e0f0f0', borderwidth = 2, relief = 'sunken')
        centerLeftFrame.pack(side = LEFT)

        #правая в центральной
        centerRightFrame = Frame(centerFrame, width = 450, height = 700, bg = '#e0f0f0', borderwidth = 2, relief = 'sunken')
        centerRightFrame.pack()

        #поисковая строка
        searchBar = LabelFrame(centerRightFrame, width = 440, height = 175, text = 'Поиск', bg = '#9bc9ff')
        searchBar.pack(fill = BOTH)
        self.lbl_search = Label(searchBar, text = 'Поиск', font = 'arial 12 bold', bg = '#9bc9ff', fg = 'white')
        self.lbl_search.grid(row = 0, column = 0, padx = 20, pady = 10)
        self.ent_search = Entry(searchBar, width = 30, bd = 10)
        self.ent_search.grid(row = 0, column = 1, columnspan = 3, padx = 10, pady = 10)
        self.btn_search = Button(searchBar, text = 'Поиск', font = 'arial 12', bg = '#fcc324', fg = 'white',
                                 command = self.searchCars)
        self.btn_search.grid(row = 0, column = 4, padx = 20, pady = 10)

        #список
        listBar = LabelFrame(centerRightFrame, width = 440, height = 175, text = 'Список', bg = '#fcc324')
        listBar.pack(fill = BOTH)
        lbl_list = Label(listBar, text = 'Отсортировать по:', font = 'times 16 bold', fg  = '#2488ff', bg = '#fcc324')
        lbl_list.grid(row = 0, column = 1)

        self.listChoice = IntVar()
        rb1 = Radiobutton(listBar, text = 'Все автомобили', var = self.listChoice, value = 1, bg = '#fcc324')
        rb2 = Radiobutton(listBar, text = 'Доступные автомобили', var = self.listChoice, value = 2, bg = '#fcc324')
        rb3 = Radiobutton(listBar, text = 'Взятые автомобили', var = self.listChoice, value = 3, bg = '#fcc324')
        rb1.grid(row = 1, column = 0)
        rb2.grid(row = 1, column = 1)
        rb3.grid(row = 1, column = 2)
        btn_list = Button(listBar, text = 'Список автомобилей', bg = '#2488ff', fg = 'white', font = 'arial 12', command = self.listCars)
        btn_list.grid(row = 2, column = 1, padx = 40, pady = 10)

        #заголовок и картинка
        image_bar = Frame(centerRightFrame, width = 440, height = 350)
        image_bar.pack(fill = BOTH)
        self.title_right = Label(image_bar, text = 'Добро пожаловать в Автопарк Компании', font = 'arial 16 bold')
        self.title_right.grid(row = 0)
        self.img_library = PhotoImage(file = 'icons/cars.png')
        self.lblImg = Label(image_bar, image = self.img_library)
        self.lblImg.grid(row = 1)

########################### СТРОКА ИНСТРУМЕНТОВ ###################################

        #добавить авто
        self.iconCar = PhotoImage(file = 'icons/add_book.png')
        self.btnCar = Button(topFrame, text = 'Добавить Автомобиль', image = self.iconCar,
                              compound = LEFT, font = 'arial 12 bold', command = self.addCar)
        self.btnCar.pack(side = LEFT, padx = 10)

        #добавить читателя
        self.iconMember = PhotoImage(file = 'icons/add_member.png')
        self.btnMember = Button(topFrame, text = 'Добавить Сотрудника', font = 'arial 12 bold', padx = 10, command = self.addMember)
        self.btnMember.configure(image = self.iconMember, compound = LEFT)
        self.btnMember.pack(side = LEFT)

        #дать авто
        self.iconGive = PhotoImage(file = 'icons/give_book.png')
        self.btnGive = Button(topFrame, text = 'Выдать Автомобиль', font = 'arial 12 bold', padx = 10, image = self.iconGive, compound = LEFT, command = self.giveCar)
        self.btnGive.pack(side = LEFT)

        # вернуть авто
        self.iconGet = PhotoImage(file='icons/give_book.png')
        self.btnGet = Button(topFrame, text='Вернуть Автомобиль', font='arial 12 bold', padx=10, image=self.iconGive, compound=LEFT, command=self.getCar)
        self.btnGet.pack(side=LEFT)
        #редактировать
        self.iconEdit = PhotoImage(file='icons/edit.png')
        self.btnEdit = Button(topFrame, text='Изменить Данные Автомобиля', image=self.iconEdit,
                             compound=LEFT, font='arial 12 bold', command=self.editCar)
        self.btnEdit.pack(side=LEFT, padx=10)
################################ Таблички #####################################

        self.tabs = ttk.Notebook(centerLeftFrame, width = 900, height = 660)
        self.tabs.pack()
        ######################## tab1 ############################
        self.tab1_icon = PhotoImage(file = 'icons/give_book.png')
        self.tab2_icon = PhotoImage(file = 'icons/give_book.png')
        self.tab3_icon = PhotoImage(file = 'icons/give_book.png')
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tab3 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab1, text = 'Управление Автопарком', image = self.tab1_icon, compound = LEFT)
        self.tabs.add(self.tab2, text = 'Статистика', image = self.tab2_icon, compound = LEFT)
        self.tabs.add(self.tab3, text='Сотрудники', image=self.tab2_icon, compound=LEFT)

        #список авто
        self.list_cars = Listbox(self.tab1, width = 40, height = 30, bd = 5, font = 'times 12 bold')
        self.sb = Scrollbar(self.tab1, orient = VERTICAL)
        self.list_cars.grid(row = 0, column = 0, padx = (10, 0), pady = 10, sticky = N)
        self.sb.config(command = self.list_cars.yview)
        self.list_cars.config(yscrollcommand = self.sb.set)
        self.sb.grid(row = 0, column = 0, sticky = N + S + E)

        self.list_members = Listbox(self.tab3, width=40, height=30, bd=5, font='times 12 bold')
        self.sb_members = Scrollbar(self.tab3, orient=VERTICAL)
        self.list_members.grid(row=0, column=0, padx=(10, 0), pady=10, sticky=N)
        self.sb_members.config(command=self.list_members.yview)
        self.list_members.config(yscrollcommand=self.sb_members.set)
        self.sb_members.grid(row=0, column=0, sticky=N + S + E)
        self.list_members_details = Listbox(self.tab3, width=80, height=303, bd=5, font='times 12 bold')
        self.list_members_details.grid(row=0, column=1, padx=(10, 0), pady=10, sticky=N)

        #описание авто
        self.list_details = Listbox(self.tab1, width = 80, height = 303, bd = 5, font = 'times 12 bold')
        self.list_details.grid(row = 0, column = 1, padx = (10,0), pady = 10, sticky = N)

        ########################### tab2 ###########################
        #статистика
        self.lbl_cars = Label(self.tab2, text = '', pady = 20, font = 'verdana 14 bold')
        self.lbl_cars.grid(row = 0)
        self.lbl_member_count = Label(self.tab2, text = '', pady = 20, font = 'verdana 14 bold')
        self.lbl_member_count.grid(row = 2, sticky = W)
        self.lbl_taken_count = Label(self.tab2, text = '', pady = 20, font = 'verdana 14 bold')
        self.lbl_taken_count.grid(row = 3, sticky = W)

        #функции
        displayCars(self)
        displayStatictics(self)
        displayMembers(self)
    def addCar(self):
        add = addcar.AddCar()
    def addMember(self):
        member = addmember.AddMember()
    def editCar(self):
        edit = editauto.EditCar()
    def searchCars(self):
        value = self.ent_search.get()
        search = cur.execute("SELECT * FROM cars WHERE number LIKE ?", ('%'+value+'%',)).fetchall()

        self.list_cars.delete(0, END)
        count = 0
        for car in search:
            self.list_cars.insert(count, str(car[0]) + '-' + car[1] + " " + car[2])
            count += 1
    def listCars(self):
        value = self.listChoice.get()
        if value == 1:
            allCars = cur.execute('SELECT * FROM Cars').fetchall()
            self.list_cars.delete(0, END)

            count = 0
            for car in allCars:
                self.list_cars.insert(count, str(car[0]) + ' - '+car[1] + " " + car[2])
                count += 1
        elif value == 2:
            cars_in_autopark = cur.execute("SELECT * FROM Cars WHERE status = ?",(0,)).fetchall()
            self.list_cars.delete(0, END)

            count = 0
            for car in cars_in_autopark:
                self.list_cars.insert(count, str(car[0]) + ' - ' + car[1] + " " + car[2])
                count += 1
        else:

            taken_cars = cur.execute("SELECT * FROM cars WHERE status = ?",(1,)).fetchall()
            self.list_cars.delete(0, END)

            count = 0
            for car in taken_cars:
                self.list_cars.insert(count, str(car[0]) + ' - ' + car[1] + " " + car[2])
                count += 1
    def getCar(self):
        get_book = getcar.GetCar()
    def giveCar(self):
        give_book = givecar.GiveCar()



def main():
    root = Tk()
    app = Main(root)
    root.title("Автопарк")
    root.geometry("1350x750+350+200")
    root.iconbitmap() #иконки
    root.mainloop()
if __name__ == "__main__":
    main()