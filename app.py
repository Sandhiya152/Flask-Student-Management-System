from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Create database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    department TEXT,
    year INTEGER,
    email TEXT
)
""")

conn.commit()
conn.close()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add', methods=['POST'])
def add_student():

    name = request.form['name']
    department = request.form['department']
    year = request.form['year']
    email = request.form['email']

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students(name,department,year,email) VALUES(?,?,?,?)",
        (name, department, year, email)
    )

    conn.commit()
    conn.close()

    return "<h2>Student Added Successfully!</h2><a href='/'>Go Back</a>"
@app.route('/students')
def view_students():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    conn.close()

    return render_template(
        'students.html',
        students=students
    )
@app.route('/delete/<int:id>')
def delete_student(id):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return '''
    <h2>Student Deleted Successfully!</h2>
    <a href="/students">View Students</a>
    '''
if __name__ == '__main__':
    app.run(debug=True)