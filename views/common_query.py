import utility.questions as questions
import streamlit as st

st.set_page_config(layout="wide")
user = st.session_state.user

col_title, col_user = st.columns([3, 1])

with col_title:
    st.markdown("<h1>Common query</h1>", unsafe_allow_html=True)

with col_user:
    st.markdown(f"""
        <div style='text-align: right; padding-top: 15px;'>
            👤 <b>{user['username']}</b><br>
            <small>{user['role']}</small>
        </div>
    """, unsafe_allow_html=True)

st.divider()

questions =  {
    "All Customers Sales": questions.get_customers_sales,
    "All Branches": questions.get_branches,
    "All Payment Splits": questions.get_payment_splits,
    "All Open Sales": questions.get_all_sales_by_status,
    "Total Gross Sales by Branch": questions.get_total_grosssales_all_branch,
    "Total Received Amount": questions.get_total_received_amount,
    "Total Pending Amount": questions.get_total_pending_amount,
    "Count of Sales by Branch": questions.get_count_of_sales_by_branch,
    "Customers Sales with Branch Name": questions.get_customers_sales_with_branch_name,
    "Customers Sales with Total Payment": questions.get_customers_sales_with_total_payment,
    "Customers Sales by Branchwise": questions.get_customers_sales_by_branchwise,
    "Customers Sales with Admin Name": questions.get_customers_sales_with_admin_name,
    "Total Collection by Payment Method": questions.get_total_collection_by_payment_method,
    "Pending Amount Greater than 5000": questions.get_pending_amount_greater_than_5000,
    "Top Three Gross Sales": questions.get_topthree_gross_sales
}
selected_query_name = st.selectbox("❓ Query ", options=[""] + list(questions.keys()))

if selected_query_name:
    data = questions[selected_query_name]()
    st.dataframe(data, use_container_width=True, hide_index=True)
