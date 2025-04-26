# Expense Analyzer

A web application to help users manage, track, and analyze their expenses with AI support.
Built using **Flask**, **SQLite**, and **Python**.

## Project Structure
```
ai/
  └── expense_analyzer.py         # AI analysis logic
static/
  ├── graph.png                  # Generated graph image
  └── style.css                  # Application styling
templates/
  ├── base.html                  # Base template
  ├── edit.html                  # Edit expense page
  ├── graph.html                 # Graph visualization page
  ├── home.html                  # Homepage
  ├── login.html                 # User login page
  └── register.html              # User registration page
utils/
  └── file_handler.py             # Utility functions

app.py                           # Main Flask application
database.db                      # SQLite database
```

## Features
- User registration and login functionality
- Add, edit, and delete expenses
- AI-powered expense analysis
- Visualization of expenses using graphs
- Responsive and clean user interface

## Installation and Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/jeslipriya/Expense-Tracker.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Expense-Tracker
   ```
3. Install the required dependencies:
   ```bash
   pip install flask
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open your browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

## Future Enhancements
- Generate detailed monthly and yearly reports
- Enable data export to CSV files
- Improve mobile responsiveness
- Enhance AI analysis features

## License
This project is licensed under the MIT License.

---

> Developed with passion and precision.

