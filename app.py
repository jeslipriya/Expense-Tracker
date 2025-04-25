import os
import sqlite3
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, request, redirect, url_for, flash, session
from ai.expense_analyzer import expense_recommendations, total_expenses
from utils.file_handler import load_expenses_from_csv

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")  # Use environment variable for production

# Database setup
DATABASE = "database.db"

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        ''')
        conn.commit()

init_db()  # Initialize database

@app.route('/')
def home():
    if 'username' in session:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM expenses WHERE username = ?", (session['username'],))
            expenses = cursor.fetchall()
        return render_template('home.html', expenses=expenses)
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                flash("Registration successful! Please log in.", "success")
                return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists. Please choose a different username.", "error")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            if user:
                session['username'] = username
                flash("Login successful!", "success")
                return redirect(url_for('home'))
            else:
                flash("Invalid username or password.", "error")
    return render_template('login.html')

@app.route('/add_expense', methods=['POST'])
def add_expense():
    if 'username' in session:
        category = request.form['category']
        if category == 'Others':
            category = request.form['custom_category']
        amount = float(request.form['amount'])
        description = request.form['description']
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO expenses (username, category, amount, description) VALUES (?, ?, ?, ?)", 
                           (session['username'], category, amount, description))
            conn.commit()
        flash("Expense added successfully!", "success")
    return redirect(url_for('home'))

@app.route('/edit_expense/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    if 'username' in session:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM expenses WHERE id = ?", (id,))
            expense = cursor.fetchone()
        
        if request.method == 'POST':
            category = request.form['category']
            if category == 'Others':
                category = request.form['custom_category']
            amount = float(request.form['amount'])
            description = request.form['description']
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE expenses SET category = ?, amount = ?, description = ? WHERE id = ?", 
                               (category, amount, description, id))
                conn.commit()
            flash("Expense updated successfully!", "success")
            return redirect(url_for('home'))
        
        return render_template('edit.html', expense=expense)

@app.route('/delete_expense/<int:id>', methods=['GET'])
def delete_expense(id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))
        conn.commit()
    flash("Expense deleted successfully!", "success")
    return redirect(url_for('home'))

@app.route('/graph')
def graph():
    if 'username' in session:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE username = ? GROUP BY category", 
                           (session['username'],))
            data = cursor.fetchall()
        
        categories, amounts = zip(*data) if data else ([], [])
        plt.bar(categories, amounts, color='blue')
        plt.xlabel('Categories')
        plt.ylabel('Total Amount')
        plt.title('Expense Distribution')

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return render_template('graph.html', graph_url=graph_url)
    else:
        flash("You must be logged in to view the graph.", "error")
        return redirect(url_for('login'))

@app.route('/ai_advice', methods=['POST'])
def ai_advice():
    if 'username' in session:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category, amount FROM expenses WHERE username = ?", (session['username'],))
            expenses = cursor.fetchall()

        # Assuming you have expense_recommendations function to get the advice
        recommendations = expense_recommendations(expenses)

        return render_template('home.html', recommendations=recommendations)
    flash("You must be logged in to get advice.", "error")
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
