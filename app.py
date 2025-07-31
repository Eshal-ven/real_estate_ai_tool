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

# ---------------- API KEYS ----------------
EXCHANGE_API_KEY = "6765835acf37d023c7ca3f8a"  # ExchangeRate API
OPENCAGE_API_KEY = "b7ff050f08204f8abb29020b73fffdf5"  # OpenCage Geocoding
GEOAPIFY_API_KEY = "17c2750503544d329fd46895ff1e6ede"  # Geoapify for Map Tiles

# ---------------- CURRENCY CONVERSION ----------------
@st.cache_data
def get_conversion_rates(base="USD"):
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{base}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("conversion_rates", {})
    except:
        st.warning("Using fallback currency rates.")
        return {"USD": 1, "PKR": 278, "EUR": 0.91, "GBP": 0.78}

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
        st.error("Failed to geocode the location.")
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
    pdf.output(buffer)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="report.pdf">Download PDF Report</a>'
    return href

# ---------------- STREAMLIT APP ----------------
st.set_page_config(page_title="Real Estate ROI Tool", layout="wide")
st.title("🏠 Real Estate Investment Analyzer")

# Inputs
st.sidebar.header("📥 Enter Property Details")
location = st.sidebar.text_input("Enter Property Location", "Islamabad, Pakistan")
purchase_price = st.sidebar.number_input("Purchase Price ($)", value=100000)
monthly_rent = st.sidebar.number_input("Monthly Rent ($)", value=1000)
expenses = st.sidebar.number_input("Monthly Expenses ($)", value=300)
duration_years = st.sidebar.slider("Investment Duration (Years)", 1, 30, 10)

# Currency selection
rates = get_conversion_rates("USD")
currency = st.sidebar.selectbox("Convert to Currency", list(rates.keys()))
conversion_rate = rates.get(currency, 1)

# ROI Calculation
total_income = monthly_rent * 12 * duration_years
total_expense = expenses * 12 * duration_years
net_profit = total_income - total_expense
roi = (net_profit / purchase_price) * 100
converted_profit = net_profit * conversion_rate
converted_price = purchase_price * conversion_rate

# Display ROI
st.metric("Total ROI (%)", f"{roi:.2f}%")
st.metric("Net Profit (Converted)", f"{converted_profit:.2f} {currency}")

# PDF Report
if st.button("📄 Generate PDF Report"):
    href = generate_pdf(purchase_price, roi, location)
    st.markdown(href, unsafe_allow_html=True)

# Geocode & Map
lat, lon = geocode_location(location)
if lat and lon:
    st.subheader("🗺 Property Location Map")
    m = folium.Map(location=[lat, lon], zoom_start=13, tiles=f"https://maps.geoapify.com/v1/tile/osm-carto/{{z}}/{{x}}/{{y}}.png?apiKey={GEOAPIFY_API_KEY}", attr="Geoapify")
    folium.Marker([lat, lon], popup=location).add_to(m)
    st_folium(m, width=700, height=500)

# Upload CSV
st.subheader("📁 Upload Real Estate Dataset")
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Sample Data:", df.head())

    # Visuals
    st.subheader("📊 Data Visualizations")
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if numeric_cols:
        x_col = st.selectbox("X-axis", numeric_cols)
        y_col = st.selectbox("Y-axis", numeric_cols, index=1)
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
        st.pyplot(fig)
    else:
        st.warning("No numeric columns found for plotting.")

