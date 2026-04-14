from db import execute_query

#create database
def create_database():
    query = "CREATE DATABASE IF NOT EXISTS Sales_Management_System"
    execute_query(query)

#create tables
def branches_Table():
    query = """
            CREATE TABLE branches(
            branch_id INT PRIMARY KEY AUTO_INCREMENT,
            branch_name VARCHAR(100),
            branch_admin_name VARCHAR(100)
            )
            """
    execute_query(query)

def customersSales_Table():
    query = """
            CREATE TABLE customer_sales(
            sale_id INT PRIMARY KEY AUTO_INCREMENT,
            branch_id INT,
            date DATE,
            name VARCHAR(100),
            mobile_number VARCHAR(15),
            product_name VARCHAR(30),
            gross_sales DECIMAL(12,2),
            received_amount DECIMAL(12,2),
            pending_amount DECIMAL(12,2) GENERATED ALWAYS AS (gross_sales - received_amount) STORED,
            status ENUM('Open','Close'),
            FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
            )
            """
    execute_query(query)

def user_Table():
    query = """
            CREATE TABLE users(
            user_id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(100),
            password VARCHAR(255),
            branch_id INT,
            role ENUM('Super Admin', 'Admin'),
            email VARCHAR(255) UNIQUE,
            FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
            )
            """
    execute_query(query)

def paymentSplit_Table():
    query = """ 
            CREATE TABLE payment_splits(
            payment_id INT PRIMARY KEY AUTO_INCREMENT,
            sale_id INT,
            payment_date DATE,
            amount_paid DECIMAL(12,2),
            payment_method VARCHAR(50),
            FOREIGN KEY (sale_id) REFERENCES customer_sales(sale_id)
            )
            """
    execute_query(query)

def create_trigger1():
    query = """ 
            CREATE TRIGGER AFTER_PAYMENT_INSERT
            AFTER INSERT
            ON payment_splits
            FOR EACH ROW
            BEGIN
                DECLARE Total_Paid DECIMAL(12,2);
                SELECT SUM(amount_paid) INTO Total_Paid FROM payment_splits WHERE sale_id = NEW.sale_id;
                UPDATE customer_sales SET received_amount = Total_Paid WHERE sale_id = NEW.sale_id;
            END
            """
    execute_query(query)

def create_trigger2():
    query = """ 
            CREATE TRIGGER close_sale_after_payment
            AFTER INSERT ON payment_splits
            FOR EACH ROW
            BEGIN
                UPDATE customer_sales 
                SET status = 'Close'
                WHERE sale_id = NEW.sale_id 
                AND pending_amount <= 0;
            END;
            """
    execute_query(query)


# create_database() # only uncomment this line if you want to create database first time
# then run the rest of the code to create tables and triggers
# branches_Table()
# customersSales_Table()
# user_Table()
# paymentSplit_Table()
# create_trigger1()
# create_trigger2()
