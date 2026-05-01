import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

# ══════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="PhonePe Pulse Dashboard",
    page_icon="💜",
    layout="wide"
)

# ══════════════════════════════════════════════
# CUSTOM CSS
# ══════════════════════════════════════════════
st.markdown("""
    <style>
    .main { background-color: #f0f0f0; }
    .block-container { padding-top: 1rem; }
    h1 { color: #5f259f; }
    h2, h3 { color: #3d1a6e; }
    .metric-card {
        background-color: #5f259f;
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# DB CONNECTION
# ══════════════════════════════════════════════
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="2301",  
        database="phonepe_pulse"
    )

@st.cache_data
def load_data(query):
    conn = get_connection()
    return pd.read_sql(query, conn)

# ══════════════════════════════════════════════
# LOAD ALL DATA
# ══════════════════════════════════════════════
agg_trans = load_data("SELECT * FROM aggregated_transaction")
agg_user  = load_data("SELECT * FROM aggregated_user")
agg_ins   = load_data("SELECT * FROM aggregated_insurance")
map_trans = load_data("SELECT * FROM map_transaction")
map_user  = load_data("SELECT * FROM map_user")
top_trans = load_data("SELECT * FROM top_transaction")
top_user  = load_data("SELECT * FROM top_user")

# Clean state names
for df in [agg_trans, agg_user, agg_ins, map_trans, map_user, top_trans, top_user]:
    df['state'] = df['state'].str.replace('-', ' ').str.title()

# ══════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════
st.markdown("""
    <h1 style='text-align: center;'>💜 PhonePe Pulse Dashboard</h1>
    <p style='text-align: center; color: gray;'>
        Interactive insights on Transactions, Users & Insurance across India
    </p>
    <hr>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# SIDEBAR FILTERS
# ══════════════════════════════════════════════
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/PhonePe_Logo.png/200px-PhonePe_Logo.png",
    width=150
)
st.sidebar.title("🔍 Filters")

years     = sorted(agg_trans['year'].unique())
quarters  = sorted(agg_trans['quarter'].unique())
states    = sorted(agg_trans['state'].unique())

selected_year    = st.sidebar.selectbox("Select Year", ["All"] + list(years))
selected_quarter = st.sidebar.selectbox("Select Quarter", ["All"] + list(quarters))
selected_state   = st.sidebar.selectbox("Select State", ["All"] + list(states))

# Apply filters
def apply_filters(df):
    filtered = df.copy()
    if selected_year != "All":
        filtered = filtered[filtered['year'] == selected_year]
    if selected_quarter != "All":
        filtered = filtered[filtered['quarter'] == selected_quarter]
    if 'state' in filtered.columns and selected_state != "All":
        filtered = filtered[filtered['state'] == selected_state]
    return filtered

ft = apply_filters(agg_trans)
fu = apply_filters(agg_user)
fi = apply_filters(agg_ins)
fmt = apply_filters(map_trans)
fmu = apply_filters(map_user)

# ══════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Transactions", "👥 Users", "🛡️ Insurance", "🏆 Top Performers"
])

# ══════════════════════════════════════════════
# TAB 1 — TRANSACTIONS
# ══════════════════════════════════════════════
with tab1:
    st.subheader("📊 Transaction Overview")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    total_count  = ft['transaction_count'].sum()
    total_amount = ft['transaction_amount'].sum() / 1e7
    avg_amount   = ft['transaction_amount'].mean() / 1e7
    total_states = ft['state'].nunique()

    col1.metric("💳 Total Transactions", f"{total_count:,.0f}")
    col2.metric("💰 Total Amount", f"₹{total_amount:,.0f} Cr")
    col3.metric("📈 Avg Amount", f"₹{avg_amount:,.2f} Cr")
    col4.metric("🗺️ States Active", f"{total_states}")

    st.markdown("---")

    # Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Transaction Type Distribution")
        type_data = ft.groupby('transaction_type')['transaction_count'].sum().reset_index()
        fig = px.pie(type_data, values='transaction_count',
                     names='transaction_type',
                     color_discrete_sequence=px.colors.sequential.Purples_r)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Transaction Amount by Type")
        amt_data = ft.groupby('transaction_type')['transaction_amount'].sum().reset_index()
        amt_data['amount_crores'] = (amt_data['transaction_amount'] / 1e7).round(2)
        fig = px.bar(amt_data, x='transaction_type', y='amount_crores',
                     color='transaction_type',
                     color_discrete_sequence=px.colors.sequential.Purples_r,
                     labels={'amount_crores': 'Amount (Crores)', 'transaction_type': 'Type'})
        st.plotly_chart(fig, use_container_width=True)

    # Row 2
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Year-wise Transaction Growth")
        yearly = agg_trans.groupby('year')['transaction_count'].sum().reset_index()
        fig = px.line(yearly, x='year', y='transaction_count',
                      markers=True,
                      color_discrete_sequence=['#5f259f'])
        fig.update_traces(line_width=3, marker_size=8)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Top 10 States by Transaction Amount")
        state_data = ft.groupby('state')['transaction_amount'].sum().reset_index()
        state_data['amount_crores'] = (state_data['transaction_amount'] / 1e7).round(2)
        state_data = state_data.nlargest(10, 'amount_crores')
        fig = px.bar(state_data, x='amount_crores', y='state',
                     orientation='h',
                     color='amount_crores',
                     color_continuous_scale='Purples',
                     labels={'amount_crores': 'Amount (Crores)', 'state': 'State'})
        st.plotly_chart(fig, use_container_width=True)

    # Row 3 — India Map
    st.markdown("#### 🗺️ State-wise Transaction Amount Map")
    map_data = ft.groupby('state')['transaction_amount'].sum().reset_index()
    map_data['amount_crores'] = (map_data['transaction_amount'] / 1e7).round(2)
    fig = px.choropleth(
        map_data,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='amount_crores',
        color_continuous_scale='Purples',
        title='Transaction Amount by State (Crores)'
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 2 — USERS
# ══════════════════════════════════════════════
with tab2:
    st.subheader("👥 User Engagement Overview")

    # KPI Cards
    col1, col2, col3 = st.columns(3)
    total_users   = fmu['registered_users'].sum()
    total_opens   = fmu['app_opens'].sum()
    eng_ratio     = (total_opens / total_users).round(2) if total_users > 0 else 0

    col1.metric("👤 Registered Users", f"{total_users:,.0f}")
    col2.metric("📱 App Opens", f"{total_opens:,.0f}")
    col3.metric("🔄 Engagement Ratio", f"{eng_ratio}x")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top 10 States by Registered Users")
        user_state = fmu.groupby('state')['registered_users'].sum().reset_index()
        user_state = user_state.nlargest(10, 'registered_users')
        fig = px.bar(user_state, x='registered_users', y='state',
                     orientation='h',
                     color='registered_users',
                     color_continuous_scale='Purples')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Top Device Brands")
        brand_data = fu.groupby('brand')['user_count'].sum().reset_index()
        brand_data = brand_data.nlargest(10, 'user_count')
        fig = px.pie(brand_data, values='user_count', names='brand',
                     color_discrete_sequence=px.colors.sequential.Purples_r)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    # Engagement ratio map
    st.markdown("#### 🗺️ User Engagement Ratio by State")
    eng_data = fmu.groupby('state').apply(
        lambda x: (x['app_opens'].sum() / x['registered_users'].sum()).round(2), include_groups=False
    ).reset_index()
    eng_data.columns = ['state', 'engagement_ratio']
    fig = px.choropleth(
        eng_data,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='engagement_ratio',
        color_continuous_scale='Purples',
        title='App Opens per Registered User by State'
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 3 — INSURANCE
# ══════════════════════════════════════════════
with tab3:
    st.subheader("🛡️ Insurance Overview")

    col1, col2 = st.columns(2)
    total_ins_count  = fi['insurance_count'].sum()
    total_ins_amount = fi['insurance_amount'].sum() / 1e7

    col1.metric("📋 Total Insurance Policies", f"{total_ins_count:,.0f}")
    col2.metric("💰 Total Insurance Amount", f"₹{total_ins_amount:,.0f} Cr")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top 10 States by Insurance Amount")
        ins_state = fi.groupby('state')['insurance_amount'].sum().reset_index()
        ins_state['amount_crores'] = (ins_state['insurance_amount'] / 1e7).round(2)
        ins_state = ins_state.nlargest(10, 'amount_crores')
        fig = px.bar(ins_state, x='amount_crores', y='state',
                     orientation='h',
                     color='amount_crores',
                     color_continuous_scale='Purples')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Insurance Growth by Year")
        ins_year = agg_ins.groupby('year')['insurance_amount'].sum().reset_index()
        ins_year['amount_crores'] = (ins_year['insurance_amount'] / 1e7).round(2)
        fig = px.line(ins_year, x='year', y='amount_crores',
                      markers=True,
                      color_discrete_sequence=['#5f259f'])
        fig.update_traces(line_width=3, marker_size=8)
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 4 — TOP PERFORMERS
# ══════════════════════════════════════════════
with tab4:
    st.subheader("🏆 Top Performers")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top 10 Districts by Transaction Amount")
        dist_data = fmt.groupby(['state', 'district'])['transaction_amount'].sum().reset_index()
        dist_data['amount_crores'] = (dist_data['transaction_amount'] / 1e7).round(2)
        dist_data['label'] = dist_data['state'] + ' - ' + dist_data['district']
        dist_data = dist_data.nlargest(10, 'amount_crores')
        fig = px.bar(dist_data, x='amount_crores', y='label',
                     orientation='h',
                     color='amount_crores',
                     color_continuous_scale='Purples')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Top 10 Districts by Registered Users")
        user_dist = fmu.groupby(['state', 'district'])['registered_users'].sum().reset_index()
        user_dist['label'] = user_dist['state'] + ' - ' + user_dist['district']
        user_dist = user_dist.nlargest(10, 'registered_users')
        fig = px.bar(user_dist, x='registered_users', y='label',
                     orientation='h',
                     color='registered_users',
                     color_continuous_scale='Purples')
        st.plotly_chart(fig, use_container_width=True)

    # Quarter performance
    st.markdown("#### Quarter-wise Transaction Performance")
    qtr_data = agg_trans.groupby(['year', 'quarter'])['transaction_amount'].sum().reset_index()
    qtr_data['amount_crores'] = (qtr_data['transaction_amount'] / 1e7).round(2)
    qtr_data['year_quarter'] = qtr_data['year'].astype(str) + '-Q' + qtr_data['quarter'].astype(str)
    fig = px.bar(qtr_data, x='year_quarter', y='amount_crores',
                 color='quarter',
                 color_continuous_scale='Purples',
                 labels={'amount_crores': 'Amount (Crores)', 'year_quarter': 'Year-Quarter'})
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════
st.markdown("---")
st.markdown("""
    <p style='text-align: center; color: gray;'>
        💜 PhonePe Pulse Dashboard | Built by Sabitha | Data Source: PhonePe Pulse GitHub
    </p>
""", unsafe_allow_html=True)