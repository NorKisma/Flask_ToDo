
from flask import Flask, render_template, request, redirect, url_for, flash, session
import hashlib  # Add this line

app = Flask(__name__)
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'sample'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        # Hash the incoming password and compare it with the stored hashed password
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        if user and user['password'] == hashed_password:
            session['user_id'] = user['id']
            session['role'] = user['role']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')










@app.route('/index')
def index():
   

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks ORDER BY deadline")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    # Directly process the task addition without role check
    description = request.form['description']
    deadline = request.form['deadline']
    priority = request.form['priority']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO tasks (description, deadline, created_date, priority) VALUES (%s, %s, %s, %s)"
    values = (description, deadline, datetime.now().date(), priority)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))


@app.route('/edit/<int:id>')
def edit_task(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (id,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit.html', task=task)

@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Access denied', 'danger')
        return redirect(url_for('login'))

    description = request.form['description']
    deadline = request.form['deadline']
    priority = request.form['priority']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE tasks SET description = %s, deadline = %s, priority = %s WHERE id = %s"
    values = (description, deadline, priority, id)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_task(id):
    if 'role' not in session or session['role'] != 'admin':
        flash('Access denied', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))
@app.route('/register', methods=['GET', 'POST'])  # Correct the method string
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))

        # Hash the password before storing it
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        conn = get_db_connection()  # Use the correct connection method
        mycursor = conn.cursor()

        try:
            mycursor.execute(
                "INSERT INTO users (ful_name, email, password, status) VALUES (%s, %s, %s, %s)",
                (full_name, email, hashed_password, 'active')
            )
            conn.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
            return redirect(url_for('register'))
        finally:
            mycursor.close()
            conn.close()  # Close the connection properly

    return render_template('register.html')

@app.route('/users')
def list_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('users.html', users=users)

@app.route('/delete_user/<int:id>', methods=['GET'])
def delete_user(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('list_users'))



@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        status = request.form['status']
        role = request.form['role']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('edit_user', id=id))

        # Hash the password before storing it
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        try:
            cursor.execute(
                "UPDATE users SET ful_name = %s, email = %s, password = %s, status = %s, role = %s WHERE id = %s",
                (full_name, email, hashed_password, status, role, id)
            )
            conn.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('users'))
        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
            return redirect(url_for('edit_user', id=id))
        finally:
            cursor.close()
            conn.close()

    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('edit_user.html', user=user)



if __name__ == '__main__':
    app.run(debug=True)
