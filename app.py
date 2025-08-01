import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from fpdf import FPDF
from io import BytesIO
import base64

# ---------------- API KEYS FROM SECRETS ----------------
EXCHANGE_API_KEY = st.secrets["api"]["currency_key"]
OPENCAGE_API_KEY = st.secrets["api"]["opencage_key"]
GEOAPIFY_API_KEY = st.secrets["api"]["geoapify_key"]

# ---------------- CURRENCY CONVERSION ----------------
@st.cache_data(ttl=3600)
def get_conversion_rates(base="USD"):
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{base}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("conversion_rates", {})
    except:
        st.warning("⚠️ Using fallback currency rates.")
        return {"USD": 1, "PKR": 283.75 , "EUR": 0.88 , "GBP": 0.76 }

# ---------------- GEOCODING LOCATION ----------------
def geocode_location(location):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={OPENCAGE_API_KEY}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        if data['results']:
            geometry = data['results'][0]['geometry']
            return geometry['lat'], geometry['lng']
    except:
        st.error("❌ Failed to geocode location.")
        return None, None

# ---------------- PDF GENERATION ----------------
def generate_pdf(investment, roi, location):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Real Estate Investment Report", ln=True, align="C")
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Investment Amount: {investment}\nLocation: {location}\nROI: {roi:.2f}%")
    buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')  # Fixed line
    buffer.write(pdf_output)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="report.pdf">📄 Download PDF Report</a>'
    return href

# ---------------- ROI ANALYSIS FUNCTION ----------------
def analyze_property(purchase_price, monthly_rent, expenses, years, downpayment_pct):
    downpayment = (downpayment_pct / 100) * purchase_price
    total_income = monthly_rent * 12 * years
    total_expense = expenses * 12 * years
    net_profit = total_income - total_expense
    roi = (net_profit / downpayment) * 100 if downpayment else 0
    return downpayment, net_profit, roi

# ---------------- STREAMLIT APP ----------------
st.set_page_config(page_title="Real Estate ROI Tool", layout="wide")
st.title("🏠 Real Estate Investment Analyzer")

tab1, tab2, tab3 = st.tabs(["🔍 Single Property", "📊 Compare Properties", "📬 Contact Me"])

# --- TAB 1: Single Property ---
with tab1:
    st.sidebar.header("📥 Enter Property Details")
    location = st.sidebar.text_input("Enter Property Location", "Islamabad, Pakistan")
    purchase_price = st.sidebar.number_input("Purchase Price ($)", value=100000)
    monthly_rent = st.sidebar.number_input("Monthly Rent ($)", value=1000)
    expenses = st.sidebar.number_input("Monthly Expenses ($)", value=300)
    duration_years = st.sidebar.slider("Investment Duration (Years)", 1, 30, 10)
    downpayment_pct = st.sidebar.slider("Downpayment (%)", 0, 100, 20)
    risk_rating = st.sidebar.slider("Risk Rating (1 Low - 10 High)", 1, 10, 5)

    rates = get_conversion_rates("USD")
    currency = st.sidebar.selectbox("Convert to Currency", list(rates.keys()))
    conversion_rate = rates.get(currency, 1)

    downpayment, net_profit, roi = analyze_property(purchase_price, monthly_rent, expenses, duration_years, downpayment_pct)
    converted_profit = net_profit * conversion_rate
    converted_price = purchase_price * conversion_rate

    st.metric("Total ROI (%)", f"{roi:.2f}%")
    st.metric("Net Profit (Converted)", f"{converted_profit:.2f} {currency}")
    st.write(f"**Downpayment:** ${downpayment:,.2f}")

    if roi > 10 and risk_rating <= 5:
        st.success("✅ Good Investment Opportunity")
    elif roi > 5 and risk_rating <= 7:
        st.warning("⚠️ Moderate Risk. Analyze More")
    else:
        st.error("❌ High Risk / Low ROI")

    if st.button("📄 Generate PDF Report"):
        href = generate_pdf(purchase_price, roi, location)
        st.markdown(href, unsafe_allow_html=True)

    lat, lon = geocode_location(location)
    if lat and lon:
        st.subheader("🗺 Property Location Map")
        m = folium.Map(location=[lat, lon], zoom_start=13,
                       tiles=f"https://maps.geoapify.com/v1/tile/osm-carto/{{z}}/{{x}}/{{y}}.png?apiKey={GEOAPIFY_API_KEY}",
                       attr="Geoapify")
        folium.Marker([lat, lon], popup=location).add_to(m)
        st_folium(m, width=700, height=500)

# --- TAB 2: Compare Properties ---
with tab2:
    st.subheader("📊 Compare Two Properties Side-by-Side")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏘 Property 1")
        p1_price = st.number_input("P1 Purchase Price ($)", value=120000, key='p1_price')
        p1_rent = st.number_input("P1 Monthly Rent ($)", value=1200, key='p1_rent')
        p1_exp = st.number_input("P1 Monthly Expenses ($)", value=400, key='p1_exp')
        p1_years = st.slider("P1 Investment Years", 1, 30, 10, key='p1_years')
        p1_down = st.slider("P1 Downpayment (%)", 0, 100, 20, key='p1_down')

    with col2:
        st.markdown("### 🏘 Property 2")
        p2_price = st.number_input("P2 Purchase Price ($)", value=150000, key='p2_price')
        p2_rent = st.number_input("P2 Monthly Rent ($)", value=1500, key='p2_rent')
        p2_exp = st.number_input("P2 Monthly Expenses ($)", value=500, key='p2_exp')
        p2_years = st.slider("P2 Investment Years", 1, 30, 10, key='p2_years')
        p2_down = st.slider("P2 Downpayment (%)", 0, 100, 25, key='p2_down')

    p1_down_amt, p1_profit, p1_roi = analyze_property(p1_price, p1_rent, p1_exp, p1_years, p1_down)
    p2_down_amt, p2_profit, p2_roi = analyze_property(p2_price, p2_rent, p2_exp, p2_years, p2_down)

    st.markdown("### 📈 ROI Comparison Chart")
    comparison_df = pd.DataFrame({
        "Property": ["Property 1", "Property 2"],
        "ROI (%)": [p1_roi, p2_roi],
        "Net Profit ($)": [p1_profit, p2_profit],
        "Downpayment ($)": [p1_down_amt, p2_down_amt]
    })

    st.dataframe(comparison_df)

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x="Property", y="ROI (%)", data=comparison_df, palette="viridis", ax=ax)
    ax.set_title("ROI Comparison")
    st.pyplot(fig)

# --- TAB 3: Contact ---
with tab3:
    st.header("📬 Contact the Developer")
    st.markdown("Feel free to connect on [LinkedIn](https://www.linkedin.com/in/eshal-fatima-) or email me at `eshlfatimah@gmail.com`.")



