import streamlit as st
import pandas as pd
import plotly.express as px

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
    </style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# LOAD DATA FROM GITHUB
# ══════════════════════════════════════════════
@st.cache_data
def load_all_data():
    path = 'https://raw.githubusercontent.com/Sabitha-23/phonepe_project/master/data/'
    agg_trans = pd.read_csv(path + 'aggregated_transaction.csv')
    agg_user  = pd.read_csv(path + 'aggregated_user.csv')
    agg_ins   = pd.read_csv(path + 'aggregated_insurance.csv')
    map_trans = pd.read_csv(path + 'map_transaction.csv')
    map_user  = pd.read_csv(path + 'map_user.csv')
    top_trans = pd.read_csv(path + 'top_transaction.csv')
    top_user  = pd.read_csv(path + 'top_user.csv')
    # Clean state names
    for df in [agg_trans, agg_user, agg_ins, map_trans, map_user, top_trans, top_user]:
        df['state'] = df['state'].str.replace('-', ' ').str.title()
    return agg_trans, agg_user, agg_ins, map_trans, map_user, top_trans, top_user

agg_trans, agg_user, agg_ins, map_trans, map_user, top_trans, top_user = load_all_data()

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

years    = sorted(agg_trans['year'].unique())
quarters = sorted(agg_trans['quarter'].unique())
states   = sorted(agg_trans['state'].unique())

selected_year    = st.sidebar.selectbox("Select Year", ["All"] + list(years))
selected_quarter = st.sidebar.selectbox("Select Quarter", ["All"] + list(quarters))
selected_state   = st.sidebar.selectbox("Select State", ["All"] + list(states))

# ── Apply filters to chart data (excludes state filter for maps) ──
def apply_filters(df, apply_state=True):
    filtered = df.copy()
    if selected_year != "All" and 'year' in filtered.columns:
        filtered = filtered[filtered['year'] == selected_year]
    if selected_quarter != "All" and 'quarter' in filtered.columns:
        filtered = filtered[filtered['quarter'] == selected_quarter]
    if apply_state and selected_state != "All" and 'state' in filtered.columns:
        filtered = filtered[filtered['state'] == selected_state]
    return filtered

# Filtered dataframes — for charts
ft  = apply_filters(agg_trans)
fu  = apply_filters(agg_user)
fi  = apply_filters(agg_ins)
fmt = apply_filters(map_trans)
fmu = apply_filters(map_user)

# Map dataframes — NO state filter so India map always shows all states
ft_map  = apply_filters(agg_trans, apply_state=False)
fmu_map = apply_filters(map_user,  apply_state=False)

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
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💳 Total Transactions", f"{ft['transaction_count'].sum():,.0f}")
    col2.metric("💰 Total Amount", f"₹{ft['transaction_amount'].sum()/1e7:,.0f} Cr")
    col3.metric("📈 Avg Amount", f"₹{ft['transaction_amount'].mean()/1e7:,.2f} Cr")
    col4.metric("🗺️ States Active", f"{ft['state'].nunique()}")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Transaction Type Distribution")
        type_data = ft.groupby('transaction_type')['transaction_count'].sum().reset_index()
        fig = px.pie(type_data, values='transaction_count', names='transaction_type',
                     color_discrete_sequence=px.colors.sequential.Purples_r)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Transaction Amount by Type")
        amt_data = ft.groupby('transaction_type')['transaction_amount'].sum().reset_index()
        amt_data['amount_crores'] = (amt_data['transaction_amount'] / 1e7).round(2)
        fig = px.bar(amt_data, x='transaction_type', y='amount_crores',
                     color='transaction_type',
                     color_discrete_sequence=px.colors.sequential.Purples_r)
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Year-wise Transaction Growth")
        yearly = agg_trans.groupby('year')['transaction_count'].sum().reset_index()
        fig = px.line(yearly, x='year', y='transaction_count',
                      markers=True, color_discrete_sequence=['#5f259f'])
        fig.update_traces(line_width=3, marker_size=8)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Top 10 States by Transaction Amount")
        state_data = ft.groupby('state')['transaction_amount'].sum().reset_index()
        state_data['amount_crores'] = (state_data['transaction_amount'] / 1e7).round(2)
        state_data = state_data.nlargest(10, 'amount_crores')
        fig = px.bar(state_data, x='amount_crores', y='state', orientation='h',
                     color='amount_crores', color_continuous_scale='Purples')
        st.plotly_chart(fig, use_container_width=True)

    # ── India Map — uses ft_map (no state filter) ──
    st.markdown("#### 🗺️ State-wise Transaction Amount Map")
    map_data = ft.groupby('state')['transaction_amount'].sum().reset_index()
    map_data['amount_crores'] = (map_data['transaction_amount'] / 1e7).round(2)
    fig = px.choropleth(
        map_data,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state', color='amount_crores',
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
    col1, col2, col3 = st.columns(3)
    total_users = fmu['registered_users'].sum()
    total_opens = fmu['app_opens'].sum()
    eng_ratio   = round(total_opens / total_users, 2) if total_users > 0 else 0
    col1.metric("👤 Registered Users", f"{total_users:,.0f}")
    col2.metric("📱 App Opens", f"{total_opens:,.0f}")
    col3.metric("🔄 Engagement Ratio", f"{eng_ratio}x")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Top 10 States by Registered Users")
        user_state = fmu.groupby('state')['registered_users'].sum().reset_index()
        user_state = user_state.nlargest(10, 'registered_users')
        fig = px.bar(user_state, x='registered_users', y='state', orientation='h',
                     color='registered_users', color_continuous_scale='Purples')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Top Device Brands")
        brand_data = fu.groupby('brand')['user_count'].sum().reset_index()
        brand_data = brand_data.nlargest(10, 'user_count')
        fig = px.pie(brand_data, values='user_count', names='brand',
                     color_discrete_sequence=px.colors.sequential.Purples_r)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    # ── Engagement Map — uses fmu_map (no state filter) ──
    st.markdown("#### 🗺️ User Engagement Ratio by State")
    eng_state = fmu_map.groupby('state').agg(
        total_opens=('app_opens', 'sum'),
        total_users=('registered_users', 'sum')
    ).reset_index()
    eng_state['engagement_ratio'] = (
        eng_state['total_opens'] / eng_state['total_users'].replace(0, 1)
    ).round(2)
    eng_data = eng_state[['state', 'engagement_ratio']]
    fig = px.choropleth(
        eng_data,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state', color='engagement_ratio',
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
    col1.metric("📋 Total Insurance Policies", f"{fi['insurance_count'].sum():,.0f}")
    col2.metric("💰 Total Insurance Amount", f"₹{fi['insurance_amount'].sum()/1e7:,.0f} Cr")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Top 10 States by Insurance Amount")
        ins_state = fi.groupby('state')['insurance_amount'].sum().reset_index()
        ins_state['amount_crores'] = (ins_state['insurance_amount'] / 1e7).round(2)
        ins_state = ins_state.nlargest(10, 'amount_crores')
        fig = px.bar(ins_state, x='amount_crores', y='state', orientation='h',
                     color='amount_crores', color_continuous_scale='Purples')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Insurance Growth by Year")
        ins_year = agg_ins.groupby('year')['insurance_amount'].sum().reset_index()
        ins_year['amount_crores'] = (ins_year['insurance_amount'] / 1e7).round(2)
        fig = px.line(ins_year, x='year', y='amount_crores',
                      markers=True, color_discrete_sequence=['#5f259f'])
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
        fig = px.bar(dist_data, x='amount_crores', y='label', orientation='h',
                     color='amount_crores', color_continuous_scale='Purples')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Top 10 Districts by Registered Users")
        user_dist = fmu.groupby(['state', 'district'])['registered_users'].sum().reset_index()
        user_dist['label'] = user_dist['state'] + ' - ' + user_dist['district']
        user_dist = user_dist.nlargest(10, 'registered_users')
        fig = px.bar(user_dist, x='registered_users', y='label', orientation='h',
                     color='registered_users', color_continuous_scale='Purples')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Quarter-wise Transaction Performance")
    qtr_data = agg_trans.groupby(['year', 'quarter'])['transaction_amount'].sum().reset_index()
    qtr_data['amount_crores'] = (qtr_data['transaction_amount'] / 1e7).round(2)
    qtr_data['year_quarter']  = qtr_data['year'].astype(str) + '-Q' + qtr_data['quarter'].astype(str)
    fig = px.bar(qtr_data, x='year_quarter', y='amount_crores',
                 color='quarter', color_continuous_scale='Purples')
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