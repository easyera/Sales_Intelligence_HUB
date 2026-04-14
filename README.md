# Sales Intelligence Hub

A simple Streamlit application for Branch-Based Sales Management System.

## ⚙️ Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database Credentials

This project loads database settings from environment variables using `python-dotenv`.

Create or update the `.env` file in the project root with your MySQL settings:

```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=Sales_Management_System
# Optional: uncomment if your database uses a custom port
# DB_PORT=3306
```

> `config/db.py` reads `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, and optional `DB_PORT`.

### 3. Create Database & Tables

The database creation helper is in `config/Dbcreation.py`.

1. Ensure your `.env` file is configured.
2. If the database does not exist yet, create it manually in MySQL or use a MySQL client first.
3. Run the helper script:

```bash
python config/Dbcreation.py
```

The file contains definitions for creating the database, tables, and triggers. Uncomment the bottom function calls in `config/Dbcreation.py` as needed before running the script.

### 4. Run the App

```bash
streamlit run main.py
```

## Notes

- `config/db.py` will raise an error if `DB_USER`, `DB_PASSWORD`, or `DB_NAME` are missing.
- Keep your `.env` file private and do not commit it to source control.
