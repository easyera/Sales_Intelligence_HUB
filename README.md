# Sales_Intelligence_HUB
a simple streamlit application for Branch-Based Sales Management System.
## ⚙️ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Database Setup
Open `config/db.py` and update your MySQL credentials:
```python
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="Sales_Management_System"
    )
```

### 3. Create Database & Tables
Open `config/create_db.py`:

**Step 1** — Comment out the `database` field in `get_connection()` inside `db.py`:
```python
# database="Sales_Management_System"  ← comment this
```
Uncomment `create_database()` at the bottom of `create_db.py` and run:
```bash
python config/create_db.py
```

**Step 2** — Uncomment the `database` field back in `db.py`:
```python
database="Sales_Management_System"  ← uncomment this
```
Now uncomment all remaining functions in `create_db.py` and run again:
```bash
python config/create_db.py
```

This will create all tables and triggers. ✅

### 4. Run the App
```bash
streamlit run main.py
```
