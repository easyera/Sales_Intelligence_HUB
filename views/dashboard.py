import streamlit as st
from datetime import date, timedelta
from utility.queries import (
    get_branches, get_products, build_filters,
    get_KPI_data, get_sales_data, get_status_summary,
    get_branch_summary, get_payment_summary
)

st.set_page_config(layout="wide")

user = st.session_state.user

#  Fetch filter options 
branch_map = {b['branch_id']: b['branch_name'] for b in get_branches()}
product_options = [p['product_name'] for p in get_products()]

#  Header 
col_title, col_user = st.columns([3, 1])

with col_title:
    st.markdown("<h1>Sales Dashboard</h1>", unsafe_allow_html=True)

with col_user:
    st.markdown(f"""
        <div style='text-align: right; padding-top: 15px;'>
            👤 <b>{user['username']}</b><br>
            <small>{user['role']}</small>
        </div>
    """, unsafe_allow_html=True)

st.divider()

#  Navigation 
col1, col2, col3 = st.columns([5, 5, 5])

with col1:
    if st.button("➕ Add Sale", use_container_width=True):
        st.switch_page("views/add_sale.py")

with col2:
    if st.button("💳 Add Payment", use_container_width=True):
        st.switch_page("views/add_payment.py")

st.divider()

#  Filters 
filter_cols = st.columns(4)

with filter_cols[0]:
    if user['role'] == "Super Admin":
        branch_options = {"All": None, **{v: k for k, v in branch_map.items()}}
        selected_branch_name = st.selectbox("🏢 Branch", options=list(branch_options.keys()))
        selected_branch_id = branch_options[selected_branch_name]
    else:
        st.markdown("**🏢 Branch**")
        st.write(branch_map.get(user['branch_id'], '—'))
        selected_branch_id = user['branch_id']

today = date.today()
last_day = date(today.year + (today.month // 12), today.month % 12 + 1, 1) - timedelta(days=1)

with filter_cols[1]:
    date_from = st.date_input("📅 From", value=today.replace(day=1))

with filter_cols[2]:
    date_to = st.date_input("📅 To", value=last_day, min_value=date_from)

with filter_cols[3]:
    status = st.selectbox("📌 Status", options=["All", "Open", "Close"])

selected_products = st.multiselect("📦 Product", options=product_options)

st.divider()

#  Apply filters 
where, params = build_filters(
    role=user['role'],
    branch_id=selected_branch_id,
    date_from=date_from,
    date_to=date_to,
    status=status,
    products=selected_products
)

#  KPI Cards 
kpi = get_KPI_data(where, params)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Total Sales", f"₹{kpi['total_sales']:,}")
with col2:
    st.metric("✅ Total Received", f"₹{kpi['total_received']:,}")
with col3:
    st.metric("⏳ Total Pending", f"₹{kpi['total_pending']:,}")
with col4:
    st.metric("🛒 Total Orders", kpi['total_orders'])

st.divider()

#  Sales Table 
st.header("Sales")
sales = get_sales_data(where, params)
row_height = 35
header_height = 38
dynamic_height = min(header_height + len(sales) * row_height, 400)
st.dataframe(sales, use_container_width=True, hide_index=True, height=dynamic_height)

st.divider()

#  Pending Table 
st.header("Pending Sales")
where_pending = where + " AND pending_amount > 0" if where else "WHERE pending_amount > 0"
pending = get_sales_data(where_pending, params)
dynamic_height = min(header_height + len(pending) * row_height, 400)
st.dataframe(pending, use_container_width=True, hide_index=True, height=dynamic_height)

st.divider()

#  Summaries 
st.markdown("### 📊 Summaries")

col1, col2, col3 = st.columns(3)
status_data = get_status_summary(where, params)

with col1:
    st.markdown("**📌 Sales Status**")
    if not status_data:
        st.caption("No sales found")
    else:
        for row in status_data:
            if row['status'] == 'Open':
                st.metric(f"🟡 {row['status']}", f"₹{row['total_gross']:,}", f"{row['count']} orders")
                st.caption(f"Received: ₹{row['total_received']:,} | Pending: ₹{row['total_pending']:,}")
            else:
                st.metric(f"🟢 {row['status']}", f"₹{row['total_gross']:,}", f"{row['count']} orders")

with col2:
    st.markdown("**⏳ Pending**")
    if not status_data:
        st.caption("No sales found")
    else:
        pending_row = next((row for row in status_data if row['status'] == 'Open'), None)
        if pending_row:
            st.metric("⏳ Total Pending", f"₹{pending_row['total_pending']:,}", f"{pending_row['count']} orders")
        else:
            st.metric("⏳ Total Pending", "₹0")

with col3:
    st.markdown("**💳 Payment Methods**")
    payment_data = get_payment_summary(where, params)
    if not payment_data:
        st.caption("No payments found")
    else:
        payment_icons = {"Cash": "💵", "UPI": "📱", "Card": "💳"}
        with st.container(height=300):
            for row in payment_data:
                icon = payment_icons.get(row['payment_method'], "💰")
                st.metric(f"{icon} {row['payment_method']}", f"₹{row['total']:,}", f"{row['count']} payments")

#  Branch Performance 
if user['role'] == "Super Admin":
    st.divider()
    st.markdown("### 🏢 Branch Performance Summary")
    branch_data = get_branch_summary(date_from, date_to, status, selected_products)

    if not branch_data:
        st.caption("No data found")
    else:
        # Format for display
        formatted = [{
            "🏢 Branch": row['branch_name'],
            "💰 Total Sales": f"₹{row['total_sales']:,}",
            "✅ Received": f"₹{row['total_received']:,}",
            "⏳ Pending": f"₹{row['total_pending']:,}",
            "🛒 Orders": row['total_orders']
        } for row in branch_data]

        row_height = 35
        header_height = 38
        dynamic_height = min(header_height + len(formatted) * row_height, 400)

        st.dataframe(formatted, use_container_width=True, hide_index=True, height=dynamic_height)
    

    