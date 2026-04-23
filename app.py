import streamlit as st
import pandas as pd
import os
crop_df = pd.read_csv("Crop_recommendation.csv")
crop_df.dropna(inplace=True)
# Page config
st.set_page_config(page_title="CropCare", layout="wide")
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)
st.title("🌱 CropCare Dashboard")

# File setup
FILE = "data.csv"

# Create file if it doesn't exist
if not os.path.exists(FILE):
    df = pd.DataFrame(columns=["crop", "health", "yield"])
    df.to_csv(FILE, index=False)

# Load data
data = pd.read_csv(FILE)

# Sidebar menu
menu = st.radio(
    "Navigation",
    ["Dashboard", "Crop Recommendation", "Add Crop Data", "Disease Detection", "Image Upload", "Analytics", "Alerts"],
    horizontal=True
)
if menu == "Crop Recommendation":
    st.subheader("🌱 Crop Recommendation System")

    n = st.number_input("Nitrogen")
    p = st.number_input("Phosphorus")
    k = st.number_input("Potassium")
    temp = st.number_input("Temperature")
    humidity = st.number_input("Humidity")
    ph = st.number_input("pH")
    rainfall = st.number_input("Rainfall")

    if st.button("Recommend Crop"):
        filtered = crop_df[crop_df["temperature"] <= temp]

        st.success("Recommended Crops:")
        st.write(filtered["label"].unique()[:5])
uploaded_file = st.sidebar.file_uploader(
    "Upload Crop Dataset (CSV)",
    type=["csv"]
)

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.subheader("📊 Crop Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("🌾 Total Crops", len(data))
    col2.metric("📈 Avg Yield", int(data["yield"].mean()) if len(data) > 0 else 0)

    healthy = len(data[data["health"] == "Good"])
    col3.metric("✅ Healthy Crops", healthy)

    st.markdown("### 📋 Crop Data")
    st.dataframe(data, use_container_width=True)

# ---------------- ADD DATA ----------------
elif menu == "Add Crop Data":
    st.subheader("➕ Add New Crop")

    col1, col2 = st.columns(2)

    crop = col1.text_input("Crop Name")
    health = col1.selectbox("Health Status", ["Good", "Moderate", "Bad"])
    yield_val = col2.number_input("Yield Estimate", min_value=0)

    if st.button("Add Crop"):
        if crop.strip() == "":
            st.warning("Please enter crop name")
        else:
            new_data = pd.DataFrame({
                "crop": [crop],
                "health": [health],
                "yield": [yield_val]
            })

            new_data.to_csv(FILE, mode='a', header=False, index=False)
            st.success("✅ Crop data added successfully!")
            st.rerun()

# ---------------- ANALYTICS ----------------
elif menu == "Analytics":
    st.subheader("📈 Crop Analytics")

    if len(data) > 0:
        col1, col2 = st.columns(2)

        col1.bar_chart(data.set_index("crop")["yield"])
        col2.bar_chart(data["health"].value_counts())
    else:
        st.info("No data available")

# ---------------- ALERTS ----------------
elif menu == "Alerts":
    st.subheader("⚠️ Alerts")

    if len(data) == 0:
        st.info("No data available")
    else:
        for _, row in data.iterrows():
            if row["health"] == "Bad":
                st.error(f"{row['crop']} needs immediate attention!")
            elif row["health"] == "Moderate":
                st.warning(f"{row['crop']} condition is average")
            else:
                st.success(f"{row['crop']} is healthy")

elif menu == "Image Upload":
    st.subheader("📸 Crop Image Analysis")

    uploaded_image = st.file_uploader("Upload Crop Image", type=["jpg", "png", "jpeg"])

    if uploaded_image:
        col1, col2 = st.columns(2)

        col1.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        col2.info("Analyzing image...")
        col2.success("Possible Issue: Leaf infection (demo)")
elif menu == "Disease Detection":
    st.subheader("🌾 Disease Detection")

    selected_crop = st.selectbox("Select Crop", data["crop"].unique())
    selected_health = st.selectbox("Select Health", data["health"].unique())

    if st.button("Check Disease"):
        result = data[
            (data["crop"] == selected_crop) &
            (data["health"] == selected_health)
        ]

        if not result.empty:
            st.success("Disease Info:")
            st.write("Possible issue based on health:", selected_health)
        else:
            st.warning("No matching record found")