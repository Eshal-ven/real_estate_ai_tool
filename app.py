import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF
import io


def get_market_data(location):
    city = location.lower()
    if any(term in city for term in ["austin", "nashville", "denver", "941", "787"]):
        return {"rent_per_sqft": 2.5, "price_per_sqft": 350, "demand": "High", "risk": "Low"}
    elif any(term in city for term in ["tulsa", "fresno", "charlotte", "606", "750"]):
        return {"rent_per_sqft": 1.8, "price_per_sqft": 250, "demand": "Medium", "risk": "Medium"}
    else:
        return {"rent_per_sqft": 1.2, "price_per_sqft": 150, "demand": "Low", "risk": "High"}


def real_estate_analysis(price, expected_rent, annual_expenses, downpayment, location, sqft):
    market = get_market_data(location)
    est_rent = market["rent_per_sqft"] * sqft
    est_price = market["price_per_sqft"] * sqft
    annual_income = expected_rent * 12
    net_operating_income = annual_income - annual_expenses
    cash_flow = net_operating_income
    cap_rate = (net_operating_income / price) * 100
    roi = (cash_flow / price) * 100
    cash_on_cash = (cash_flow / downpayment) * 100

    recommendation = "Buy" if cash_on_cash >= 10 else "Hold" if cash_on_cash >= 5 else "Avoid"

    return {
        "ROI %": round(roi, 2),
        "Cap Rate %": round(cap_rate, 2),
        "Cash-on-Cash Return %": round(cash_on_cash, 2),
        "Recommendation": recommendation,
        "Market Rent Estimate ($/mo)": round(est_rent, 2),
        "Market Price Estimate": round(est_price, 2),
        "Demand Score": market["demand"],
        "Risk Score": market["risk"]
    }


def generate_pdf(results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Real Estate Investment Report", ln=True, align="C")
    pdf.ln(10)
    for key, value in results.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    return pdf.output(dest='S').encode('latin-1')


st.title("🏘️ Real Estate ROI Analyzer")
st.markdown("Analyze, compare, and export your property investments.")

st.subheader("🏠 Property #1")
col1, col2 = st.columns(2)
with col1:
    price1 = st.number_input("Price ($)", key="p1", value=300000)
    rent1 = st.number_input("Expected Rent ($/mo)", key="r1", value=2500)
    down1 = st.number_input("Downpayment ($)", key="d1", value=60000)
with col2:
    exp1 = st.number_input("Annual Expenses ($)", key="e1", value=8000)
    loc1 = st.text_input("Location", key="l1", value="Austin, TX")
    sqft1 = st.number_input("Size (sqft)", key="s1", value=1200)


with st.expander("Compare With Property #2"):
    col3, col4 = st.columns(2)
    with col3:
        price2 = st.number_input("Price ($)", key="p2", value=280000)
        rent2 = st.number_input("Expected Rent ($/mo)", key="r2", value=2400)
        down2 = st.number_input("Downpayment ($)", key="d2", value=56000)
    with col4:
        exp2 = st.number_input("Annual Expenses ($)", key="e2", value=7500)
        loc2 = st.text_input("Location", key="l2", value="Tulsa, OK")
        sqft2 = st.number_input("Size (sqft)", key="s2", value=1100)

if st.button("Run Analysis"):
    result1 = real_estate_analysis(price1, rent1, exp1, down1, loc1, sqft1)
    result2 = real_estate_analysis(price2, rent2, exp2, down2, loc2, sqft2)

    st.success("✅ Analysis Complete!")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📍 Property 1 Results")
        for k, v in result1.items():
            st.write(f"**{k}**: {v}")
    with col2:
        st.subheader("📍 Property 2 Results")
        for k, v in result2.items():
            st.write(f"**{k}**: {v}")

    
    if "history" not in st.session_state:
        st.session_state["history"] = []
    st.session_state["history"].append(result1)

    
    pdf = generate_pdf(result1)
    st.download_button("📄 Download PDF Report for Property 1", data=pdf, file_name="investment_report.pdf")


st.subheader("📁 Upload CSV of Properties")
csv_file = st.file_uploader("Upload CSV", type="csv")
if csv_file:
    df = pd.read_csv(csv_file)
    st.write("Uploaded Data:", df)
    st.subheader("📊 Analysis Results")
    for index, row in df.iterrows():
        res = real_estate_analysis(
            row["price"], row["expected_rent"], row["annual_expenses"],
            row["downpayment"], row["location"], row["sqft"]
        )
        st.write(f"**Property {index+1}:**")
        st.json(res)


st.subheader("📧 Stay Connected")
with st.form("contact_form 1"):
    email = st.text_input("Enter your email to get reports or updates")
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.success("Thanks! We'll be in touch via email.")


if st.button("📜 Show Past Property Analyses"):
    if "history" in st.session_state:
        for i, h in enumerate(st.session_state["history"]):
            st.write(f"🔹 Past Analysis #{i+1}:")
            st.json(h)
    else:
        st.info("No past analysis found yet.")
        st.header("📬 Contact Me")

with st.form(key='contact_form 2'):
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")
    submit_button = st.form_submit_button("Submit")

    if submit_button:
        if email and message:
            st.success("✅ Thanks for reaching out! I'll get back to you soon.")
            # (Optional) You can save this data later or send via email
        else:
            st.error("❗ Please fill in both email and message fields.")



