import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

con = sqlite3.connect("gruz.bd")
# БД занятого транспорта транспорта
class BusyBases:
    def create_busyBD(self):
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS busy_transport(
                    ID int PRIMARY KEY,
                    Тип text, 
                    Грузоподъёмность real, 
                    Длина real,
                    Ширина real,
                    Высота real   
                    )''')
        con.commit()

    def Insert_busy(self, request):
        cur = con.cursor()
        info = request
        cur.executemany("INSERT INTO busy_transport VALUES (?, ?, ?, ?, ?, ?)", info)
        con.commit()

# БД свободного транспорта
class FreeBases:
    def create_freeBD(self):
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS free_transport(
                    ID int PRIMARY KEY,
                    Тип text, 
                    Грузоподъёмность real, 
                    Длина real,
                    Ширина real,
                    Высота real   
                    )''')
        con.commit()

    def Insert_free(self, id, name, m, l, w, h):
        cur = con.cursor()
        info = [(id, name, m, l, w, h)]
        cur.executemany("INSERT INTO free_transport VALUES (?, ?, ?, ?, ?, ?)", info)
        con.commit()

    def delete_from_Free(self, id):
        cur = con.cursor()
        cur.execute(f"DELETE FROM free_transport WHERE ID={id}")

# БД всего транспорта
class DataBases:
    def create_bd(self):
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS transport(
                    ID int PRIMARY KEY,
                    Тип text, 
                    Грузоподъёмность real, 
                    Длина real,
                    Ширина real,
                    Высота real   
                    )''')
        con.commit()

    def Insert(self, id, name, m, l, w, h):
        cur = con.cursor()
        info = [(id, name, m, l, w, h)]
        cur.executemany("INSERT INTO transport VALUES (?, ?, ?, ?, ?, ?)", info)
        con.commit()


# main menu
class main_window(DataBases, FreeBases, BusyBases):
    def __init__(self):
        self.main_win= Tk()
        self.main_win.title("учет грузового транспорта")
        self.main_win.geometry('1600x768+240+210')
        self.main_win.resizable(False, False)

        self.view_transport=DoubleVar()
        self.view_transport.set(0)
        self.rechange_tr=DoubleVar()
        self.rechange_tr.set(0)

        One=LabelFrame(self.main_win, text="Посмотреть Транспорт", font='Cambria 16', padx=10, pady=10)
        One.pack(fill=BOTH)
        Two=LabelFrame(self.main_win, text="Изменить Список Транспорта", font='Cambria 16', padx=10, pady=10)
        Two.pack(fill=BOTH)
        Tree=LabelFrame(self.main_win, text="Внести Заявку На Траспорт", font='Cambria 16', padx=10, pady=10)
        Tree.pack(fill=BOTH)
        check_vieAdd_window=Radiobutton(text="Просмотреть весь доступный транспорт", variable=self.view_transport, value=0)
        check_view2=Radiobutton(text="Просмотреть транспорт по грузоподъёмности", variable=self.view_transport, value=1)
        check_view3=Radiobutton(text="Просмотреть свободный транспорт", variable=self.view_transport, value=2)
        check_view4=Radiobutton(text="Просмотреть занятый транспорт", variable=self.view_transport, value=3)
        check_vieAdd_window.place(x=700, y=15)
        check_view2.place(x=700, y=35)
        check_view3.place(x=700, y=55)
        check_view4.place(x=700, y=75)

        bt1=Button(One ,text='Показать Траспорт',font='Helvetica 28', command=lambda:self.show_transport_table())
        bt1.pack(side=RIGHT)
        bt2=Button(Two ,text='Добавить грузовой транспорт',font='Helvetica 28', command=lambda:Add_window())
        bt2.pack(side=TOP)
        bt3=Button(Two ,text='Удалить грузовой транспорт',font='Helvetica 28', command=lambda:remove_from_acc())
        bt3.pack(side=RIGHT)
        bt3=Button(Tree, text="Подобрать транспорт", font='Helvetica 28', command=lambda: select_window())
        bt3.grid(column=17, row=3, padx=30, pady=20)
        bt4=Button(Tree, text="Забронировать Нужную Машину", font='Helvetica 30',\
             background='light steel blue', command=lambda:Call_select_window())
        bt4.grid(column=25, row=10, padx=30, pady=80)
        bt5=Button(self.main_win, text="Выход", command=lambda:self.ex_prog())
        bt5.place(x=1500, y=720)
        self.main_win.mainloop()
    def show_transport_table(self):
        if self.view_transport.get()==0:
            window_b = see_all_window()
        if self.view_transport.get()==1:
            window_c = Cargo_window()
        if self.view_transport.get()==2:
            window_f = Free_TS_window()
        if self.view_transport.get()==3:
            window_g = Busy_TS_window()
    def ex_prog(self):
        self.main_win.destroy()
        self.main_win.quit()

# Подбор по параметрам
class select_TS_window(FreeBases, BusyBases):
    def __init__(self, information):
        self.truks=information
        self.window_i=Tk()
        self.window_i.title("Выбор Транспортного Средства")
        self.window_i.geometry('1024x512+340+290')
        scrollFrame=Canvas(self.window_i)
        scrollFrame.pack(expand=True, fill=BOTH)
        tab_tr=Frame(scrollFrame)
        tab_tr.pack(expand=True, fill=BOTH)
        Label(tab_tr, text='ID', font='Helvetica 16').grid(row=0, column=0, padx=15)
        Label(tab_tr, text='Тип', font='Helvetica 16').grid(row=0, column=1, padx=15)
        Label(tab_tr, text='Грузоподъемность', font='Helvetica 16').grid(row=0, column=2, padx=15)
        Label(tab_tr, text='Длина', font='Helvetica 16').grid(row=0, column=3, padx=15)
        Label(tab_tr, text='Ширина', font='Helvetica 16').grid(row=0, column=4, padx=15)
        Label(tab_tr, text='Высота', font='Helvetica 16').grid(row=0, column=5, padx=15)
        for i, item in enumerate(self.truks):
            for col, ttx in enumerate(item):
                if col==1:
                    Button(tab_tr, text=ttx, width=30, height=2, font='Helvetica 9',\
                         command= lambda x=i: self.get_gruz(x)).grid(row=i+1, column=1, padx=9)
                else:
                    Label(tab_tr, text=ttx, width=10, height=2, font='Helvetica 14').grid(row=i+1, column=col, padx=9)
        my_scrollbar=Scrollbar(scrollFrame, orient=VERTICAL, command=scrollFrame.yview)
        scrollFrame.create_window((0, 0), window=tab_tr, anchor="nw")
        scrollFrame.bind("<Configure>", lambda e:scrollFrame.configure(scrollregion=tab_tr.bbox('all')))
        my_scrollbar.pack(side=RIGHT, fill="y")
        self.window_i.mainloop()
    def get_gruz(self, i):
        id=self.truks[i][0]
        self.delete_from_Free(id)
        self.Insert_busy([self.truks[i]])
        messagebox.showinfo('Info', 'Транспортное Средство: '+self.truks[i][1]+' -забронировано')
        self.window_i.destroy()
# Внести заявку по габаритам
class Call_select_window(FreeBases):
    def __init__(self):
        self.window_h=Tk()
        self.window_h.title("Заявка на транспорт")
        self.window_h.geometry("640x240+580+600")
        self.window_h.resizable(0, 0)
        self.label1=Label(self.window_h, text="Масса Груза, т")
        self.label1.grid(row=1, column=0)
        self.entry1=Entry(self.window_h, width=80)
        self.entry1.grid(row=1, column=1)
        self.label2=Label(self.window_h, text="Длина, м")
        self.label2.grid(row=2, column=0)
        self.entry2=Entry(self.window_h, width=80)
        self.entry2.grid(row=2, column=1)
        self.label3=Label(self.window_h, text="Ширина, м")
        self.label3.grid(row=3, column=0)
        self.entry3=Entry(self.window_h, width=80)
        self.entry3.grid(row=3, column=1)
        self.label4=Label(self.window_h, text="Высота, м")
        self.label4.grid(row=4, column=0)
        self.entry4=Entry(self.window_h, width=80)
        self.entry4.grid(row=4, column=1)
        self.b1=Button(self.window_h, text="Подобрать транспорт", font='Cambria 16', background='DarkSeaGreen3',\
            activebackground="#E1B16A",command=self.find_tr).place(x=80, y=110)
        self.window_h.mainloop()

    def find_tr(self):
        try:
            m=float(self.entry1.get())
            l=float(self.entry2.get())
            w=float(self.entry3.get())
            h=float(self.entry4.get())
            if m>0 and l>0 and w>0 and h>0:
                param = []
                c = con.cursor()
                sql="SELECT * FROM free_transport"
                spis=c.execute(sql).fetchall()
                for el in spis:
                    ch_size=bool(el[3]>=l and el[4]>=w and el[5]>=h)
                    if ch_size and el[2]>=m:
                        param.append(el)
                self.window_h.destroy()
                window9 = select_TS_window(param)
            else:
                messagebox.showerror("Ошибка", "Параметры должны быть положительными!")
        except:
            messagebox.showerror("Ошибка", "Неверный ввод данных")

# Посмотреть занятый транспорт
class Busy_TS_window(BusyBases):
    def __init__(self):
        self.window_g=Tk()
        self.window_g.geometry("880x500+700+400")
        self.window_g.title('Занятые Транспортные Средства')
        self.window_g.resizable(0, 0)

        self.heads=["ID", "Тип", "Грузоподъёмность, тонн", "Длина", "Ширина", "Высота"]
        sql = "SELECT * from busy_transport"
        c=con.cursor()
        q = c.execute(sql).fetchall()
        self.table = ttk.Treeview(self.window_g, show='headings')
        self.table['column']=self.heads
        for header in self.heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center', width=2)

        for row in q:
            self.table.insert('', 'end', values=row)

        self.scroll_plane=ttk.Scrollbar(self.window_g, command=self.table.yview)
        self.scroll_plane.pack(side=RIGHT, fill=Y)
        self.table.config(yscroll=self.scroll_plane.set)

        self.table.pack(expand=YES, fill=BOTH)
        self.b1=Button(self.window_g, text="Закрыть", activebackground="#A0522D",
                         command=self.window_g.destroy).pack(side=TOP)
        self.window_g.mainloop()


# Посмотреть свободный транспорт
class Free_TS_window(FreeBases):
    def __init__(self):
        self.window_f=Tk()
        self.window_f.geometry("880x500+800+400")
        self.window_f.title('Свободные Транспортные Средства')
        self.window_f.resizable(0, 0)

        self.heads = ["ID", "Тип", "Грузоподъёмность, тонн", "Длина", "Ширина", "Высота"]
        sql = "SELECT * from free_transport"
        c = con.cursor()
        q = c.execute(sql).fetchall()


        self.table=ttk.Treeview(self.window_f, show='headings')
        self.table['column']=self.heads

        for header in self.heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center', width=2)

        for row in q:
            self.table.insert('', 'end', values=row)

        self.scroll_plane=ttk.Scrollbar(self.window_f, command=self.table.yview)
        self.scroll_plane.pack(side=RIGHT, fill=Y)
        self.table.config(yscroll=self.scroll_plane.set)

        self.table.pack(expand=YES, fill=BOTH)
        self.b1=Button(self.window_f, text="Закрыть", activebackground="#A0522D",
                         command=self.window_f.destroy).pack(side=TOP)
        self.window_f.mainloop()


# Подбор транспорта
class select_window(FreeBases, BusyBases):
    def __init__(self):
        self.window_e=Tk()
        self.window_e.title("Подбор ТС")
        self.window_e.geometry("300x75+1000+500")
        self.window_e.resizable(0, 0)
        self.label1=Label(self.window_e, text="Введите ID транспортного средства,\n которое хотите забронировать")
        self.label1.pack(side=TOP)
        self.entry1=Entry(self.window_e)
        self.entry1.pack(side=TOP)
        self.b1=Button(self.window_e, text="Забронировать", activebackground="#FAB352",
                         command=self.get_gruz).pack(side=BOTTOM)
        self.window_e.mainloop()

    def get_gruz(self):
        try:
            id=int(self.entry1.get())
            sql=f"SELECT * from free_transport WHERE ID={id}"
            c=con.cursor()
            request = c.execute(sql).fetchall()
            if len(request) == 0:
                sql_from_busy = f"SELECT * from busy_transport WHERE ID={id}"
                if len(c.execute(sql_from_busy).fetchall()) == 0:
                    messagebox.showerror("Ошибка", "Транспорта с таким ID не существует")
                else:
                    messagebox.showerror("Ошибка", "Транспорта с таким ID уже забронирован")
            else:
                self.Insert_busy(request)
                self.delete_from_Free(id)
                messagebox.showinfo("Инфо", "Вы успешно забронировали Транспорт")
                self.window_e.destroy()
        except:
            messagebox.showerror("Ошибка", "Неверный ввод данных")


# Удалить ТС
class remove_from_acc(DataBases, FreeBases, BusyBases):
    def __init__(self):
        self.window_d=Tk()
        self.window_d.geometry("300x100+1000+500")
        self.label1=Label(self.window_d, text="Введите ID транспорта, который хотите удалить")
        self.label1.pack(side=TOP)
        self.entry1=Entry(self.window_d)
        self.entry1.pack(side=TOP)
        self.b1=Button(self.window_d, text="Удалить", activebackground="#87CEFA",
                         command=self.delete_from_bd).pack(side=TOP)

        self.window_d.mainloop()

    def delete_from_bd(self):
        try:
            id = int(self.entry1.get())
            if id > 0:
                sql = f"DELETE FROM transport WHERE ID={id}"
                c = con.cursor()
                sql2 = f"SELECT * FROM transport WHERE ID={id}"
                if len(c.execute(sql2).fetchall())==0:
                    messagebox.showerror("Ошибка", "Такого ID не существует")
                else:
                    sql_free_baza =f"SELECT * FROM free_transport WHERE ID={id}"
                    sql_busy_baza =f"SELECT * FROM busy_trasport WHERE ID={id}"
                    if len(c.execute(sql_free_baza).fetchall())!=0:
                        deleting1 = f"DELETE FROM free_transport WHERE ID={id}"
                        c.execute(deleting1)
                    else:
                        deleting2 = f"DELETE FROM busy_transport WHERE ID={id}"
                        c.execute(deleting2)
                    c.execute(sql)
                    con.commit()
                    messagebox.showinfo("Удаление", "Объект удален из базы данных")
                    self.window_d.destroy()
            else:
                messagebox.showerror("Ошибка", "ID не может быть отрицательным!")
        except:
            messagebox.showerror("Ошибка", "Такого ID не существует")


# Сорт по грузоподъёмности
class Cargo_window(FreeBases):
    def __init__(self):
        self.window_c=Tk()
        self.window_c.geometry("880x500+700+400")
        self.window_c.title('Транспорт по грузоподъемности')
        self.window_c.resizable(0, 0)
        #ключ сортировки
        def get_cargo(x):
            return x[2]
        self.heads=["ID", "Тип", "Грузоподъёмность, тонн"]
        sql="SELECT * from free_transport"
        c = con.cursor()
        q =c.execute(sql).fetchall()
        q.sort(key=get_cargo)

        self.table = ttk.Treeview(self.window_c, show='headings')
        self.table['column']=self.heads
        #формирование таблицы
        for header in self.heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center', width=2)

        for row in q:
            self.table.insert('', 'end', values=row)

        self.scroll_plane=ttk.Scrollbar(self.window_c, command=self.table.yview)
        self.scroll_plane.pack(side=RIGHT, fill=Y)
        self.table.config(yscroll=self.scroll_plane.set)

        self.table.pack(expand=YES, fill=BOTH)
        self.b1 = Button(self.window_c, text="Закрыть", activebackground="#A0522D",
                         command=self.window_c.destroy).pack(side=TOP)
        self.window_c.mainloop()

#Все доспупные ТС
class see_all_window(DataBases):
    def __init__(self):
        self.window_b = Tk()
        self.window_b.geometry("880x500+800+400")
        self.window_b.resizable(0, 0)
        self.window_b.title('Доступные Транспортные Средства')
        self.heads=["ID", "Тип", "Грузоподъёмность, тонн", "Длина", "Ширина", "Высота"]
        #обращаемся к базе данных и формируем ttk.Treeview для вывода
        sql="SELECT * from transport"
        c=con.cursor()
        q=c.execute(sql).fetchall()
        

        self.table=ttk.Treeview(self.window_b, show='headings')
        self.table['column']=self.heads

        for header in self.heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center', width=2)

        for row in q:
            self.table.insert('', 'end', values=row)

        self.scroll_plane=ttk.Scrollbar(self.window_b, command=self.table.yview)
        self.scroll_plane.pack(side=RIGHT, fill=Y)
        self.table.config(yscroll=self.scroll_plane.set)

        self.table.pack(expand=YES, fill=BOTH)
        self.b1=Button(self.window_b, text="Закрыть", activebackground="#A0522D",
                         command=self.window_b.destroy).pack(side=TOP)
        self.window_b.mainloop()


# Добавить новый транспорт
class Add_window(DataBases, FreeBases):
    def __init__(self):
        self.window_a=Tk()
        self.window_a.geometry("230x160+1350+400")
        self.window_a.title('Добавление нового ТС')
        self.window_a.resizable(0, 0)
        #id
        self.label0 = Label(self.window_a, text="ID")
        self.label0.grid(row=0, column=0)
        self.entry0 = Entry(self.window_a, width=10)
        self.entry0.grid(row=0, column=1)
        #его характеристики
        self.label1 = Label(self.window_a, text="Тип")
        self.label1.grid(row=1, column=0)
        self.entry1 = Entry(self.window_a, width=10)
        self.entry1.grid(row=1, column=1)
        self.label2 = Label(self.window_a, text="Грузоподъёмность, тонн")
        self.label2.grid(row=2, column=0)
        self.entry2 = Entry(self.window_a, width=10)
        self.entry2.grid(row=2, column=1)
        self.label3 = Label(self.window_a, text="Длина")
        self.label3.grid(row=3, column=0)
        self.entry3 = Entry(self.window_a, width=10)
        self.entry3.grid(row=3, column=1)
        self.label4 = Label(self.window_a, text="Ширина")
        self.label4.grid(row=4, column=0)
        self.entry4 = Entry(self.window_a, width=10)
        self.entry4.grid(row=4, column=1)
        self.label5 = Label(self.window_a, text="Высота")
        self.label5.grid(row=5, column=0)
        self.entry5 = Entry(self.window_a, width=10)
        self.entry5.grid(row=5, column=1)
        self.b1 = Button(self.window_a, text="Добавить", activebackground="#98FB98",
                         command=self.input_info).place(x=160, y=130)
        self.window_a.mainloop()
    #обработка исключений
    def input_info(self):
        try:
            if not str(self.entry1.get()).isdigit():
                a1 = self.entry1.get()
            a0 = int(self.entry0.get())
            a2 = float(self.entry2.get())
            a3 = float(self.entry3.get())
            a4 = float(self.entry4.get())
            a5 = float(self.entry5.get())
            if a2 > 0 and a3 > 0 and a4 > 0 and a5 > 0 and a0 > 0:
                self.Insert(a0, a1, a2, a3, a4, a5)
                self.Insert_free(a0, a1, a2, a3, a4, a5)
                messagebox.showinfo("Добавление в БД", "Транспорт был успешно добавлен")
                self.window_a.destroy()
            else:
                messagebox.showerror("Ошибка", "Неверный ввод данных")
        except:
            messagebox.showerror("Ошибка", "Неверный ввод данных")


if __name__ == "__main__":
    c = con.cursor()
    DB = DataBases()
    DB.create_bd()
    FreDB = FreeBases()
    FreDB.create_freeBD()
    BusyDB = BusyBases()
    BusyDB.create_busyBD()
    App = main_window()
