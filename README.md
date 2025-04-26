# Expense Analyzer 

A web app that helps users manage and analyze their expenses smartly using AI.  
Built with **Flask**, **SQLite**.

## Project Structure 🏗️
```
ai/
  └── expense_analyzer.py (AI logic)
static/
  ├── graph.png (Generated graph)
  └── style.css (App styling)
templates/
  ├── base.html (Base layout)
  ├── edit.html (Edit expenses)
  ├── graph.html (Expense graph)
  ├── home.html (Homepage)
  ├── login.html (Login page)
  └── register.html (Register page)
utils/
  └── file_handler.py (Helper functions)

app.py (Main Flask app)
database.db (SQLite database)
```

## Features 🚀
- User Authentication (Login/Register)
- Add/Edit/Delete expenses
- AI-based Expense Analysis
- Visual graphs 📊
- Clean UI with CSS magic ✨

## How to Run 🖥️
1. Clone the repo  
2. Install dependencies:  
   ```bash
   pip install flask
   ```
3. Run the app:  
   ```bash
   python app.py
   ```
4. Open `http://127.0.0.1:5000/` in your browser!

## Future Improvements 🔥
- Add monthly/yearly reports
- Export data to CSV
- Make it mobile responsive 📱

---

