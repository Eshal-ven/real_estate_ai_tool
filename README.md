# 🏡 Real Estate ROI Analyzer — AI-Powered Property Investment Tool

Analyze, visualize, and export your property investment data using this powerful, AI-driven real estate app. Built with Python and Streamlit, this tool helps investors make smarter property decisions by combining real-time metrics, interactive maps, and PDF reporting — all in one place.

🎯 Ideal for real estate investors, brokers, data analysts, landlords, and property managers.

🔗 **Live Demo**: [Click to Launch App](https://realestateaitool.streamlit.app)

📄 **Downloadable PDF Report**: Generate, preview, and export a full property investment report with one click.

---

## ✨ Key Features

### 📊 Smart Investment Calculator
- **ROI (Return on Investment)**
- **Cap Rate (%)**
- **Cash-on-Cash Return**
- Smart advice engine: **Buy**, **Hold**, or **Avoid**

### 🧠 AI-Enhanced Market Estimations
- Estimate **price per sqft** and **rent per sqft** based on **city** or **ZIP code**
- Automated **Demand Score** and **Risk Assessment** for smarter investment
- Regional metrics to help compare local market trends

### 📍 Interactive Map (New!)
- **Folium-powered map** integration using `streamlit-folium`
- View properties directly on a **clickable, zoomable map**
- See pricing, ROI, and rental potential by hovering or clicking on map markers
- Supports **custom coordinates**, ZIP codes, and city-based search

### 📌 Geospatial Analysis
- Visualize neighborhood-level data using lat/long or region-based lookup
- Spot profitable zones with **color-coded map overlays**
- Lay groundwork for future features like **heatmaps**, **school zones**, and **crime data overlays**

### 🧾 PDF Report Generator
- One-click export of complete investment analysis
- Fully formatted and **client-ready PDF reports**
- Great for sharing insights with partners, agents, or clients

### 🖥️ User-Friendly Streamlit Interface
- Clean, mobile-responsive UI
- Real-time feedback on all inputs
- Error handling, smart defaults, and beginner-friendly tooltips

---

## 📷 Screenshots

> _(Coming Soon)_ Add these after deployment:
- Investment Summary View  
- Interactive Map with Property Pins  
- Sample PDF Export  

---

## 🔧 Tech Stack

| Tool | Purpose |
|------|---------|
| **Python** | Core language |
| **Streamlit** | UI framework |
| **Matplotlib** | Graph and data visualization |
| **FPDF** | PDF generation |
| **Folium** | Interactive mapping |
| **streamlit-folium** | Streamlit + Folium integration |
| **Base64**, **BytesIO** | Image and PDF rendering in-browser |
| **NumPy & Pandas** | (Optional) For future ML & analytics |
| **OpenAI API** | (Upcoming) Smart comparison and market prediction engine |

---

## 🚀 Upcoming Features

- 🔮 **AI Price & Rent Predictions** using ML
- 📈 Compare multiple properties side-by-side
- 🌐 Add real estate heatmaps (based on ROI, demand, risk)
- 🧭 Click-to-analyze map tools
- 🏫 School zone overlays, crime stats, and transport access mapping
- 📉 Market trend tracking by ZIP/region

---

## 💰 Monetization & Use Cases

- ✅ Use as a **freemium tool** and upsell PDF reports or advanced insights
- ✅ License to **real estate agents or broker platforms**
- ✅ Integrate with your **property listing website**
- ✅ Monetize with **affiliate links**, **email capture**, or **API plans**

---

## 🙌 Contributing

We welcome contributions and feedback. Fork this repo, suggest ideas, or build with us!

---

## 📬 Contact

Have feedback or business inquiries?

📧 Email: eshlfatimah@gmail.com  
🔗Linkedin:  www.linkedin.com/in/eshal-fatima-


---

# Step 1: Clone the repo
git clone https://github.com/eshal-ven/real_estate_ai_tool.git
cd real_estate_ai_tool

# Step 2: Install required libraries
pip install -r requirements.txt

# Step 3: Run the Streamlit app
streamlit run app.py


