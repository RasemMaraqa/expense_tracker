# Expense Tracker

A small Flask web application for tracking personal expenses. Users can sign up, log in, add expenses, and remove their own expense entries. The application stores data in a local SQLite database.

## Features

- User registration and password-hashed login
- Session-protected dashboard
- Add expenses with a description and amount
- Delete your own expenses
- Admin-only user and expense views
- SQLite persistence via Flask-SQLAlchemy

## Tech stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML, CSS, and JavaScript

## Getting started

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Create a private secret key (one-time setup). Copy and run these lines in PowerShell:

   ```powershell
   $newSecret = python -c "import secrets; print(secrets.token_urlsafe(32))"
   [Environment]::SetEnvironmentVariable("SECRET_KEY", $newSecret, "User")
   $env:SECRET_KEY = $newSecret
   ```

   This creates a random private key that keeps your login session secure. It is saved for your Windows user account and is not added to Git. Keep it private—never paste it into the code, README, or a public post. If you open a new terminal later, close and reopen it before running the app.

4. Start the application:

   ```powershell
   python app.py
   ```

5. Open `http://127.0.0.1:5000/signup` in a browser to create an account. After signing in, you can use the built-in frontend dashboard to add, view, and delete your expenses.

The database is created automatically on first startup at `instance/site.db`.

## Routes

| Route | Methods | Purpose |
| --- | --- | --- |
| `/signup` | GET, POST | Create an account |
| `/login` | GET, POST | Sign in |
| `/logout` | POST | Sign out |
| `/user` | GET | View the signed-in user's dashboard |
| `/add_expense` | POST | Create an expense using JSON data |
| `/delete_expense/<expense_id>` | DELETE | Delete one of the signed-in user's expenses |
| `/view` | GET | Admin-only JSON list of users and their expenses |

## API example

While signed in, add an expense by sending JSON to `/add_expense`:

```json
{
  "description": "Groceries",
  "amount": 42.50
}
```

## Project structure

```text
app.py             Flask application setup and blueprint registration
routes/            HTTP routes
models/            User and expense database models
services/          Authentication and data-access helpers
decorators/        Login and admin access controls
templates/         HTML pages
extensions/        Flask-SQLAlchemy setup
instance/site.db   Local SQLite database
```

## Notes

- Flask debug mode is disabled by default.
- `SECRET_KEY` is required at startup and must be stored as an environment variable.
