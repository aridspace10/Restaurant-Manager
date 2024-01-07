import sqlite3 as sql
import random
DATABASE = 'Manage.db'
ORDER_TYPES = ['In', 'Takeout', 'Delivery']
date = input('Populate what date: ')

with sql.connect(DATABASE) as conn:
    cursor = conn.cursor()

    for _ in range(random.randint(1,10)):
        hour = random.randint(1,24)
        if len(str(hour)) == 1:
            hour = '0' + str(hour)
        minute = random.randint(0,60)
        if len(str(minute)) == 1:
            minute = '0' + str(minute)

        minute_s = random.randint(2,30)
        if (int(minute) + minute_s) > 60:
            hour_s = str(int(hour) + 1)
            if len(str(hour_s)) == 1:
                hour_s = '0' + str(hour_s)
            minute_s = minute_s % 60
        else:
            hour_s = hour
            minute_s += int(minute)
            if len(str(minute_s)) == 1:
                minute_s = '0' + str(minute_s)

        cursor.execute('''INSERT INTO Orders (Type, Date, Time, Time_Sent, Status) 
        VALUES (?,?,?,?,?)''', (ORDER_TYPES[random.randint(0,2)], date, str(hour) + ':' + str(minute), str(hour_s) + ':' + str(minute_s), 'Sent'))
        conn.commit()

        cursor.execute('SELECT OrderID FROM Orders ORDER BY OrderID DESC LIMIT 1')
        id = cursor.fetchall()[0][0]

        for type in ['Drink', 'Food']:
            cursor.execute('SELECT * FROM ' + type + 's')
            items = len(cursor.fetchall())
            for _ in range(random.randint(1,10)):
                cursor.execute('INSERT INTO Order' + type + '(OrderID, ' + type + 'ID, qty) VALUES (?,?,?)', (id, random.randint(1, items), 1))
                conn.commit()
