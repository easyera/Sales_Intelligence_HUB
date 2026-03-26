from config.db import fetch_one, fetch_all, execute_query

def get_branches():
    return fetch_all("SELECT branch_id, branch_name FROM branches")

def get_products():
    return fetch_all("SELECT DISTINCT product_name FROM customer_sales ORDER BY product_name")

def build_filters(role, branch_id, date_from, date_to, status, products):
    conditions = []
    params = []

    if role != "Super Admin":
        conditions.append("branch_id = %s")
        params.append(branch_id)
    elif branch_id is not None:
        conditions.append("branch_id = %s")
        params.append(branch_id)

    conditions.append("date BETWEEN %s AND %s")
    params.extend([date_from, date_to])

    if status != "All":
        conditions.append("status = %s")
        params.append(status)

    if products:
        placeholders = ", ".join(["%s"] * len(products))
        conditions.append(f"product_name IN ({placeholders})")
        params.extend(products)

    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    return where, params

def get_KPI_data(where, params):
    return fetch_one(f"""
        SELECT 
            COALESCE(SUM(gross_sales), 0)     AS total_sales,
            COALESCE(SUM(received_amount), 0)  AS total_received,
            COALESCE(SUM(pending_amount), 0)   AS total_pending,
            COUNT(sale_id)                     AS total_orders
        FROM customer_sales
        {where}
    """, params)

def get_sales_data(where, params):
    return fetch_all(f"SELECT * FROM customer_sales {where}", params)

def get_status_summary(where, params):
    return fetch_all(f"""
        SELECT 
            status,
            COUNT(*) as count,
            COALESCE(SUM(gross_sales), 0) as total_gross,
            COALESCE(SUM(received_amount), 0) as total_received,
            COALESCE(SUM(pending_amount), 0) as total_pending
        FROM customer_sales
        {where}
        GROUP BY status
    """, params)

def get_branch_summary(date_from, date_to, status, products):
    where, params = build_filters("Super Admin", None, date_from, date_to, status, products)
    return fetch_all(f"""
        SELECT 
            b.branch_name,
            COUNT(cs.sale_id) as total_orders,
            COALESCE(SUM(cs.gross_sales), 0) as total_sales,
            COALESCE(SUM(cs.received_amount), 0) as total_received,
            COALESCE(SUM(cs.pending_amount), 0) as total_pending
        FROM branches b
        LEFT JOIN customer_sales cs ON b.branch_id = cs.branch_id
        {where}
        GROUP BY b.branch_id, b.branch_name
        ORDER BY total_sales DESC
    """, params)

def get_payment_summary(where, params):
    return fetch_all(f"""
        SELECT 
            payment_method,
            COUNT(*) as count,
            COALESCE(SUM(amount_paid), 0) as total
        FROM payment_splits
        WHERE sale_id IN (
            SELECT sale_id FROM customer_sales
            {where}
        )
        GROUP BY payment_method
    """, params)

def get_products():
    return fetch_all("SELECT DISTINCT product_name FROM customer_sales ORDER BY product_name")

def insert_sale(branch_id, sale_date, gross_sales, mobile, name, product):
    execute_query("""
        INSERT INTO customer_sales 
            (branch_id, date, gross_sales, mobile_number, name, product_name, received_amount, status)
        VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (branch_id, sale_date, gross_sales, mobile, name, product, 0.00, 'Open'))

def get_open_sales(role, branch_id):
    if role == "Super Admin":
        return fetch_all("""
            SELECT sale_id, branch_id, date, CAST(pending_amount AS FLOAT) as pending_amount 
            FROM customer_sales 
            WHERE status = 'Open' AND pending_amount > 0
        """)
    else:
        return fetch_all("""
            SELECT sale_id, branch_id, date, CAST(pending_amount AS FLOAT) as pending_amount 
            FROM customer_sales 
            WHERE status = 'Open' AND pending_amount > 0 AND branch_id = %s
        """, (branch_id,))

def insert_payment(sale_id, payment_date, amount_paid, payment_method):
    execute_query("""
        INSERT INTO payment_splits (sale_id, payment_date, amount_paid, payment_method)
        VALUES (%s, %s, %s, %s)
    """, (sale_id, payment_date, amount_paid, payment_method))

