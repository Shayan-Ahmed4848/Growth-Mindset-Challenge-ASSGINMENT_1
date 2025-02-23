import streamlit as st
import pandas as pd
import numpy as np
import json
from io import BytesIO


st.title("....Growth Mindset Challenge....")

# Initialize session state for challenges and quotes
if "challenge" not in st.session_state:
    st.session_state.challenge = None
if "quote" not in st.session_state:
    st.session_state.quote = None

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Choose a Section", ["Home", "Data Manager", "Data Cleaner", "Format Converter", "Challenges", "Motivation"])

# Home Page
if page == "Home":
    # Custom CSS for styling
    st.markdown(
        """
        <style>
        .header {
            font-size: 40px;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
            padding: 20px;
        }
        .subheader {
            font-size: 24px;
            color: #FF5733;
            text-align: center;
            padding: 10px;
        }
        .assignment-details {
            background-color: #F4F4F4;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .motivation {
            font-size: 20px;
            color: #1E90FF;
            text-align: center;
            font-style: italic;
            padding: 10px;
        }
        .footer {
            font-size: 16px;
            color: #777;
            text-align: center;
            padding: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Header Section
    st.markdown('<div class="header"><---Smart Data Processor---></div>', unsafe_allow_html=True)
    st.write("Enhance your skills while processing data with an innovative growth mindset.")
    st.image("pic 1.jpg", use_container_width=True)

    # Assignment Details Section
    st.markdown('<div class="assignment-details">', unsafe_allow_html=True)
    st.markdown("### 📝 Assignment No. 1 (Growth Mindset Challenge)")
    
    # Use columns for better layout
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**👤 Name:** Muhammad Shayan Ahmed")
        st.markdown("**🎫 Roll No:** 00057287")
        st.markdown("**🏛️ Center:** Governor House Karachi")
    with col2:
        st.markdown("**📅 Days / Time:** Tuesday - 07:00 PM - 10:00 PM")
        st.markdown("**📚 Program:** Artificial Intelligence & Machine Learning (Web 3.0 and Metaverse)")
        st.markdown("**📅 Quarter:** 3 (Python)")
    st.markdown('</div>', unsafe_allow_html=True)

    # Motivation Section
    st.markdown('<div class="motivation">🌟 Motivation: Strive for progress, not perfection.</div>', unsafe_allow_html=True)


# 📂 Data Management Panel
elif page == "Data Manager":
    st.header("🛠 Data Management Panel")
    uploaded_file = st.file_uploader("📂 Upload Your File (CSV, XLSX)", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                st.error("Unsupported file format. Please upload a CSV or XLSX file.")
                df = None
            
            if df is not None:
                st.write("📜 Data Table")
                edited_df = st.data_editor(df)
                st.write("🖊 Edit Directly from Table")
                st.dataframe(edited_df)
        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")
    
    # Add New Item
    st.subheader("➕ Add New Item")
    item_name = st.text_input("Item Name")
    price = st.number_input("Price ($)", min_value=0.0)
    detail = st.text_area("Details")
    stock = st.number_input("Stock Quantity", min_value=0)
    store = st.text_input("Store Name")
    if st.button("Add Item"):
        if item_name and store:  # Basic validation
            st.success(f"✅ Item '{item_name}' added successfully!")
        else:
            st.error("Please fill in all required fields.")
    
    # Update Existing Item
    st.subheader("✏️ Update Existing Item")
    update_item = st.text_input("Enter Item Name to Update")
    update_column = st.selectbox("Select Column to Update", ["Name", "Price", "Detail", "Stock", "Store"])
    new_value = st.text_input("Enter New Value")
    if st.button("Update Item"):
        if update_item and new_value:  # Basic validation
            st.success(f"🔄 Item '{update_item}' updated successfully!")
        else:
            st.error("Please provide valid inputs for update.")

# 🧹 Data Cleaning Module
elif page == "Data Cleaner":
    st.header("🧼 Clean Your Dataset")
    uploaded_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("🔍 Preview of Uploaded Data:")
            st.dataframe(df.head())
            
            # Handle Missing Values
            st.subheader("Handle Missing Values")
            if df.isnull().sum().any():
                st.write("⚠️ Missing values detected.")
                if st.checkbox("Remove rows with missing values"):
                    df_cleaned = df.dropna()
                    st.write("✅ Cleaned Dataset (Missing Values Removed):")
                    st.dataframe(df_cleaned.head())
            else:
                st.write("🎉 No missing values found!")
            
            # Normalize Numerical Data
            st.subheader("Normalize Numerical Data")
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                if st.checkbox("Normalize numerical columns"):
                    df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].min()) / (df[numeric_cols].max() - df[numeric_cols].min())
                    st.write("📊 Normalized Data:")
                    st.dataframe(df.head())
            else:
                st.write("No numerical columns found for normalization.")
        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

# 🔄 Format Conversion Module
elif page == "Format Converter":
    st.header("🔄 Convert File Format")
    uploaded_file = st.file_uploader("📂 Upload a CSV file to convert", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            file_format = st.radio("Convert Data to:", ["CSV", "Excel (XLSX)", "JSON"])
            
            if file_format == "CSV":
                csv_data = df.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download CSV", csv_data, file_name="converted_data.csv", mime="text/csv")
            elif file_format == "Excel (XLSX)":
                # Create an in-memory buffer for the Excel file
                output = BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False)
                output.seek(0)
                st.download_button("📥 Download XLSX", output, file_name="converted_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            elif file_format == "JSON":
                json_data = df.to_json(orient="records", indent=4)
                st.download_button("📥 Download JSON", json_data, file_name="converted_data.json", mime="application/json")
        except Exception as e:
            st.error(f"An error occurred while converting the file: {e}")

# 💡 Data Science Challenges
elif page == "Challenges":
    st.header("🎯 Daily Data Science Challenge")
    challenges = [
        "🔍 Write a Python script to clean missing data in a dataset.",
        "📈 Implement a function to normalize numerical columns in a dataset.",
        "📊 Convert a dataset into multiple formats like CSV, JSON, and Excel.",
        "📊 Visualize data distributions using Matplotlib or Seaborn."
    ]
    
    if st.session_state.challenge is None:
        st.session_state.challenge = np.random.choice(challenges)
    
    st.write(f"Today's Challenge: {st.session_state.challenge}")
    
    if st.button("Get Another Challenge"):
        st.session_state.challenge = np.random.choice(challenges)
        st.rerun()

# 💪 Motivational Quotes & Growth Mindset
elif page == "Motivation":
    st.header("💡 Stay Inspired!")
    quotes = [
        "🌱 Mistakes are proof that you are trying.",
        "🚀 Great things never come from comfort zones.",
        "🎯 Strive for progress, not perfection."
    ]
    
    if st.session_state.quote is None:
        st.session_state.quote = np.random.choice(quotes)
    
    st.write(f"Quote of the Day: {st.session_state.quote}")
    
    if st.button("Get Another Quote"):
        st.session_state.quote = np.random.choice(quotes)
        st.rerun()

# Run the app with: streamlit run app.py