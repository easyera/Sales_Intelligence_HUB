from config.db import fetch_all,execute_query

def get_customers_sales():
        return fetch_all("SELECT * FROM customer_sales")
    
def get_branches():
    return fetch_all("SELECT * FROM branches")

def get_payment_splits():
    return fetch_all("SELECT * FROM payment_splits")

def get_all_sales_by_status():
    return fetch_all("SELECT * FROM customer_sales where status = 'Open'")
            
def get_total_grosssales_all_branch():
    query ="""
            SELECT COALESCE(SUM(gross_sales), 0) AS total_gross_sale
            FROM customer_sales
            """
    return fetch_all(query)

def get_total_received_amount():
    return fetch_all("SELECT COALESCE(SUM(received_amount), 0) AS total_received FROM customer_sales")

def get_total_pending_amount():
    return fetch_all("SELECT COALESCE(SUM(pending_amount), 0) AS total_pending FROM customer_sales")

def get_count_of_sales_by_branch():
    query = """
            SELECT b.branch_name, COUNT(cs.sale_id) AS total_sales FROM branches b LEFT
            JOIN customer_sales cs ON cs.branch_id = b.branch_id
            GROUP BY b.branch_name
            ORDER BY total_sales DESC
            """
    return fetch_all(query)

def get_customers_sales_with_branch_name():
    query = """
            SELECT cs.*, b.branch_name FROM customer_sales cs LEFT
            JOIN branches b ON cs.branch_id = b.branch_id
            """
    return fetch_all(query)

def get_customers_sales_with_total_payment():
    query = """
            SELECT cs.*, COUNT(p.payment_id) AS total_payment FROM customer_sales cs LEFT
            JOIN payment_splits p ON cs.sale_id = p.sale_id
            GROUP BY cs.sale_id
            """
    return fetch_all(query)

def get_customers_sales_by_branchwise():
    query = """
            SELECT b.branch_name, SUM(cs.gross_sales)AS total_gross_sale FROM branches b JOIN customer_sales
            cs ON cs.branch_id = b.branch_id GROUP BY b.branch_name
            """
    return fetch_all(query)

def get_customers_sales_with_admin_name():
    query = """
            SELECT cs.*, u.username FROM customer_sales cs LEFT
            JOIN users u ON cs.branch_id = u.branch_id 
            """
    return fetch_all(query)

def get_total_collection_by_payment_method():
    return fetch_all(f"""
        SELECT 
            payment_method,
            COUNT(*) AS count
        FROM payment_splits GROUP BY payment_method
    """)
def get_pending_amount_greater_than_5000():
    return fetch_all("SELECT * FROM customer_sales WHERE pending_amount > 5000")

def get_topthree_gross_sales():
    return fetch_all("SELECT * FROM customer_sales ORDER BY gross_sales DESC LIMIT 3")