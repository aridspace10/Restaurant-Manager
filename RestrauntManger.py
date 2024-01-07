from msilib.schema import Class
import tkinter as tk
from tkinter.ttk import Label
from tkinter import Menu, messagebox
import datetime
import sqlite3 as sql
from functools import partial, total_ordering
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

DIMENSIONS = "1200x800"
DATABASE = 'Manage.db'
DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
DATE = datetime.datetime.now()
['Raw items', 'Proccessed items', 'Menu Items']
TYPE_TO_DATABASE = {
    'Raw items': 'RawItems',
    'Proccessed items': 'ProccessedItems',
    'Foods': 'Foods',
    'Drinks': 'Drinks'
}


OPTIONS = ['Total Revenue', 'Food Revenue', 'Drink Revenue', 'Total Cost', 
           'Food Cost', 'Drink Cost', 'Hours worked', 'Profit/Loss', 'Amount of Orders'
          ]

with sql.connect(DATABASE) as conn:
    cursor = conn.cursor()
    for y in ['Foods', 'Drinks']:
        cursor.execute('SELECT Name FROM ' + y)
        data = cursor.fetchall()
        for x in data:
            OPTIONS.append(x[0] + ' Sold')
    


BUTTONS = {}

class User():
    def __init__(self):
        self.ID = ''
        self.f_name = ''

user = User()

class Abstract():
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.master.title("Restraunt Manager")
        self.master.geometry(DIMENSIONS)
        self.master.configure(bg='light green')
        
        self._draw()

    def get_date(date: datetime = datetime.datetime.now()) -> str:
        date = str(date)
        return (date[8:10] + "/" + date[5:7] + "/" + date[0:4])

    def get_time(date: datetime = datetime.datetime.now()) -> str:
        return str(date)[11:16]
    
    def clear(self, instance) -> None:
        ''' Clear all tkinter widgets from screen 
        
        Parameters:
            instance: frame or root which needs to be cleared
        '''
        
        for widgets in instance.winfo_children():
            widgets.destroy()
    
    def _draw(self) -> None:
        raise NotImplementedError
    
    def go_there(self, page) -> None:
        ''' Destories current screen and displays the given screen
        
        Parameters:
            page: class of the screen wanted to be displayed
        '''
        self.master.destroy()
        root = tk.Tk()
        app = page(root)

    def redraw(self) -> None:
        self.clear(self.master)
        self._draw()
    
    def retreive_all_order_day(self, day = get_date()) -> list:
        """ Retreive all order made on the day

        Parameter:
            day: day we want to retreive with default being todays date
        """
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Orders')
            orders = cursor.fetchall()
            day_order = []
            for order in orders:
                if order[2] == self.get_date():
                    day_order.append(order)
        return day_order
    
    def calculate_total_order(self, orderID: str, type: list[str,str]) -> int:
        '''Calculates the total food or drink revenue from an order
        
        Parameters:
            orderID: the id of the order
            type: str1 is either food or drink and str2 is either price or cost
        '''
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            revenue = 0
            cursor.execute('SELECT * FROM Order' + type[0] + ' WHERE OrderID = ?', (orderID,))
            items = cursor.fetchall()
            for item in items:
                cursor.execute('SELECT ' + type[1] + ' FROM ' + type[0] + 's WHERE ' + type[0] + 'ID = ?', (item[1],))
                revenue += cursor.fetchall()[0][0] * item[2]
            return revenue

class menu(Abstract):
    def __init__(self,master: tk.Tk):
        super().__init__(master)
        self.code = ''
    
    def _draw(self) -> None:
        self.title = tk.Label(self.master, text = 'Enter your Pin', bg = 'light green', font = ('Calibri',45))
        self.title.pack(side = tk.TOP, pady= 10)

        self.codevar = tk.StringVar()
        self.CodeEntry = tk.Entry(self.master, width = 7, textvariable = self.codevar, font = ('Calibri',45))
        self.CodeEntry.pack(side = tk.TOP, pady = (100,0))

        self.user_code = tk.Frame(self.master)
        self.user_code.pack(anchor = 'center')
        
        self.Btn9 = tk.Button(self.user_code, text = '9', width = 9, height = 5, command = lambda: self.entry('9'))
        self.Btn9.grid(row = 1, column = 1)
        self.Btn8 = tk.Button(self.user_code, text = '8', width = 9, height = 5, command = lambda: self.entry('8'))
        self.Btn8.grid(row = 1, column = 2)
        self.Btn7 = tk.Button(self.user_code, text = '7', width = 9, height = 5, command = lambda: self.entry('7'))
        self.Btn7.grid(row = 1, column = 3)
        self.Btn6 = tk.Button(self.user_code, text = '6', width = 9, height = 5, command = lambda: self.entry('6'))
        self.Btn6.grid(row = 2, column = 1)
        self.Btn5 = tk.Button(self.user_code, text = '5', width = 9, height = 5, command = lambda: self.entry('5'))
        self.Btn5.grid(row = 2, column = 2)
        self.Btn4 = tk.Button(self.user_code, text = '4', width = 9, height = 5, command = lambda: self.entry('4'))
        self.Btn4.grid(row = 2, column = 3)
        self.Btn3 = tk.Button(self.user_code, text = '3', width = 9, height = 5, command = lambda: self.entry('3'))
        self.Btn3.grid(row = 3, column = 1)
        self.Btn2 = tk.Button(self.user_code, text = '2', width = 9, height = 5, command = lambda: self.entry('2'))
        self.Btn2.grid(row = 3, column = 2)
        self.Btn1 = tk.Button(self.user_code, text = '1', width = 9, height = 5, command = lambda: self.entry('1'))
        self.Btn1.grid(row = 3, column = 3)
        self.Btn0 = tk.Button(self.user_code, text = '0', width = 9, height = 5, command = lambda: self.entry('0'))
        self.Btn0.grid(row = 4, column = 1)
        self.EnterBtn = tk.Button(self.user_code, text = 'Enter', width = 9, height = 5, command = self.enter)
        self.EnterBtn.grid(row = 4, column = 2)
        self.ClearBtn = tk.Button(self.user_code, text = 'Clear', width = 9, height = 5, command = self.clear)
        self.ClearBtn.grid(row = 4, column = 3)

    def entry(self, num: str) -> None:
        ''' Adds a number to the code displayed 
        
        Parameters:
            num: the number to be added
        '''
        self.CodeEntry.config(fg = 'black')
        if len(self.code) < 4:
            self.code += num
            self.codevar.set(self.code)
    def clear(self) -> None:
        self.code = ''
        self.CodeEntry.config(fg = 'black')
        self.codevar.set(self.code)
    def enter(self) -> None:
        if self.code == '0000':
            user.ID = 0
            user.f_name = 'Admin'
            self.go_there(manage)
        else:
            with sql.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT FName FROM Employee WHERE EmployeeNum = ?', (self.code,))
                data = cursor.fetchall()
                if len(data) > 0:
                    user.ID = self.code
                    user.f_name = data[0][0]
                    self.go_there(manage)
                else:
                    self.CodeEntry.config(fg = 'red')


class manage(Abstract):
    def _draw(self) -> None:
        if user.f_name == 'Admin':
            self._draw_admin() 
        else:
            self._draw_member()

    def _draw_admin(self) -> None:
        self.TitleLabel = tk.Label(self.master, highlightbackground="black", highlightthickness=2, bg = 'purple', text = 'Restaurant Manager',font = ('Calibri', 40))
        self.TitleLabel.pack(side = tk.TOP, pady = 20)

        self.buttons = tk.Frame(self.master, bg = 'purple')
        self.buttons.pack()

        self.EmployeeInfoBtn = tk.Button(self.buttons, text = 'Employee Info', command = lambda: self.go_there(EmployeeInfo))
        self.EmployeeInfoBtn.grid(row = 1, column= 1, padx = 20, pady = 20, ipadx = 20, ipady = 20)
        
        self.RosterBtn = tk.Button(self.buttons, text = 'Roster', command = lambda: self.go_there(Roster))
        self.RosterBtn.grid(row = 1, column= 2, padx = 20, pady = 20, ipadx = 20, ipady = 20)

        self.DailyStatsBtn = tk.Button(self.buttons, text = 'Daily Stats', command = lambda: self.go_there(Daily))
        self.DailyStatsBtn.grid(row = 1, column= 3, padx = 20, pady = 20, ipadx = 20, ipady = 20)

        self.StasticsBtn = tk.Button(self.buttons, text = 'Stastics', command = lambda: self.go_there(Stastics))
        self.StasticsBtn.grid(row = 1, column= 4, padx = 20, pady = 20, ipadx = 20, ipady = 20)

        self.OrderScreenBtn = tk.Button(self.buttons, text = 'Orders Screen', command = lambda: self.go_there(OrderScreen))
        self.OrderScreenBtn.grid(row = 1, column= 5, padx = 20, pady = 20, ipadx = 20, ipady = 20)

        self.registerScreenBtn = tk.Button(self.buttons, text = 'Register Screen', command = lambda: self.go_there(RegisterScreen))
        self.registerScreenBtn.grid(row = 2, column= 1, padx = 20, pady = 20, ipadx = 20, ipady = 20)

        self.itemsScreenBtn = tk.Button(self.buttons, text = 'Items', command = lambda: self.go_there(ItemScreen))
        self.itemsScreenBtn.grid(row = 2, column= 2, padx = 20, pady = 20, ipadx = 20, ipady = 20)

        self.RosteringSystemScreenBtn = tk.Button(self.buttons, text = 'Rostering System', command = lambda: self.go_there(RosteringSystem))
        self.RosteringSystemScreenBtn.grid(row = 2, column= 3, padx = 20, pady = 20, ipadx = 20, ipady = 20)
    
    def _draw_member(self) -> None:
        self.welcome_label = tk.Label(self.master, text = 'Welcome ' + user.f_name, bg = 'light green', font = ('Calibri', 40))
        self.welcome_label.pack(side = tk.TOP, pady = 20)

        self.frame = tk.Frame(self.master, bg = 'purple')
        self.frame.pack(side=tk.TOP)

        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Working WHERE EmployeeNum = ?', (user.ID,))
            data = cursor.fetchall()
            if len(data) > 0:
                self.time_working_label = tk.Label(self.frame, text = 'You have been working for ' + str(self.calculate_time()) + ' Hours', bg = 'purple')
                self.time_working_label.pack(side= tk.TOP)

                self.punch_out_btn = tk.Button(self.frame, text = 'Punch Out', command = self.punch_out)
                self.punch_out_btn.pack(side= tk.RIGHT, padx = 5)

                if self.on_break() == False:
                    self.break_btn = tk.Button(self.frame, text = 'Start Break', command = self.start_break)
                    self.break_btn.pack(side= tk.LEFT, padx = 5)
                else:
                    self.break_btn = tk.Button(self.frame, text = 'End Break', command = self.end_break)
                    self.break_btn.pack(side= tk.RIGHT, padx = 5)
            else:
                self.punch_in_btn = tk.Button(self.frame, text = 'Punch In', command = self.punch_in)
                self.punch_in_btn.pack(side= tk.TOP)

        self.buttons = tk.Frame(self.master, bg = 'purple')
        self.buttons.pack()

        self.RosterBtn = tk.Button(self.buttons, text = 'Roster', command = lambda: self.go_there(Roster))
        self.RosterBtn.grid(row = 1, column= 2, padx = 20, pady = 20, ipadx = 20, ipady = 20)

    
    def on_break(self) -> bool:
        ''' Checks if the user is on break'''
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Working Where EmployeeNum = ?', (user.ID,))
            data = cursor.fetchall()
            print (data)
            if data[0][4] == None:
                return False
            else:
                return True

    def punch_in(self) -> None:
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Working (EmployeeNum, Date, Start_Time) VALUES (?,?,?)', (user.ID, self.self.get_date(), self.get_time()))
            conn.commit()
        self.go_there(menu)

    def punch_out(self) -> None:
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE Working SET End_Time = ? WHERE EmployeeNum = ?', (self.get_time(), user.ID,))
            conn.commit()
        self.redraw()

    def start_break(self) -> None:
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE Working SET B_Start_Time = ? WHERE EmployeeNum = ?', (self.get_time(), user.ID,))
            conn.commit()
        self.go_there(manage)

    def end_break(self) -> None:
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE Working SET B_End_Time = ? WHERE EmployeeNum = ?', (self.get_time(), user.ID,))
            conn.commit()
        self.go_there(manage)

    def calculate_time(self) -> None:
        self.convert = lambda x: int(x[0:2]) * 60 + int(x[3:])
        self.difference = lambda x,y: self.convert(y) - self.convert(x)
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Working Where EmployeeNum = ?', (user.ID,))
        return round(self.difference(cursor.fetchall()[0][1], self.get_time()) / 60, 2)


class EmployeeInfo(Abstract):
    def _draw(self) -> None:
        self.back = tk.Button(self.master, text = 'Go Back', command = lambda: self.go_there(manage))

        self.back.pack(anchor = tk.NW, padx = 10, pady = 10)
        
        self.title = tk.Label(self.master, text = 'Employee Info', font=('Arial',40,'bold'))
        self.title.pack(side=tk.TOP, pady = 10)
        
        self.table = tk.Frame(self.master)
        self.table.pack(side = tk.TOP, pady = (0, 50))
        
        info = self.retrive()
        
        pinfo = []
        for x in info:
            DOB = '07/03/1998'
            dayB,monthB,yearB = int(DOB[0:2]),int(DOB[3:5]),int(DOB[6:])
            D = datetime.datetime.now()
            dayC,monthC,yearC = int(D.strftime("%d")),int(D.strftime("%m")),int(D.strftime("%Y"))
            if monthC < monthB:
                age = yearC - yearB
            else:
                if dayC >= dayB:
                    age = yearC - yearB + 1
                else:
                    age = yearC - yearB
            pinfo.append((x[0], x[1] + ' ' + x[2], x[3],x[4],str(age),x[5]))
        
        headings = ['ID','FName','LName', 'Phone', 'Email', 'Trained', 'DOB']

        for x in headings:
            self.entry = tk.Entry(self.table, width=12,font=('Arial',16))
            self.entry.grid(row=0, column = headings.index(x))
            self.entry.insert(tk.END, x)
        
        for i in range(len(info)):
            for j in range(len(info[0])):
                self.e = tk.Entry(self.table, width=12,font=('Arial',16))
                self.e.grid(row=i+1, column=j)
                self.e.insert(tk.END, info[i][j])

            self.button = tk.Button(self.master, text = 'View', command = lambda: self.view(info[i][1], info[i][2]))
            self.button.place(x=1500,y= 100 + (j * 20))

        self.add_employee_btn = tk.Button(self.master, text = 'Add Employee', command = self.create_top_add_employee)
        self.add_employee_btn.pack(side = tk.TOP)
        
    def retrive(self):
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT EmployeeNum, FName, LName, Phone, Email, trained, DOB FROM Employee')
            return cursor.fetchall()

    def view(self,fname,lname):
        print(fname + ' ' + lname)
    
    def create_top_add_employee(self) -> None:
        ''' Creates toplevel instance for adding an employee'''
        top = tk.Toplevel(self.master)
        
        self.f_name_label = tk.Label(top, text = "First Name")
        self.f_name_label.pack(side = tk.LEFT)

        self.f_name_entry = tk.Entry(top)
        self.f_name_entry.pack(side = tk.LEFT)

        self.l_name_label = tk.Label(top, text = 'Last Name')
        self.l_name_label.pack(side = tk.LEFT)

        self.l_name_entry = tk.Entry(top)
        self.l_name_entry.pack(side = tk.LEFT)

        self.phone_label = tk.Label(top, text = 'Phone')
        self.phone_label.pack(side = tk.LEFT)

        self.phone_entry = tk.Entry(top)
        self.phone_entry.pack(side = tk.LEFT)

        self.email_label = tk.Label(top, text = "Email")
        self.email_label.pack(side = tk.LEFT)

        self.email_entry = tk.Entry(top)
        self.email_entry.pack(side = tk.LEFT)

        self.address_label = tk.Label(top, text = 'Address')
        self.address_label.pack(side = tk.LEFT)

        self.address_entry = tk.Entry(top)
        self.address_entry.pack(side = tk.LEFT)

        self.DOB_label = tk.Label(top, text = 'DOB')
        self.DOB_label.pack(side = tk.LEFT)

        self.DOB_entry = tk.Entry(top)
        self.DOB_entry.pack(side = tk.LEFT)

        self.role_label = tk.Label(top, text = 'Role')
        self.role_label.pack(side = tk.LEFT)

        self.role_entry = tk.Entry(top)
        self.role_entry.pack(side = tk.LEFT)
        
        tk.Button(top, text = 'Sumbit', command = self.add_employee).pack(side = tk.BOTTOM, padx = 20, pady = 20)

    def add_employee(self) -> None:
        ''' Adds an employee to the database '''

        data = [self.f_name_entry.get(), self.l_name_entry.get(),self.phone_entry.get(), 
        self.email_entry.get(), self.address_entry.get(), self.role_entry.get(), self.DOB_entry.get(), self.get_date()  ]

        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Employee (FName, LName, Phone, Email, Address, Trained, DOB, DOH) VALUES (?,?,?,?,?,?,?,?)', (data))
            conn.commit()

class Roster(Abstract):
    def _draw(self) -> None:
        self.date = datetime.datetime.now()

        month_and_date = str(self.date.strftime('%B')) + ' ' + str(self.date.strftime('%Y'))

        self.back = tk.Button(self.master, text = 'Go Back', command = lambda: self.go_there(manage))
        self.back.pack(anchor = tk.NW, padx = 10, pady = 10)

        self.title = tk.Label(self.master, bg = 'light green', text = 'Roster', font = ('Calibri',45))
        self.title.pack(side = tk.TOP)

        self.month_year = tk.Label(self.master, text = month_and_date, bg = 'light green')
        self.month_year.pack(side = tk.TOP)

        self.days = tk.Frame(self.master, bg = 'light green')
        self.days.pack(side = tk.TOP)

        self.left_arrow = tk.Button(self.days, text = '<-', command = lambda : self.change_week(-1))
        self.left_arrow.grid(row = 2, column = 0)

        for x in range(0, len(DAYS)):
            tk.Label(self.days, text = DAYS[x]).grid(row = 1, column = x + 1)

        #self.day1var = tk.StringVar()
        #self.day1var.set(self.date_find(0))
        #self.Day1 = tk.Button(self.days, textvariable = self.day1var, width = 15, command = lambda: self.changeDay(0))
        #self.Day1.grid(row = 2, column = 1)

        self.Day1 = tk.Button(self.days, text = self.date_find(0), width = 15, command = lambda: self.change_day(0))
        self.Day1.grid(row = 2, column = 1)
        
        self.Day2 = tk.Button(self.days,text = self.date_find(1), width = 15, command = lambda: self.change_day(1))
        self.Day2.grid(row = 2, column = 2)
        
        self.Day3 = tk.Button(self.days,text = self.date_find(2), width = 15, command = lambda: self.change_day(2))
        self.Day3.grid(row = 2, column = 3)
        
        self.Day4 = tk.Button(self.days,text = self.date_find(3), width = 15, command = lambda: self.change_day(3))
        self.Day4.grid(row = 2, column = 4)
        
        self.Day5 = tk.Button(self.days,text = self.date_find(4), width = 15, command = lambda: self.change_day(4))
        self.Day5.grid(row = 2, column = 5)
        
        self.Day6 = tk.Button(self.days,text = self.date_find(5), width = 15, command = lambda: self.change_day(5))
        self.Day6.grid(row = 2, column = 6)
        
        self.Day7 = tk.Button(self.days,text = self.date_find(6), width = 15, command = lambda: self.change_day(6))
        self.Day7.grid(row = 2, column = 7)

        self.right_arrow = tk.Button(self.days, text = '->', command = lambda: self.change_week(1))
        self.right_arrow.grid(row = 2, column = 8)
        
        self.table = tk.Frame(self.master)
        self.table.pack(anchor = tk.CENTER)

        self.current_day = self.get_date()
        self.retrieve_data(self.get_date())       
            
        self.Name = tk.Entry(self.table, width=12,font=('Arial',16))
        self.Name.grid(row=0, column=0)
        self.Name.insert(tk.END, 'Name')
        
        self.Role = tk.Entry(self.table, width=12,font=('Arial',16))
        self.Role.grid(row=0, column=1)
        self.Role.insert(tk.END, 'Role')
        
        self.StartTime = tk.Entry(self.table, width=12,font=('Arial',16))
        self.StartTime.grid(row=0, column=2)
        self.StartTime.insert(tk.END, 'Start Time')
        
        self.EndTime = tk.Entry(self.table, width=12,font=('Arial',16))
        self.EndTime.grid(row=0, column=3)
        self.EndTime.insert(tk.END, 'End Time')

        self.Date = tk.Entry(self.table, width=12,font=('Arial',16))
        self.Date.grid(row=0, column=4)
        self.Date.insert(tk.END, 'Date')
        
        
        for i in range(len(self.info)):
            print (self.info)
            for j in range(len(self.info[0])):
                self.e = tk.Entry(self.table, width=12,font=('Arial',16))
                self.e.grid(row=i+1, column=j)
                self.e.insert(tk.END, self.info[i][j])
        
        self.add = tk.Frame(self.master)
        self.add.pack()

        self.ID = tk.Entry(self.add)
        self.ID.pack(pady=30)

        if user.f_name == 'Admin':
            self.add_shifts = tk.Button(self.add, text = 'Add Shift', command= self.create_top)
            self.add_shifts.pack()
    
    def create_top(self) -> None:
        top = tk.Toplevel(self.master)

        self.id_label = tk.Label(top, text = "ID")
        self.id_label.pack(side = tk.LEFT)

        self.id_entry = tk.Entry(top)
        self.id_entry.pack(side = tk.LEFT)

        self.start_time_label = tk.Label(top, text = "Start Time")
        self.start_time_label.pack(side = tk.LEFT)

        self.start_time_entry = tk.Entry(top)
        self.start_time_entry.pack(side = tk.LEFT)

        self.end_time_label = tk.Label(top, text = "End Time")
        self.end_time_label.pack(side = tk.LEFT)

        self.end_time_entry = tk.Entry(top)
        self.end_time_entry.pack(side = tk.LEFT)

        self.role_label = tk.Label(top, text = "Role")
        self.role_label.pack(side = tk.LEFT)

        self.role_entry = tk.Entry(top)
        self.role_entry.pack(side = tk.LEFT)

        tk.Button(top, text = 'Sumbit', command = self.add_shift).pack(side = tk.LEFT, padx = 20, pady = 20)

    def add_shift(self) -> None:
        ''' Add a shift to the roster database'''

        data = [self.id_entry.get(),self.role_entry.get(),self.start_time_entry.get(),self.end_time_entry.get(), self.current_day]
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Roster (EmployeeNum, role, startTime, endTime, Date) VALUES (?,?,?,?,?)' , (data))
            conn.commit()
        
        self.clear(self.master)
        self._draw()

    def change_day(self,value: int) -> None:
        day = DATE + datetime.timedelta(days = value)
        self.retrieve_data(day)
        self.current_day = day
        self.clear(self.master)
        self._draw()

    
    def change_week(self, value : int ) -> None:
        self.date += datetime.timedelta(days = 7)
        self.Day1.config(text = self.date_find(0))
        self.Day2.config(text = self.date_find(1))
        self.Day3.config(text = self.date_find(2))
        self.Day4.config(text = self.date_find(3))
        self.Day5.config(text = self.date_find(4))
        self.Day6.config(text = self.date_find(5))
        self.Day7.config(text = self.date_find(6))

    def date_find(self, future: int) -> None:
        return (self.date + datetime.timedelta(days = future)).strftime('%d')

    def retrieve_data(self, day: str):
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Roster WHERE date = ?', (day,))
            self.raw_info = cursor.fetchall()    
            self.info = []
            
            for x in range(0, len(self.raw_info)):
                cursor.execute('SELECT FName, LName FROM Employee WHERE EmployeeNum = ?', (self.raw_info[x][0],))
                name = cursor.fetchall()
                full_name = str(name[0][0]) + ' ' + str(name[0][1])
                temp = [full_name]
                temp.extend(self.raw_info[x][1:])
                self.info.append(temp)
                
            
class Stastics(Abstract):
    def __init__(self,master) -> None:
        self.type = 'Days'
        self.x,self.y = self.generate_data('Total Revenue', 7)
        super().__init__(master)

    def _draw(self) -> None:
        tk.Button(self.master, text = 'Back', command = lambda: self.go_there(manage)).pack(anchor = tk.NW)
        
        tk.Label(self.master, text = 'Statistics', font = ('Calibri',24)).pack(side = tk.TOP)


        fig = Figure(figsize = (9, 9),
				dpi = 80)

        plot = fig.add_subplot(111)
        plot.plot(self.x, self.y, '-o')
        plot.set_xlabel('Revenue ($)')
        plot.set_xlabel('Date (d/m/y)')

        for i, j in zip(self.x,self.y):
            plot.text(i, j, str(j), fontsize = 12)


        canvas = FigureCanvasTkAgg(fig,
                                master = self.master)
        canvas.draw()
        canvas.get_tk_widget().pack(side = tk.LEFT, padx = 50, pady = 50)

        self.options_frame = tk.Frame(self.master)
        self.options_frame.pack(side = tk.LEFT)
        self.options_frame.config(highlightbackground= 'Black', highlightthickness=5)

        self.drop_down_variable = tk.StringVar(self.master)
        self.drop_down_variable.set(OPTIONS[0])

        self.type_drop = tk.OptionMenu(self.options_frame, self.drop_down_variable, *OPTIONS)
        self.type_drop.pack(side = tk.TOP, padx = 30, pady = 30)

        self.times_frame = tk.Frame(self.options_frame)
        self.times_frame.pack()

        self.days_btn = tk.Button(self.times_frame, text = 'Days', command = lambda: self.change_type('Days'))
        self.days_btn.pack(side = tk.LEFT, padx = 10, pady = 10)

        self.weeks_btn = tk.Button(self.times_frame, text = 'Weeks', command = lambda: self.change_type('Weeks'))
        self.weeks_btn.pack(side = tk.LEFT, padx = 10, pady = 10)

        self.months_btn = tk.Button(self.times_frame, text = 'Months', command = lambda: self.change_type('Months'))
        self.months_btn.pack(side = tk.LEFT, padx = 10, pady = 10)

        self.time_label = tk.Label(self.options_frame, text = 'Time')
        self.time_label.pack(side = tk.LEFT)

        self.time_entry = tk.Entry(self.options_frame)
        self.time_entry.pack(side = tk.LEFT)

        self.sumbit_btn = tk.Button(self.options_frame, text = 'Sumbit', command = self.sumbit)
        self.sumbit_btn.pack(side = tk.TOP, padx = 30, pady = 30)

        self.time_error_label = tk.Label(self.options_frame, text = '')
        self.time_error_label.pack()
    
    def change_type(self, type: str) -> None:
        ''' Change type of display in days, weeks, months'''
        self.type = type
        if type == 'Days':
            self.days_btn.config(bg = 'Black')
            self.weeks_btn.config(bg = 'White')
            self.months_btn.config(bg = 'White')
        elif type == 'Weeks':
            self.days_btn.config(bg = 'White')
            self.weeks_btn.config(bg = 'Black')
            self.months_btn.config(bg = 'White')
        else:
            self.days_btn.config(bg = 'White')
            self.weeks_btn.config(bg = 'White')
            self.months_btn.config(bg = 'Black')

    def sumbit(self) -> None:
        ''' Generates the new and data and redraws screen'''

        try:
            x,y = self.generate_data(self.drop_down_variable.get(), int(self.time_entry.get()))
            self.y = y
            self.x = x
            self.time_error_label.destroy()
        except ValueError:
            self.time_error_label.config(text = 'Enter a number please')
        except AttributeError:
            pass

        self.clear(self.master)
        self._draw()


    def generate_data(self, type: str, length: str) -> list:
        ''' Generate data to be plotted on to the figure 
        
        Parameters:
            type: type of data to be generated
            length: in days of how many to show

        '''
        dates = self.generate_x_data(length)
        dates.append(self.get_date())

        with sql.connect(DATABASE) as conn:
            self.cursor = conn.cursor()
            if type == 'Profit/Loss':
                zipped = list(zip(
                    self.calculate_total_orders(dates, 'Total Revenue'),
                    self.calculate_total_orders(dates, 'Total Cost')))
                    
                revenue = ['$' + str(float(i[1:]) - float(j[1:])) for i,j in zipped]
            elif type == 'Amount of Orders':
                revenue = self.calculate_amount_orders(dates)
            elif type.endswith('Sold'):
                revenue = self.calculate_amount_of_item(dates, type)
            else:
                revenue = self.calculate_total_orders(dates, type)
        return dates, revenue

    def generate_x_data(self, length: str) -> list:
        if self.type == 'Days':
            return self.generate_day_data(length, [])
        elif self.type == 'Weeks':
            return self.generate_week_data(length, [])
        
            
    def generate_day_data(self, length: str, dates: list) -> list:
        if not length:
            return dates
        
        dates.append(self.get_date(DATE - datetime.timedelta(days = length)))
        return self.generate_day_data(length - 1, dates)
    
    def generate_week_data(self, length: str, weeks: list) -> list:
        if not length:
            return weeks
        
        weeks.append(self.generate_day_data(7, []))
        return self.generate_week_data(length - 1, weeks)
    
    def setup_dictionary(self, dates: list[str]) -> dict:
        day_to_values = {}
        for date in dates:
            day_to_values[date] = 0
        return day_to_values

    def get_orders(self) -> list:
        self.cursor.execute(''' SELECT * FROM Orders''')
        return self.cursor.fetchall()

    def calculate_amount_orders(self, dates: list[str]) -> list:
        x = []
        day_to_orders = self.setup_dictionary(dates)

        orders = self.get_orders()
        for order in orders:
            if order[2] in dates:
                day_to_orders[order[2]] += 1
        
        for day in day_to_orders:
            x.append(day_to_orders[day])
        
        return x
 
    def calculate_total_orders(self, dates: list[str], type: str) -> list:
        ''' Calculate total order revenue 
        
        Parameters:
            dates: list of dates needed to be calculated
        '''
        x = []
        day_to_money = self.setup_dictionary(dates)
        orders = self.get_orders()

        for order in orders:
            if order[2] in dates:
                if type == 'Total Revenue':
                    total = (self.calculate_total_order(order[0], ['Food', 'Price']) + 
                    self.calculate_total_order(order[0], ['Drink', 'Price']))
                elif type == 'Food Revemue':
                    total = self.calculate_total_order(order[0], ['Food', 'Price'])
                elif type == 'Drink Revenue':
                    total = self.calculate_total_order(order[0], ['Drink', 'Price'])
                elif type == 'Total Cost':
                    total = (self.calculate_total_order(order[0], ['Food', 'Cost']) + 
                    self.calculate_total_order(order[0], ['Drink', 'Cost']))
                elif type == 'Food Cost':
                    total = self.calculate_total_order(order[0], ['Food', 'Cost'])
                elif type == 'Drink Cost':
                    total = self.calculate_total_order(order[0], ['Drink', 'Cost'])
                else:
                    raise NotImplementedError

                day_to_money[order[2]] += total
        
        for day in day_to_money:
            x.append(day_to_money[day])
        
        return x
    
    def calculate_amount_of_item(self, dates: list[str], type: str) -> list:
        print (type)
        x = []
        day_to_orders = self.setup_dictionary(dates)

        self.cursor.execute('SELECT foodID FROM Foods WHERE Name = ?', (type.split(' ')[0],))
        id = self.cursor.fetchall()[0]

        self.cursor.execute('''SELECT Orders.OrderID, Orders.Date, OrderFood.qty
        FROM Orders, OrderFood WHERE Orders.OrderID = OrderFood.OrderID AND OrderFood.FoodID = ?''', (id))
        
        orders = self.cursor.fetchall()
        for order in orders:
            if order[1] in dates:
                day_to_orders[order[1]] += order[2] 

        for day in day_to_orders:
            x.append(day_to_orders[day])
        
        return x

class RegisterScreen(Abstract):
    def __init__(self,master: tk.Tk) -> None:
        self.items = {}
        self.order_type = 'Takeout'
        self.high = '' # self.high keeps track of the highlighted items
        self.qty = 1
        super().__init__(master)

    def _draw(self) -> None:

        self.backBtn = tk.Button(self.master, text = 'Go Back', command = lambda: self.go_there(manage))
        self.backBtn.pack(anchor = tk.NW)
        
        self.left_frame = tk.Frame(self.master, bg = 'light green', highlightbackground="black", highlightthickness=2, width = 1, height = 1)
        self.left_frame.pack(side = tk.LEFT, fill=tk.BOTH, expand = tk.TRUE)

        self.server_name = tk.Label(self.left_frame, text = user.f_name, bg = 'light green')
        self.server_name.pack(anchor= tk.NE)

        self.items_frame = tk.Frame(self.left_frame, bg = 'light green')
        self.items_frame.pack(side = tk.TOP, fill = tk.BOTH, expand = tk.TRUE)

        self.output_order()

        self.pay_frame = tk.Frame(self.left_frame, bg = 'light green')
        self.pay_frame.pack(side = tk.BOTTOM, fill = tk.BOTH)
        self.pay_frame.config(highlightthickness= 2,highlightbackground="blue")

        self.total = 0

        self.total_label = tk.Label(self.pay_frame,bg = 'light green', text = 'Total: $' + str(self.total), font = ('Calibri', 20))
        self.total_label.pack(anchor= tk.NW)

        self.pay_btn = tk.Button(self.pay_frame, bg = 'blue', text = 'Pay', command = self.pay)
        self.pay_btn.pack(anchor = tk.SW, ipadx= 30, ipady= 30)

        for x in ['Takeaway','Eat In', 'Delivery']:
            tk.Button(
                self.pay_frame,
                text=x,
                bg = 'blue',
                command = lambda: self.set_type(x)
            ).pack(anchor = tk.NE, ipadx= 20, ipady = 10)

        self.right_frame = tk.Frame(self.master, bg = 'light green', highlightbackground="black", highlightthickness=2, width = 1, height = 1)
        self.right_frame.pack(side = tk.LEFT, fill=tk.BOTH, expand = tk.TRUE)

        self.food_btn = tk.Button(self.right_frame, text = 'Foods', command = lambda: self.output_items(self.get_foods()), bg = 'blue')
        self.food_btn.grid(row = 0,column= 0,  ipadx= 20, ipady = 20, padx= 10, pady = 10)

        self.drinks_btn = tk.Button(self.right_frame, text = 'Drinks', command = lambda: self.output_items(self.get_drinks()), bg = 'blue')
        self.drinks_btn.grid(row = 0, column= 1, ipadx= 20, ipady = 20, padx= 10, pady = 10)

        self.output_frame = tk.Frame(self.right_frame, bg = 'light green')
        self.output_frame.grid(row=1, column = 0)

    def set_order_type(self, type: str) -> None:
        ''' Sets type of order
        
        parameters:
            type: str which is the new type of order
        '''
        self.order_type = type

    def pay(self) -> None:
        ''''''
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Orders (Type,Date,Time,Time_Sent) VALUES (?,?,?,?)', (self.order_type, self.get_date(), self.get_time(), ''))
            conn.commit()
            cursor.execute('SELECT OrderID FROM Orders ORDER BY OrderID DESC LIMIT 1')

            OrderID = cursor.fetchall()[0][0]

            # for every item, check if its a food or drink and add to relevant database
            for x in self.items:
                foods = self.get_foods()
                drinks = self.get_drinks()
                if x in [food[1] for food in foods]:
                    value = 'Food'
                elif x in [drink[1] for drink in drinks]:
                    value = 'Drink'
                cursor.execute('INSERT INTO Order' + value + '(OrderID,' + value + 'ID, qty) VALUES (?,?,?)', (OrderID, self.items[x][0], self.items[x][1]))

            conn.commit()
        
        self.items = {}
        self.clear(self.master)
        self._draw()


    def get_foods(self) -> None:
        ''' Get all the foods '''
        self.display_type = 'Food'
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Foods')
            foods = cursor.fetchall()
            return foods

    def get_drinks(self) -> None:
        ''' Get all the drinks '''
        self.display_type = 'Drink'
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Drinks')
            drinks = cursor.fetchall()
            return drinks

    def output_items(self, items) -> None:
        ''' Output all possible items in top right for user to pick 
        
        Parameters:
            items: list of items to be displayed
        '''
        self.clear(self.output_frame)

        for item in items:
            if item[1] == self.high:
                tk.Button(self.output_frame, bg = 'blue', text = item[1], command = partial(self.click, item[1])).pack(side = tk.LEFT, ipadx= 20, ipady = 20, padx= 10, pady = 10)
            else:
                tk.Button(self.output_frame, text = item[1], command = partial(self.click, item[1])).pack(side = tk.LEFT, ipadx= 20, ipady = 20, padx= 10, pady = 10)

    def click(self, name: str) -> None:
        ''' Handles clicking of menu item buttons
        
        paramaters:
            name: str which is the name of the item
        '''
        if self.display_type == 'Drink':
            self.output_items(self.get_drinks())
        else:
            self.output_items(self.get_foods())

        if name == self.high:
            self.high = ''
        else:
            self.high = name

            self.add_frame = tk.Frame(self.right_frame)
            self.add_frame.grid(row = 3, column = 0, pady= (480,0))

            self.qty_frame = tk.Frame(self.add_frame)
            self.qty_frame.pack(anchor = tk.NW)

            self.qty_var = tk.StringVar(self.master)
            self.qty_var.set(1)
            self.qty_entry = tk.Entry(self.qty_frame, text = self.qty_var)
            self.qty_entry.pack(side=tk.LEFT)

            self.qty_up_btn = tk.Button(self.qty_frame, text = '↑', command = lambda: self.change_qty(1))
            self.qty_up_btn.pack(side = tk.TOP)

            self.qty_down_btn = tk.Button(self.qty_frame, text = '↓', command = lambda: self.change_qty(-1))
            self.qty_down_btn.pack(side = tk.TOP)

            self.add_item_btn = tk.Button(self.add_frame, text = 'Add', command = self.add_item)
            self.add_item_btn.pack(anchor = tk.SW)

            self.modify_frame = tk.Frame(self.add_frame)
            self.modify_frame.pack(anchor = tk.NE)

            self.draw_modifiy_frame()

    def draw_modifiy_frame(self) -> None:
        #self.items_frame = tk.Frame(self.right_frame)
        #self.items_frame.grid(row = 2, column = 0)

        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT foodID FROM Foods WHERE Name = ?', (self.high,))
            id = cursor.fetchall()[0][0] # will throw exception here
            cursor.execute('SELECT * FROM FoodBuilds WHERE FoodID = ?', (id,))
            items = cursor.fetchall()
            print(items)
        
            for x in range(0,len(items)):
                cursor.execute('SELECT Name FROM ProccessedItems WHERE Name = ?', (items[x][1],))
                name = cursor.fetchall()
                print (name)
                tk.Label(self.modify_frame, text=name).grid(row=x + 1, column=0)
                tk.Label(self.modify_frame, text = 'Remove').grid(row=x+1, column = 1)

    def modify(self) -> None:
        '''Modify selected item
        Parameters:
            None
        '''
    
    def change_qty(self, change: int) -> None:
        ''' changes qty of chosen item
        
        Parameters:
            change: int which is either 1 or -1
        '''
        self.qty_var.set(int(self.qty_var.get()) + change)
    
    def add_item(self) -> None:
        name = self.high
        try:
            self.items[name][1] += int(self.qty_var.get())
            self.items[name][3] = self.items[name][2] * self.items[name][1]
        except:
            with sql.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM Foods WHERE Name = ?', (name,))
                info = cursor.fetchall()
                if not len(info):
                    cursor.execute('SELECT * FROM Drinks WHERE Name = ?', (name,))
                    info = cursor.fetchall()
                self.items[name] = [info[0][0], int(self.qty_var.get()), info[0][2], info[0][2]]
                row_enter = 1 + len(self.items)

        self.total += self.items[name][2] * int(self.qty_var.get())
        self.total_label.config(text = 'Total: $' + str(self.total))
        self.output_order()
    
    def output_order(self):

        self.item_name = tk.Label(self.items_frame,bg = 'light green', text = 'Name', font = (('Calibri', 24)))
        self.item_name.grid(row=1,column=1, padx= 100)

        self.item_qty = tk.Label(self.items_frame, bg = 'light green', text = 'Qty', font = (('Calibri', 24)))
        self.item_qty.grid(row=1,column=2, padx = 30)

        self.item_each = tk.Label(self.items_frame, bg = 'light green', text = 'Each', font = (('Calibri', 24)))
        self.item_each.grid(row=1,column=3, padx = 30)

        self.item_total = tk.Label(self.items_frame, bg = 'light green', text = 'Total', font = (('Calibri', 24)))
        self.item_total.grid(row=1,column=4, padx = 30)

        row = 2
        for x in self.items:
            tk.Label(self.items_frame, bg = 'light green', text = x).grid(row= row, column= 1)
            tk.Label(self.items_frame, bg = 'light green', text = self.items[x][1]).grid(row = row, column = 2)
            tk.Label(self.items_frame, bg = 'light green', text = self.items[x][2]).grid(row = row, column = 3)
            tk.Label(self.items_frame, bg = 'light green', text = self.items[x][3]).grid(row = row, column = 4)
            row += 1
                    

class OrderScreen(Abstract):
    def _draw(self) -> None:
        self.TopFrame = tk.Frame(self.master)
        self.TopFrame.pack(side = tk.TOP)

        self.backBtn = tk.Button(self.TopFrame, text = 'Go Back', command = lambda: self.go_there(manage))
        self.backBtn.pack(side = tk.LEFT)

        self.Title = tk.Label(self.TopFrame, text = 'Orders', font = (('Calibri',45)))
        self.Title.pack()

        self.orders_frame = tk.Frame(self.master)
        self.orders_frame.pack(side=tk.TOP)

        current_orders = self.get_current_orders()
        for x in current_orders:
            self.order_frame = tk.Frame(self.orders_frame, highlightbackground="black", highlightthickness=2)
            self.order_frame.pack(side=tk.LEFT, expand = tk.TRUE, fill = tk.BOTH, ipadx= 100, ipady = 100)

            colour = self.get_order_colour(x[3])

            self.top_frame = tk.Frame(self.order_frame, background = colour, highlightbackground="black", highlightthickness=2)
            self.top_frame.pack(side=tk.TOP, fill = tk.BOTH)

            self.order_num_label = tk.Label(self.top_frame, text = x[0], bg = colour)
            self.order_num_label.pack(anchor= tk.NW)

            self.order_type_label = tk.Label(self.top_frame, text = x[1], bg = colour)
            self.order_type_label.pack(anchor= tk.N)

            self.order_time_label = tk.Label(self.top_frame, text = x[3], bg = colour)
            self.order_time_label.pack(anchor= tk.NE)

            self.order_send_btn = tk.Button(self.top_frame, text = 'Send Order', command= lambda: self.send_order(x[0]))
            self.order_send_btn.pack(anchor= tk.N)

            items = self.get_items(x[0])

            for x in items:
                output = str(x[2]) + ' x ' + self.get_item_name(x[1])
                tk.Label(self.order_frame, text = output).pack(side=tk.TOP)

        self.BottomFrame = tk.Frame(self.master)
        self.BottomFrame.pack(side= tk.BOTTOM, fill= tk.BOTH)

        self.pastOrdersBtn = tk.Button(self.BottomFrame, text = 'Orders in the past', command = self.past_orders)
        self.pastOrdersBtn.pack(side = tk.RIGHT)

    def send_order(self, orderID: str) -> None:
        ''' Clear order from screen and update in database
        
        Parameters:
            orderID: string of the ID of order
        '''
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE Orders SET Time_Sent = ? WHERE OrderID = ?', (self.get_time(), orderID,))
            conn.commit()

        self.clear(self.master)
        self._draw()
        
    def past_orders(self) -> None:
        pass

    def get_current_orders(self) -> list:
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Orders WHERE date = ? AND Time_Sent = '' ''', (self.get_date(),))
            return cursor.fetchall() 
    
    def get_order_colour(self, time: str) -> str:
        current_time = datetime.datetime.now()
        cur_hour, cur_min = int(current_time.strftime('%H')),int(current_time.strftime('%M'))
        ord_hour, ord_min = int(time[0:2]), int(time[3:])

        time_since_purchase = ((cur_hour * 60) + cur_min) - ((ord_hour * 60) + ord_min)
        if time_since_purchase < 20:
            colour = 'green'
        elif time_since_purchase < 40:
            colour = 'yellow'
        else:
            colour = 'red'
        return colour


    def get_items(self, id: int) -> list:
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM OrderFood WHERE OrderID = ?', (id,))
            food = cursor.fetchall()
            cursor.execute('SELECT * FROM OrderDrink WHERE OrderID = ?', (id,))
            drink = cursor.fetchall()
            return food + drink
    
    def get_item_name(self, id: int) -> list:
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT Name FROM Foods WHERE FoodID = ?', (id,))
            return cursor.fetchall()[0][0]

class ItemScreen(Abstract):
    def _draw(self) -> None:
        self.clear(self.master)

        self.buttons_frame = tk.Frame(self.master, bg = 'light green')
        self.buttons_frame.pack(side=tk.TOP)

        tk.Button(
            self.buttons_frame, 
            text = 'Raw Items', 
            command = lambda: self.reload_data('RawItems')).pack(
                side = tk.LEFT,
                padx = 100,
                pady = 25
            )
        
        tk.Button(
            self.buttons_frame, 
            text = 'Proccessed items', 
            command = lambda: self.reload_data('ProccessedItems')).pack(
                side = tk.LEFT,
                padx = 100,
                pady = 25
            )
        
        tk.Button(
            self.buttons_frame, 
            text = 'Foods', 
            command = lambda: self.reload_data('Foods')).pack(
                side = tk.LEFT,
                padx = 100,
                pady = 25
            )
        
        tk.Button(
            self.buttons_frame, 
            text = 'Drinks', 
            command = lambda: self.reload_data('Drinks')).pack(
                side = tk.LEFT,
                padx = 100,
                pady = 25
            )
    
            

        self.title_label = tk.Label(self.master, text = 'Raw Items', font = ('Calibri', 24))
        self.title_label.pack(side = tk.TOP, padx = 20, pady = 20)

        self.table = tk.Frame(self.master)
        self.table.pack(side = tk.TOP, pady = (0, 50))

        self.reload_data('RawItems')

        self.type = 'RawItems'

        # Add item button
        tk.Button(self.master, text = 'Add Item', command = self.add_item_top).pack()

        # Back Button
        tk.Button(
            self.master, 
            text = 'Back', 
            command = lambda: self.go_there(manage)).pack(
                side = tk.BOTTOM, 
                padx = 20,
                pady = 20
            )
    
    def add_item_top(self) -> None:
        'Sets up add item top level'
        self.top = tk.Toplevel(self.master)

        if self.type == 'Raw items':
            self.draw_top_raw()
        elif self.type == 'ProccessedItems' or self.type == 'Foods':
            self.draw_top_menu()
        elif self.type == 'Drink':
            self.draw_top_drinks()
        
        self.sumbit_btn = tk.Button(self.top, text = 'Sumbit', command = self.submit)
        self.sumbit_btn.pack()
    def draw_top_drinks():
        pass
    
    def draw_top_raw(self) -> None:
        self.name_label = tk.Label(self.top, text = "Name")
        self.name_label.pack(side = tk.LEFT)

        self.name_entry = tk.Entry(self.top)
        self.name_entry.pack(side = tk.LEFT)

        self.cost_label = tk.Label(self.top, text = 'Cost')
        self.cost_label.pack(side = tk.LEFT)

        self.cost_entry = tk.Entry(self.top)
        self.cost_entry.pack(side = tk.LEFT)

        self.desc_label = tk.Label(self.top, text = 'Description')
        self.desc_label.pack(side = tk.LEFT)

        self.desc_entry = tk.Entry(self.top)
        self.desc_entry.pack(side = tk.LEFT)
        
    
    def draw_top_menu(self) -> None:
        self.items = []

        self.details_frame = tk.Frame(self.top)
        self.details_frame.pack()

        self.subtitle = tk.Label(self.details_frame, text = 'Details')
        self.subtitle.pack()

        self.name_label = tk.Label(self.details_frame, text = "Name")
        self.name_label.pack(side = tk.LEFT)

        self.name_entry = tk.Entry(self.details_frame)
        self.name_entry.pack(side = tk.LEFT)

        self.desc_label = tk.Label(self.details_frame, text = 'Description')
        self.desc_label.pack(side = tk.LEFT)

        self.desc_entry = tk.Entry(self.details_frame)
        self.desc_entry.pack(side = tk.LEFT)

        self.build_frame = tk.Frame(self.top)
        self.build_frame.pack(side = tk.LEFT)

        self.items_label = tk.Label(self.build_frame, text = 'Items')
        self.items_label.pack(side = tk.TOP, pady = 10)

        self.required_items_entry = tk.Entry(self.build_frame)
        self.required_items_entry.pack()

        raw = self.get_raw_items()
        raw = [item[1] for item in raw]

        self.drop_down_variable = tk.StringVar(self.top)
        self.drop_down_variable.set(raw[0])

        self.required_items_drop = tk.OptionMenu(self.build_frame, self.drop_down_variable, *raw)
        self.required_items_drop.pack(side = tk.TOP, padx = 30, pady = 30)

        self.qty_label = tk.Label(self.build_frame, text = 'QTY')
        self.qty_label.pack()

        self.qty_entry = tk.Entry(self.build_frame)
        self.qty_entry.pack()

        self.add_item_btn = tk.Button(self.build_frame, text = 'Add', command = self.add_item)
        self.add_item_btn.pack(pady = 10)

        self.cost_frame = tk.Frame(self.top)
        self.cost_frame.pack(side = tk.LEFT)

        self.cost_text = tk.Label(self.cost_frame, text = 'Cost')
        self.cost_text.pack()

        self.cost_entry = tk.Entry(self.cost_frame)
        self.cost_entry.pack()

        self.auto_calculate_btn = tk.Button(self.cost_frame, text = 'Auto Calculate Cost', command = self.calculate)
        self.auto_calculate_btn.pack(pady = 20)
    
    def calculate(self) -> None:
        cost = 0
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            database = 'ProccessedItems'
            if self.type == 'ProccessedItems':
                database = 'RawItems'

            for item in self.items:
                qty, name = item.split(' x ')
                cursor.execute('SELECT Cost FROM ' + database + ' WHERE Name = ?', (name,))
                cost += cursor.fetchall()[0][0] * int(qty)

        self.cost_entry.delete(0, tk.END)
        self.cost_entry.insert(0, cost)

    def add_item(self) -> None:
        ''' Add item to entry widget'''
        item = self.drop_down_variable.get() 
        qty = self.qty_entry.get()
        self.items.append(qty + ' x ' + item)
        self.required_items_entry.insert(tk.END, self.items[-1] + '\n')    

    def get_raw_items(self) -> None:
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM RawItems')
            return cursor.fetchall()

    def draw_top_menu(self) -> None:
        self.name_label = tk.Label(self.top, text = "Name")
        self.name_label.pack(side = tk.LEFT)

        self.name_entry = tk.Entry(self.top)
        self.name_entry.pack(side = tk.LEFT)

        self.cost_label = tk.Label(self.top, text = 'Cost')
        self.cost_label.pack(side = tk.LEFT)

        self.cost_entry = tk.Entry(self.top)
        self.cost_entry.pack(side = tk.LEFT)

        self.desc_label = tk.Label(self.top, text = 'Description')
        self.desc_label.pack(side = tk.LEFT)

        self.desc_entry = tk.Entry(self.top)
        self.desc_entry.pack(side = tk.LEFT)
    
    def submit(self) -> None:
        'Adds item to database'
        if self.type == 'Raw items':
            data = [self.name_entry.get(), self.cost_entry.get(), self.desc_entry.get()]
            with sql.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO RawItems (Name, Cost, Description) VALUES (?,?,?)', (data))
                conn.commit()
        if self.type == 'ProccessedItems':
            data = [self.name_entry.get(), self.cost_entry.get(), self.desc_entry.get()]
            with sql.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO' + self.type + ' (Name, Cost, Description) VALUES (?,?,?)', (data))
                
                cursor.execute('SELECT ID FROM ' + self.type)
                p_id = cursor.fetchall()[-1][0]
                print (self.required_items_entry.get().split('\n'))
                # For every item which needs to be added to database in the required item entry
                item = 'ProccessedItems'
                execute = 'INSERT INTO FoodBuilds (FoodID, ProccessedID, qty) VALUES (?,?,?) '
                if self.type == 'ProccessedItems':
                    item = 'RawItems'
                    execute = 'INSERT INTO ProccessedBuilds (ProccessedItemID, RawItemID, qty) VALUES (?,?,?) '

                for item in self.required_items_entry.get().split('\n'):
                    temp = item.split('x')
                    cursor.execute('SELECT ID FROM' + item + 'WHERE Name = ?', (temp[1][1:],))
                    r_id = cursor.fetchall()[0][0]
                    cursor.execute(execute, (p_id,r_id, temp[0][:-1]))
                    conn.commit()

 
        self.top.destroy()
            
    def reload_data(self, type: str) -> None:
        self.type = type

        self.title_label.config(text = type)

        self.clear(self.table)

        if type == 'Foods' or type == 'Drinks':
            headings = ['ID','Name','Price', 'Cost', 'Description']
        else:
            headings = ['ID','Name', 'Cost', 'Description']

        # Add headings
        for x in headings:
            self.entry = tk.Entry(self.table, width=12,font=('Arial',16))
            self.entry.grid(row=0, column = headings.index(x))
            self.entry.insert(tk.END, x)
        
        info = self.retrieve_data(type)

        for i in range(len(info)):
            for j in range(len(info[0])):
                self.e = tk.Entry(self.table, width=12,font=('Arial',16))
                self.e.grid(row=i+1, column=j)
                if info[i][j] == None:
                    self.e.insert(tk.END, '')
                else:
                    self.e.insert(tk.END, info[i][j])

    def retrieve_data(self, type: str) -> None:
        #table = TYPE_TO_DATABASE[type]
        table = type
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM ' + table)
            return cursor.fetchall()

class RosteringSystem(Abstract):
    def __init__(self, master: tk.Tk) -> None:
        self.expanded_weeks = False
        self.expanded_week = False
        self.week_to_expand = ''
        super().__init__(master)

    def _draw(self) -> None:
        self.sidebar = tk.Frame(self.master)
        self.sidebar.pack(anchor =tk.NW)
        self.sidebar.config(highlightcolor= 'Grey', highlightthickness= 1)

        self.weeks_btn = tk.Button(self.sidebar, text = 'Weeks', command = self.pack_unpack_weeks)
        self.weeks_btn.pack()

        self.weeks_frame = tk.Frame(self.sidebar)
        self.weeks_frame.pack()

        self.roster_frame = tk.Frame(self.master)
        self.roster_frame.pack(anchor = tk.N)

    def generate_weeks(self,count: int, weeks: list) -> list:
        ''' Recursive function which generates the weeks needed to be layed out

        count: amount of weeks which should be generated
        weeks: list of weeks 
        
        '''
        if len(weeks) == count:
            return weeks

        first = self.get_date(DATE + datetime.timedelta(days = len(weeks) * 7))
        second = self.get_date(DATE + datetime.timedelta(days = (len(weeks) + 1) * 7 - 1))
        weeks.append(first + ' - ' + second)
        return self.generate_weeks(count, weeks)
    
    def pack_unpack_weeks(self) -> None:
        self.clear(self.weeks_frame)

        if self.expanded_weeks == False:
            weeks = self.generate_weeks(10, [])

            references = []
            '''
            for week in weeks:
                references += [week]
                tk.Button(
                    self.weeks_frame, 
                    text = week, 
                    command = lambda: self.load_week(references[-1])).pack(
                        side = tk.TOP
                    )
            '''
            for index in range(len(weeks)):
                references += [weeks[index]]
                tk.Button(
                    self.weeks_frame, 
                    text = weeks[index], 
                    command = lambda: self.load_week(references[index])).pack(
                        side = tk.TOP
                    )

        # switches boolean values
        self.expanded_weeks = not self.expanded_weeks
    
    def load_week(self, week: str) -> None:
        print (week)
        headings = ['Employee']
        headings += self.generate_days(datetime.datetime.strptime(week.split(' ')[0], '%d/%m/%Y'), [])

        for x in headings:
            self.entry = tk.Entry(self.roster_frame, width=12,font=('Arial',16))
            self.entry.grid(row=0, column = headings.index(x))
            self.entry.insert(tk.END, x)

        shifts = self.get_shifts(headings[1:])
        
        for i in range(len(shifts)):
            for j in range(len(shifts[0])):
                self.e = tk.Entry(self.roster_frame, width=12,font=('Arial',16))
                self.e.grid(row=i+1, column=j)
                self.e.insert(tk.END, shifts[i][j])

    def generate_days(self, day, days: list[str]) -> list[str]:
        ''' Recursive function which generates the days needed for heading\
            
        Parmaters:
            week: str showing the start and end of the week (12/11/2022 - 18/11/2022)    
            days: list of all days 
        '''

        if len(days) == 7:
            return days

        day += datetime.timedelta(days = 1)
        days.append(self.get_date(day))
        return self.generate_days(day, days)
    
    def get_shifts(self, days) -> dict[str:tuple[tuple[str,str,str]]]:
        print (days)
        shifts = []
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            #shifts = ([cursor.execute('SELECT * FROM Roster WHERE Date = ?', (day,)) for day in days])
            for day in days:
                cursor.execute('SELECT * FROM Roster WHERE Date = ?', (day,))
                shifts.append(cursor.fetchall())
        print (shifts)
        return shifts


class Daily(Abstract):
    def __init__(self, master: tk.Tk) -> None:
        self.x, self.y = self.generate_data()
        self.convert = lambda x: int(x[0:2]) * 60 + int(x[3:])
        self.difference = lambda x,y: self.convert(y) - self.convert(x)
        super().__init__(master)
    def _draw(self) -> None:
        self.title_frame = tk.Frame(self.master, bg = 'black')
        self.title_frame.pack(side = tk.TOP, expand = tk.TRUE, fill = tk.BOTH)

        self.back = tk.Button(self.title_frame, text = 'Go Back', command = lambda: self.go_there(manage))
        self.back.pack(anchor = tk.NW)

        self.title = tk.Label(self.title_frame, text = 'Daily Stats',fg = 'white', bg = 'black', font = ('Calibri', 20))
        self.title.pack(side = tk.TOP, padx = 20, pady = 20)


        fig = Figure(figsize = (9, 9),
				dpi = 80)

        plot = fig.add_subplot(111)
        plot.plot(self.y, self.x, '-o')
        plot.set_ylabel('Revenue ($)')
        plot.set_xlabel('Date (d/m/y)')

        for i, j in zip(self.x,self.y):
            plot.text(i, j, str(j), fontsize = 12)

        canvas = FigureCanvasTkAgg(fig,
                                master = self.master)
        canvas.draw()
        canvas.get_tk_widget().pack(side = tk.LEFT)

        self.averages_frame = tk.Frame(self.master, highlightbackground="black", highlightthickness=1)
        self.averages_frame.pack()

        total_time = self.get_order_time('Total')
        out_time = self.get_order_time('Takeout')
        in_time = self.get_order_time('In')
        delivery_time = self.get_order_time('Delivery')

        self.total_frame = tk.Frame(self.averages_frame, bg = self.get_colour(total_time), highlightbackground="grey", highlightthickness=1)
        self.total_frame.pack(side = tk.LEFT, padx = 10, pady = 10)

        self.total_title = tk.Label(self.total_frame, text = 'Average time to serve any order')
        self.total_title.pack(side = tk.TOP)

        self.total_time = tk.Label(self.total_frame, text = total_time)
        self.total_time.pack(side = tk.TOP, padx = 10, pady = 10)

        self.out_frame = tk.Frame(self.averages_frame, bg = self.get_colour(out_time), highlightbackground="grey", highlightthickness=1)
        self.out_frame.pack(side = tk.LEFT, padx = 10, pady = 10)

        self.out_title = tk.Label(self.out_frame, text = 'Average time to serve out order')
        self.out_title.pack(side = tk.TOP)

        self.out_time = tk.Label(self.out_frame, text = out_time)
        self.out_time.pack(side = tk.TOP, padx = 10, pady = 10)

        self.in_frame = tk.Frame(self.averages_frame, bg = self.get_colour(in_time), highlightbackground="grey", highlightthickness=1)
        self.in_frame.pack(side = tk.LEFT, padx = 10, pady = 10)

        self.in_title = tk.Label(self.in_frame, text = 'Average time to serve in order')
        self.in_title.pack(side = tk.TOP)

        self.in_time = tk.Label(self.in_frame, text = in_time)
        self.in_time.pack(side = tk.TOP, padx = 10, pady = 10)

        self.delivery_frame = tk.Frame(self.averages_frame, bg = self.get_colour(delivery_time), highlightbackground="grey", highlightthickness=1)
        self.delivery_frame.pack(side = tk.LEFT, padx = 10, pady = 10)

        self.delivery_title = tk.Label(self.delivery_frame, text = 'Average time to serve delivery order')
        self.delivery_title.pack(side = tk.TOP)

        self.delivery_time = tk.Label(self.delivery_frame, text = delivery_time)
        self.delivery_time.pack(side = tk.TOP, padx = 10, pady = 10)
    
    def get_colour(self, time: str) -> str:
        if time == '0':
            return 'Green'
        time = self.convert(time.split(' ')[0])
        if time < 300:
            return 'Green'
        elif time < 900:
            return 'Yellow'
        else:
            return 'Red'   

    def get_order_time(self,type: str) -> str:
        ''' Retreives the average time dependings on the type of order

        Parameter:
            Type: type of order which should be [takeout, delivery etc]
        
        '''
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            if type == 'Total':
                cursor.execute('SELECT * FROM Orders WHERE date = ?', (self.get_date(),))
            else:
                cursor.execute('SELECT * FROM Orders WHERE date = ? AND type = ?', (self.get_date(), type,))
            orders = cursor.fetchall()
            if len(orders) != 0:
                mean = 0
                for order in orders:
                    try:
                        mean += self.difference(order[3], order[4])
                    except:
                        pass
                return str(round(mean / len(orders), 2)) + ' Minutes '
            else:
                return '0'

    def generate_data(self) -> list:
        ''' Generates the data of the day '''
        self.y = []
        for x in range(1,25):
            if x < 10:
                self.y.append('0' + str(x))
            else:
                self.y.append(str(x))

        self.x = []
        hours_to_revenue = {}
        for hour in self.y:
            hours_to_revenue[hour] = 0

        orders = self.retreive_all_order_day()
        for order in orders:
            time = order[3].split(':')[0]
            revenue = self.calculate_total_order(order[0], ['Food', 'Price']) + self.calculate_total_order(order[0], ['Drink', 'Price'])
            hours_to_revenue[time] += revenue
        
        for hour in hours_to_revenue:
            self.x.append(hours_to_revenue[hour])
        
        self.y = [int(num) for num in self.y]
        return self.x, self.y
    def average_check(self) -> int:
        "Generates the average pay of each order"
        orders = self.retreive_all_order_day()
        return sum((self.calculate_total_order(order[0], ['Food', 'Price']) + self.calculate_total_order(order[0], ['Drink', 'Price'])) for order in orders)
        

    
class Checklist(Abstract):
    def _draw(self) -> None:
        pass




BUTTONS = {
    'Employee Info': EmployeeInfo, 
    'Roster': Roster, 
    'Roster Maker': RosteringSystem,
    'Stastics': Stastics, 
    'Register': RegisterScreen,
    'Orders': OrderScreen,
    'Items': ItemScreen,
    }
        
root = tk.Tk()
app = menu(root)
root.mainloop()