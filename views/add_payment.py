import streamlit as st
from datetime import date
from utility.queries import get_branches, get_open_sales, insert_payment
from utility.validators import validate_payment

st.set_page_config(layout="wide")

user = st.session_state.user

#  Fetch data 
branch_map = {b['branch_id']: b['branch_name'] for b in get_branches()}
sales_map = {s['sale_id']: (s['branch_id'], s['pending_amount'], s['date']) for s in get_open_sales(user['role'], user.get('branch_id'))}

#  Header 
st.markdown("<h2>➕ Add Payment</h2>", unsafe_allow_html=True)
st.divider()

#  Branch select 
if user['role'] == "Super Admin":
    branch_options = {v: k for k, v in branch_map.items()}
    selected_branch_name = st.selectbox("🏢 Branch", options=[""] + list(branch_options.keys()))
    branch_id = branch_options.get(selected_branch_name)
else:
    st.markdown(f"**🏢 Branch:** {branch_map.get(user['branch_id'], '—')}")
    branch_id = user['branch_id']

#  Sale ID select 
if user['role'] == "Super Admin":
    filtered_sales = [""] + [k for k, v in sales_map.items() if v[0] == branch_id]
else:
    filtered_sales = [""] + list(sales_map.keys())

selected_sale_id = st.selectbox("🧾 Sale ID", options=filtered_sales)

#  Show sale info 
pending_amount = 0.0
sale_date = date.today()

if selected_sale_id:
    pending_amount = sales_map[selected_sale_id][1]
    sale_date = sales_map[selected_sale_id][2]
    st.info(f"📌 Pending Amount: ₹{pending_amount:,} | Sale Date: {sale_date}")
else:
    st.warning("⚠️ Please select a Sale ID")

#  Form 
with st.form("add_payment_form", clear_on_submit=True):
    amount_paid = st.number_input(
        "💰 Amount",
        min_value=0.0,
        max_value=float(pending_amount) if pending_amount else 0.0,
        step=1.0
    )
    payment_method = st.selectbox("💳 Payment Method", options=["Cash", "UPI", "Card"])
    payment_date = st.date_input("📅 Payment Date", value=date.today(), min_value=sale_date)

    submitted = st.form_submit_button(
        "💾 Save Payment",
        width='stretch'
    )

#  On Submit 
if submitted:
    errors = validate_payment(selected_sale_id, amount_paid, payment_method, payment_date, sale_date)

    if errors:
        for error in errors:
            st.error(f"❌ {error}")
    else:
        try:
            insert_payment(selected_sale_id, payment_date, amount_paid, payment_method)
            st.success("✅ Payment saved successfully!")
        except Exception as e:
            st.error(f"❌ Database error: {str(e)}")
