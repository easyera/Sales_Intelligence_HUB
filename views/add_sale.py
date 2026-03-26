import streamlit as st
from datetime import date
from utility.queries import get_branches, get_products, insert_sale
from utility.validators import validate_sale

st.set_page_config(layout="wide")

user = st.session_state.user

#  Fetch options 
branch_map = {b['branch_id']: b['branch_name'] for b in get_branches()}
product_options = [p['product_name'] for p in get_products()]

#  Header 
st.markdown("<h2>➕ Add Sale</h2>", unsafe_allow_html=True)
st.divider()

#  Form 
with st.form("add_sale_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("👤 Customer Name")
        mobile = st.text_input("📱 Mobile Number")
        sale_date = st.date_input("📅 Sale Date", value=date.today())

    with col2:
        product = st.selectbox("📦 Product", options=[""] + product_options)
        gross_sales = st.number_input("💰 Gross Sales (₹)", min_value=0.0, step=0.01, format="%.2f")

        if user['role'] == "Super Admin":
            branch_options = {v: k for k, v in branch_map.items()}
            selected_branch_name = st.selectbox("🏢 Branch", options=[""] + list(branch_options.keys()))
            branch_id = branch_options.get(selected_branch_name)
        else:
            st.markdown(f"**🏢 Branch:** {branch_map.get(user['branch_id'], '—')}")
            branch_id = user['branch_id']

    submitted = st.form_submit_button("💾 Save Sale", width='stretch')

#  On Submit 
if submitted:
    errors = validate_sale(name, mobile, product, gross_sales, sale_date, branch_id)

    if errors:
        for error in errors:
            st.error(f"❌ {error}")
    else:
        try:
            insert_sale(branch_id, sale_date, gross_sales, mobile.strip(), name.strip(), product.strip())
            st.success("✅ Sale added successfully!")
        except Exception as e:
            st.error(f"❌ Database error: {str(e)}")
