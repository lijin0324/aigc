import sqlite3
conn = sqlite3.connect('instance/draw.db')
cursor=conn.cursor()
cursor.execute("select * from describe")
result=cursor.fetchall()
for row in result:
    print(row)
cursor.close()
conn.close()