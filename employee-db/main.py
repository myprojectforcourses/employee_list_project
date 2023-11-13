import tkinter as tk
from tkinter import ttk
import sqlite3

#Главное окно
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db


    #Параметры окна
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file='./img/add.png')
        button_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0,
        image=self.add_img, command=self.open_dialog, compound=tk.TOP)
        button_open_dialog.pack(side=tk.LEFT)

        #Вывод TreeView с данными
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'telephone', 'email', 'salary'),
                                 height=45, show='headings')
        
        

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=170, anchor=tk.CENTER)
        self.tree.column('telephone', width=125, anchor=tk.CENTER)
        self.tree.column('email', width=170, anchor=tk.CENTER)
        self.tree.column('salary', width=75, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='Имя')
        self.tree.heading('telephone', text='Номер телефона')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='З/п')

        self.tree.pack(side=tk.LEFT)

        #Кнопка обновления данных
        self.update_img = tk.PhotoImage(file='./img/update.png')
        button_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', image=self.update_img, bd=0, command=self.open_update_dialogue, 
                                       )
        button_edit_dialog.pack(side=tk.LEFT)
        
        #Кнопка удаления данных
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        button_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', image=self.delete_img, bd=0, command=self.delete_records,
                                       )
        button_edit_dialog.pack(side=tk.LEFT)

    def open_dialog(self):
        Child() #Метод вывода окна с добавлением данных

    #Метод удаления данных
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''
        DELETE FROM db WHERE id = ?
                              ''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()     
    
    def records(self, name, telephone, email, salary):
        self.db.insert_data(name, telephone, email, salary)
        self.view_records()

    #Метод вывода окна с редактированием данных
    def open_update_dialogue(self):
        Update()

    #Метод просмотра данных
    def view_records(self):
        self.db.c.execute('''SELECT * FROM db''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    #Метод редактирования данных
    def update_record(self, name, telephone, email, salary):
        self.db.c.execute('''
        UPDATE db SET name=?, telephone=?, email=?, salary=? WHERE ID =?
                          ''', (name, telephone, email, salary,
                                self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

#Класс окна с добавлением данных
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        #Параметры окна
        self.title('Добавить')
        self.geometry('400x200') 
        self.resizable(False, False)
        #Перехват фокуса
        self.grab_set()
        self.focus_set()

        #Названия полей данных для ввода
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=50)
        label_telephone = tk.Label(self, text='Номер телефона')
        label_telephone.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail')
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text='Заработная плата')
        label_salary.place(x=50, y=140)

        #Поля ввода данных
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_telephone = ttk.Entry(self)
        self.entry_telephone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        #Кнопка для закрытия окна
        self.button_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.button_cancel.place (x=300, y = 170)

        #Кнопка для подтверждения добавления данных 
        self.button_add = ttk.Button(self, text='Добавить')
        self.button_add.place(x=220, y=170)
        self.button_add.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(), 
                                                                           self.entry_telephone.get(),
                                                                           self.entry_email.get(),
                                                                           self.entry_salary.get()))





        
#Класс окна с редактированием данных
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    #Параметры окна
    def init_edit(self):
        self.title('Редактировать данные')
        button_edit = ttk.Button(self, text='Редактировать')
        button_edit.place(x=205, y=170)

        #Кнопка подтверждения редактирования данных
        button_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(), 
                                                                          self.entry_telephone.get(),
                                                                          self.entry_email.get(),
                                                                          self.entry_salary.get()))
        button_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.button_add.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM db WHERE id=?''', (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[0])
        self.entry_telephone.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_salary.insert(0, row[3])

#База данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()
        self.c.execute('''
        CREATE TABLE IF NOT EXISTS db (id integer primary key, name text, telephone text, email text, salary text)
                       ''')
        self.conn.commit()

    def insert_data(self, name, telephone, email, salary):
        self.c.execute(''' INSERT INTO db (name, telephone, email, salary) VALUES (?, ?, ?, ?)
                       ''', (name, telephone, email, salary))
        self.conn.commit()

#Параметры окна, основные функции для работы приложения
if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Список сотрудников компании")
    root.geometry("655x450")
    root.resizable(False, False)
    root.mainloop()
