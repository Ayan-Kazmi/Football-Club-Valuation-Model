import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# 1. Page Configuration
st.set_page_config(page_title="Football Club Valuation & FFP Model", layout="wide")

st.title("⚽ European Football Club Valuation & Financial Health Dashboard")
st.markdown("Explore club valuations, financial fair play (FFP) compliance, and run predictive scenarios using machine learning.")

# 2. Load Data (Using the processed data you created)
@st.cache_data
def load_data():
    # In your GitHub repo, this reads from your processed folder
    df = pd.read_csv('data/processed/master_club_analytics.csv')
    return df

try:
    df = load_data()
except Exception:
    st.error("Processed data file not found! Make sure your Phase 2 script has been run and saved.")
    st.stop()

# 3. Sidebar Configuration for Scenario Analysis
st.sidebar.header("🔍 Club Scenario Simulator")
selected_club = st.sidebar.selectbox("Select a Club to Analyze", df['Club_ID'].unique())

# Filter data for selected club
club_data = df[df['Club_ID'] == selected_club].iloc[0]

st.sidebar.markdown("---")
st.sidebar.subheader("Adjust Financials for Simulation")
sim_revenue = st.sidebar.number_input("Total Revenue (€M)", value=float(club_data['Total_Revenue_M']))
sim_wages = st.sidebar.number_input("Total Wage Bill (€M)", value=float(club_data['Total_Wage_Bill_M']))

# Calculate simulated ratios
sim_wage_ratio = sim_wages / sim_revenue if sim_revenue > 0 else 0
sim_ffp_safe = sim_wage_ratio <= 0.70

# 4. Main Dashboard Layout - Columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Baseline Enterprise Value", value=f"€{club_data['Enterprise_Value_M']:,.0f}M")
with col2:
    st.metric(label="Actual Wage-to-Revenue", value=f"{club_data['Wage_to_Revenue_Ratio']*100:.1f}%")
with col3:
    st.metric(label="FFP Status (Baseline)", value="Safe ✅" if club_data['FFP_Compliant'] else "At Risk ⚠️")

st.markdown("---")

# 5. Interactive Simulation Results
st.subheader(f"📊 Simulation Results for: {selected_club}")
sim_col1, sim_col2 = st.columns(2)

with sim_col1:
    st.write(f"**Simulated Wage-to-Revenue Ratio:** {sim_wage_ratio*100:.1f}%")
    if sim_ffp_safe:
        st.success("Result: **FFP Compliant** under simulated conditions (Wage burden <= 70%).")
    else:
        st.error("Result: **FFP Compliance Breach Risk** (Wage burden exceeds 70% threshold).")

with sim_col2:
    st.write("**Club Financial Breakdown:**")
    st.dataframe(df[df['Club_ID'] == selected_club][['League', 'Matchday_Revenue_M', 'Broadcast_Revenue_M', 'Commercial_Revenue_M', 'Net_Debt_M']])

# 6. Data Table Overview
with st.expander("View Full Master Dataset"):
    st.dataframe(df)