import sqlite3

connection = sqlite3.connect('adva.db')
cursor = connection.cursor()

query = "CREATE TABLE IF NOT EXISTS system_command (id INTEGER PRIMARY KEY, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

query = "INSERT INTO system_command VALUES (null,'powerpoint','C:\\Program Files\\Microsoft Office\\Office16\\POWERPNT.EXE')"
cursor.execute(query)
connection.commit()

query = "INSERT INTO system_command VALUES (null,'word','C:\\Program Files\\Microsoft Office\\Office16\\WINWORD.EXE')"
cursor.execute(query)
connection.commit()

query = "CREATE TABLE IF NOT EXISTS web_command (id INTEGER PRIMARY KEY, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)

query = "INSERT INTO web_command VALUES (null,'github','www.github.com')"
cursor.execute(query)
connection.commit()




# For deleting all entries from the table
# import sqlite3
# connection = sqlite3.connect('adva.db')
# cursor = connection.cursor()

# cursor.execute("DELETE FROM system_command")
# cursor.execute("DELETE FROM web_command")
# connection.commit()
# connection.close()
