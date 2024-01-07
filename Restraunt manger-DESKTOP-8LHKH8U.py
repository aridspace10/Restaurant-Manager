from msilib.schema import Class
import tkinter as tk
from tkinter.ttk import Label
from tkinter import messagebox
import datetime
import sqlite3 as sql
from functools import partial
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
    'Menu Items': 'Foods'
}

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
        self._draw()
    
    def clear(self) -> None:
        ''' Clear all tkinter widgets from screen '''
        
        for widgets in self.master.winfo_children():
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

class menu(Abstract):
    def __init__(self,master: tk.Tk):
        super().__init__(master)
        self.code = ''
    
    def _draw(self) -> None:
        self.codevar = tk.StringVar()
        self.CodeEntry = tk.Entry(self.master, width = 7, textvariable = self.codevar, font = ('Calibri',45))
        self.CodeEntry.pack(side = tk.TOP, pady = (150,0))

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
        self.code += num
        self.codevar.set(self.code)
    def clear(self) -> None:
        self.code = ''
        self.codevar.set(self.code)
    def enter(self) -> None:
        if self.code == '0000':
            user.ID = 0
            user.f_name = 'Admin'
            self.master.destroy()
            root = tk.Tk()
            app = manage(root)

class manage(Abstract):
    def _draw(self) -> None:    
        self.TitleLabel = tk.Label(self.master, text = 'Restaurant Manager',font = ('Calibri', 40))
        self.TitleLabel.pack(side = tk.TOP, pady = 20)

        self.buttons = tk.Frame(self.master)
        self.buttons.pack()

        self.EmployeeInfoBtn = tk.Button(self.buttons, text = 'Employee Info', command = lambda: self.go_there(EmployeeInfo))
        self.EmployeeInfoBtn.grid(row = 1, column= 1, padx = 20, pady = 20, ipadx = 20, ipady = 20)
        
        self.RosterBtn = tk.Button(self.buttons, text = 'Roster', command = lambda: self.go_there(Roster))
        self.RosterBtn.grid(row = 1, column= 2, padx = 20, pady = 20, ipadx = 20, ipady = 20)

        self.StasticsBtn = tk.Button(self.buttons, text = 'Stastics', command = lambda: self.go_there(Stastics))
        self.StasticsBtn.grid(row = 1, column= 3, padx = 20, pady = 20, ipadx = 20, ipady = 20)

        self.OrderScreenBtn = tk.Button(self.buttons, text = 'Orders Screen', command = lambda: self.go_there(OrderScreen))
        self.OrderScreenBtn.grid(row = 1, column= 4, padx = 20, pady = 20, ipadx = 20, ipady = 20)

        self.registerScreenBtn = tk.Button(self.buttons, text = 'Register Screen', command = lambda: self.go_there(RegisterScreen))
        self.registerScreenBtn.grid(row = 1, column= 5, padx = 20, pady = 20, ipadx = 20, ipady = 20)

        self.itemsScreenBtn = tk.Button(self.buttons, text = 'Items', command = lambda: self.go_there(ItemScreen))
        self.itemsScreenBtn.grid(row = 2, column= 1, padx = 20, pady = 20, ipadx = 20, ipady = 20)

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
            button = tk.Button(self.master, text = 'View', command = lambda: self.view(info[i][1], info[i][2]))
            button.place(x=1450,y= 100 + (j))
        
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
        self.email_entry.get(), self.address_entry.get(), self.role_entry.get(), self.DOB_entry.get(), get_date()  ]

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

        self.title = tk.Label(self.master, text = 'Roster', font = ('Calibri',45))
        self.title.pack(side = tk.TOP)

        self.month_year = tk.Label(self.master, text = month_and_date)
        self.month_year.pack(side = tk.TOP)

        self.days = tk.Frame(self.master)
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

        self.current_day = get_date()
        self.retrieve_data(get_date())       
            
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
        
        self.clear()
        self._draw()

    def change_day(self,value: int) -> None:
        day = DATE + datetime.timedelta(days = value)
        self.retrieve_data(day)
        self.current_day = day
        self.clear()
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
    def _draw(self) -> None:
        tk.Label(self.master, text = 'Statistics', font = ('Calibri',24)).pack(side = tk.TOP)

        data = self.generate_data('Total', 7)

        fig = Figure(figsize = (5, 5),
				dpi = 100)

        plot1 = fig.add_subplot(111)
        plot1.plot(data)
        canvas = FigureCanvasTkAgg(fig,
                                master = self.master)
        canvas.draw()
        canvas.get_tk_widget().pack(side = tk.LEFT, padx = 50, pady = 50)
    
    def generate_data(self, type: str, length: str) -> list:
        ''' Generate data to be plotted on to the figure 
        
        Parameters:
            type: type of data to be generated
            length: in days of how many to show

        '''
        self.past_date = get_date() + datetime.timedelta(days = length)
        with sql.connect(DATABASE) as conn:
            self.cursor = conn.cursor()
            if type == 'Total':
                return self.calculate_total_orders_revenue()
                
    
    def calculate_total_orders_revenue(self) -> int:
        ''' Calculate total order revenue 
        
        Parameters:
            length: in days of how many to calculate
        '''
        revenue = {}
        self.cursor.execute(''' SELECT * FROM Orders''')
        orders = self.cursor.fetchall()
        for order in orders:
            if self.past_date < order[2]:
                total = (self.calculate_total_food_order_revenue(order[2]) + 
                self.calculate_total_drink_order_revenue(order[2]))
                try:
                    revenue[order[2]] += total
                except:
                    revenue[order[2]] = total

        return revenue
    
    def calculate_total_food_order_revenue(self, orderID: str) -> int:
        revenue = 0
        self.cursor.execute('''SELECT * FROM OrderFood WHERE OrderID = ?''', (orderID,))
        items = self.cursor.fetchall()
        for item in items:
            self.cursor.execute(''' SELECT Price FROM Foods WHERE foodID = ?''', (item[1]))
            revenue += self.cursor.fetchall()[0][0]
        return revenue

    def calculate_total_drink_order_revenue(self, orderID: str) -> int:
        revenue = 0
        self.cursor.execute('''SELECT * FROM OrderDrink WHERE OrderID = ?''', (orderID,))
        items = self.cursor.fetchall()
        for item in items:
            self.cursor.execute(''' SELECT Price FROM Drinks WHERE drinkID = ?''', (item[1]))
            revenue += self.cursor.fetchall()[0][0]
        return revenue



class RegisterScreen(Abstract):
    def _draw(self) -> None:

        self.backBtn = tk.Button(self.master, text = 'Go Back', command = lambda: self.go_there(manage))
        self.backBtn.pack(anchor = tk.NW)
        
        self.left_frame = tk.Frame(self.master,highlightbackground="black", highlightthickness=2, width = 1, height = 1)
        self.left_frame.pack(side = tk.LEFT, fill=tk.BOTH, expand = tk.TRUE)

        self.server_name = tk.Label(self.left_frame, text = user.f_name)
        self.server_name.pack(anchor= tk.NE)

        self.items = {}
        self.type = 'Takeout'

        self.items_frame = tk.Frame(self.left_frame)
        self.items_frame.pack(side = tk.TOP, fill = tk.BOTH, expand = tk.TRUE)

        self.output_order()

        self.pay_frame = tk.Frame(self.left_frame)
        self.pay_frame.pack(side = tk.BOTTOM, fill = tk.BOTH)
        self.pay_frame.config(highlightthickness= 2,highlightbackground="blue")

        self.total = 0

        self.total_label = tk.Label(self.pay_frame, text = 'Total: $' + str(self.total), font = ('Calibri', 20))
        self.total_label.pack(anchor= tk.NW)

        self.pay_btn = tk.Button(self.pay_frame, text = 'Pay', bg = 'blue', command = self.pay)
        self.pay_btn.pack(anchor = tk.SW, ipadx= 30, ipady= 30)

        for x in ['Takeaway','Eat In', 'Delivery']:
            tk.Button(
                self.pay_frame,
                text=x,
                command = lambda: self.set_type(x)
            ).pack(anchor = tk.NE, ipadx= 20, ipady = 10)

        self.right_frame = tk.Frame(self.master, highlightbackground="black", highlightthickness=2, width = 1, height = 1)
        self.right_frame.pack(side = tk.LEFT, fill=tk.BOTH, expand = tk.TRUE)

        self.food_btn = tk.Button(self.right_frame, text = 'Foods', command = lambda: self.output_items(self.get_foods()), bg = 'blue')
        self.food_btn.grid(row = 0,column= 0,  ipadx= 20, ipady = 20, padx= 10, pady = 10)

        self.drinks_btn = tk.Button(self.right_frame, text = 'Drinks', command = lambda: self.output_items(self.get_drinks()), bg = 'blue')
        self.drinks_btn.grid(row = 0, column= 1, ipadx= 20, ipady = 20, padx= 10, pady = 10)

        self.output_frame = tk.Frame(self.right_frame)
        self.output_frame.grid(row=1, column = 0)

    def set_type(self, type: str) -> None:
        self.type = type

    def pay(self) -> None:
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Orders (Type,Date,Time,Status) VALUES (?,?,?,?)', (self.type, get_date(), get_time(), 'Waiting'))

            cursor.execute('SELECT OrderID FROM Orders ORDER BY OrderID DESC LIMIT 1')

            OrderID = cursor.fetchall()[0][0]
            for x in self.items:
                foods = self.get_foods()
                drinks = self.get_drinks()
                if x in [food[1] for food in foods]:
                    value = 'Food'
                elif x in [drink[1] for drink in drinks]:
                    value = 'Drink'
                cursor.execute('INSERT INTO Order' + value + '(OrderID,' + value + 'ID, qty) VALUES (?,?,?)', (OrderID, self.items[x][0], self.items[x][1]))

            conn.commit()


    def get_foods(self) -> None:
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Foods')
            foods = cursor.fetchall()
            return foods

    def get_drinks(self) -> None:
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Drinks')
            drinks = cursor.fetchall()
            return drinks

    def output_items(self, items) -> None:

        self.clear()

        for item in items:
            tk.Button(self.output_frame, text = item[1], command = partial(self.add_item, item[1])).pack(side = tk.LEFT, ipadx= 20, ipady = 20, padx= 10, pady = 10)

    def add_item(self, name: int) -> None:
        try:
            self.items[name][1] += 1
            self.items[name][3] = self.items[name][2] * self.items[name][1]
        except:
            with sql.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM Foods WHERE Name = ?', (name,))
                info = cursor.fetchall()
                if not len(info):
                    cursor.execute('SELECT * FROM Drinks WHERE Name = ?', (name,))
                    info = cursor.fetchall()
                self.items[name] = [info[0][0], 1, info[0][2], info[0][2]]
                row_enter = 1 + len(self.items)

        self.total += self.items[name][2]
        self.total_label.config(text = 'Total: $' + str(self.total))
        self.output_order()
    
    def output_order(self):
        self.clear()

        self.item_name = tk.Label(self.items_frame, text = 'Name', font = (('Calibri', 24)))
        self.item_name.grid(row=1,column=1, padx= 100)

        self.item_qty = tk.Label(self.items_frame, text = 'Qty', font = (('Calibri', 24)))
        self.item_qty.grid(row=1,column=2, padx = 30)

        self.item_each = tk.Label(self.items_frame, text = 'Each', font = (('Calibri', 24)))
        self.item_each.grid(row=1,column=3, padx = 30)

        self.item_total = tk.Label(self.items_frame, text = 'Total', font = (('Calibri', 24)))
        self.item_total.grid(row=1,column=4, padx = 30)

        row = 2
        for x in self.items:
            tk.Label(self.items_frame, text = x).grid(row= row, column= 1)
            tk.Label(self.items_frame, text = self.items[x][1]).grid(row = row, column = 2)
            tk.Label(self.items_frame, text = self.items[x][2]).grid(row = row, column = 3)
            tk.Label(self.items_frame, text = self.items[x][3]).grid(row = row, column = 4)
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
            cursor.execute('UPDATE Orders SET Status = ? WHERE OrderID = ?', ('Sent', orderID,))
            conn.commit()

        self.clear()
        self._draw()
        
    def past_orders(self) -> None:
        pass

    def get_current_orders(self) -> list:
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Orders WHERE date = ? AND Status = 'Waiting' ''', (get_date(),))
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
        self.load_data('Raw items')
    
    def load_data(self, type: str) -> None:
        self.clear()

        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.pack(side=tk.TOP)

        for x in ['Raw items', 'Proccessed items', 'Menu Items']:
            tk.Button(
                self.buttons_frame, 
                text = x, 
                command = lambda: self.load_data(x)).pack(
                    side = tk.LEFT,
                    padx = 150,
                    pady = 25
                )

        tk.Label(self.master, text = type, font = ('Calibri', 24)).pack(side = tk.TOP, padx = 20, pady = 20)

        self.table = tk.Frame(self.master)
        self.table.pack(side = tk.TOP, pady = (0, 50))

        if type == 'Menu Items':
            headings = ['ID','Name','Price', 'Cost', 'Description']
        else:
            headings = ['ID','Name', 'Cost', 'Description']

        for x in headings:
            self.entry = tk.Entry(self.table, width=12,font=('Arial',16))
            self.entry.grid(row=0, column = headings.index(x))
            self.entry.insert(tk.END, x)
        
        info = self.retrieve_data(type)

        for i in range(len(info)):
            for j in range(len(info[0])):
                self.e = tk.Entry(self.table, width=12,font=('Arial',16))
                self.e.grid(row=i+1, column=j)
                self.e.insert(tk.END, info[i][j])

    def retrieve_data(self, type: str) -> None:
        table = TYPE_TO_DATABASE[type]
        with sql.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM ' + table)
            return cursor.fetchall()

def get_date(date: datetime = datetime.datetime.now()) -> str:
        date = str(date)
        return (date[8:10] + "/" + date[5:7] + "/" + date[0:4])

def get_time(date: datetime = datetime.datetime.now()) -> str:
        return str(date)[11:16]
        
root = tk.Tk()
app = menu(root)
root.mainloop()