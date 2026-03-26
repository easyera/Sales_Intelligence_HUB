import re

def validate_sale(name, mobile, product, gross_sales, sale_date, branch_id):
    errors = []

    if not name or not name.strip():
        errors.append("Customer name is required")
    elif len(name.strip()) < 2:
        errors.append("Customer name must be at least 2 characters")
    elif len(name.strip()) > 100:
        errors.append("Customer name must be under 100 characters")

    if not mobile or not mobile.strip():
        errors.append("Mobile number is required")
    elif not re.fullmatch(r'\d{10}', mobile.strip()):
        errors.append("Enter a valid 10 digit mobile number")

    if not product or not product.strip():
        errors.append("Product name is required")
    elif len(product.strip()) > 30:
        errors.append("Product name must be under 30 characters")

    if gross_sales is None or gross_sales <= 0:
        errors.append("Gross sales must be greater than 0")

    if not sale_date:
        errors.append("Sale date is required")

    if not branch_id:
        errors.append("Branch is required")

    return errors

def validate_payment(sale_id, amount_paid, payment_method, payment_date, sale_date):
    errors = []

    if not sale_id:
        errors.append("Sale ID is required")

    if not amount_paid or amount_paid <= 0:
        errors.append("Amount must be greater than 0")

    if not payment_method:
        errors.append("Payment method is required")

    if not payment_date:
        errors.append("Date is required")
    elif payment_date < sale_date:
        errors.append("Payment date cannot be before sale date")

    return errors
