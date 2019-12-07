from flask import Flask, jsonify
from flask_mysqldb import MySQL


app=Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'student_flask'

mysql = MySQL(app)


@app.route('/insert/')
def add():
    cur = mysql.connection.cursor()
    cur.execute("insert into student_details(student_name,id,college,address) values('abc','3','jntu','kakinada')")
    mysql.connection.commit()
    return "Inserted successfully"


@app.route('/select/')
def select_query():
    cur = mysql.connection.cursor()
    query="select * from student_details where id = 2"
    cur.execute(query)
    data=cur.fetchall()
    return jsonify(data)


@app.route('/update/')
def updating():
    cur=mysql.connection.cursor()
    cur.execute("Update student_details set student_name='xyz' where id=3")
    mysql.connection.commit()
    return "Updated successfully"


@app.route('/delete/')
def deleting():
    cur=mysql.connection.cursor()
    cur.execute("delete from student_details where id=3")
    mysql.connection.commit()
    return "Deleted Successfully"


app.run()
