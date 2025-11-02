import csv
import sqlite3

connection = sqlite3.connect('adva.db')
cursor = connection.cursor()

# query = "CREATE TABLE IF NOT EXISTS system_command (id INTEGER PRIMARY KEY, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO system_command VALUES (null,'powerpoint','C:\\Program Files\\Microsoft Office\\Office16\\POWERPNT.EXE')"
# cursor.execute(query)
# connection.commit()

# query = "INSERT INTO system_command VALUES (null,'word','C:\\Program Files\\Microsoft Office\\Office16\\WINWORD.EXE')"
# cursor.execute(query)
# connection.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command (id INTEGER PRIMARY KEY, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'github','www.github.com')"
# cursor.execute(query)
# connection.commit()

# query = "INSERT INTO web_command VALUES (null,'youtube','www.youtube.com')"
# cursor.execute(query)
# connection.commit()

# Create a table with the desired columns
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL, address VARCHAR(255) NULL)''')

# Inserting single contact
# query = "INSERT INTO contacts VALUES (null,'pawan', '1234567890','null')"
# cursor.execute(query)
# connection.commit()

# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 18]

# # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
# connection.commit()
# connection.close()


#### 5. Search Contacts from database
# query = 'amma'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])


# Adding personal info table
# query = "CREATE TABLE IF NOT EXISTS personal_info(name VARCHAR(100), mobile VARCHAR(40), email VARCHAR(200), city VARCHAR(300))"
# cursor.execute(query)

# Add Column in contacts table
# cursor.execute("ALTER TABLE contacts ADD COLUMN address VARCHAR(255)")

#------------------------------------------------


# For deleting all entries from the table
# import sqlite3
# connection = sqlite3.connect('adva.db')
# cursor = connection.cursor()

# cursor.execute("DELETE FROM system_command")
# cursor.execute("DELETE FROM web_command")
# connection.commit()
# connection.close()
