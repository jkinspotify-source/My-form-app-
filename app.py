import streamlit as st
import pandas as pd
from datetime import datetime

# --- Google Sheets Connection (you'll set up secrets next) ---
@st.cache_resource
def get_gsheets_connection():
    return st.connection("gsheets", type="gsheets")

st.title("Your BMI Monitor 💪")

st.write("Please fill in your details below:")

name = st.text_input("Full Name", placeholder="Type your full name here")
dob = st.date_input("Date of Birth", min_value=datetime(1950, 1, 1), max_value=datetime.today())
email = st.text_input("Email Address", placeholder="example@gmail.com")
phone = st.text_input("Phone Number (with country code)", placeholder="+91 9876543210")
age = st.text_input("Age", placeholder="e.g., 39")
weight =  st.text_input("Weight (kg)", placeholder="e.g., 70")

if st.button("Submit", type="primary"):
    # Basic validation
    if not name or not email or not phone:
        st.error("⚠️ Name, Email, and Phone are required!")
    else:
        try:
            age_num = int(age)
            weight_num = float(weight)

            # Save to Google Sheets
            conn = get_gsheets_connection()
            # Read existing data (or create empty if first time)
            try:
                existing_data = conn.read()
            except:
                existing_data = pd.DataFrame(columns=["Timestamp", "Name", "Date of Birth", "Email", "Phone", "Age", "Weight (kg)"])

            # New submission row
            new_row = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Name": name,
                "Date of Birth": dob.strftime("%Y-%m-%d"),
                "Email": email,
                "Phone": phone,
                "Age": age_num,
                "Weight (kg)": weight_num
            }])

            # Append and update sheet
            updated_data = pd.concat([existing_data, new_row], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_data)

            # Success message
            st.success(f"Thank you {name}! Your details have been saved successfully! 👋")
            st.write(f"Date of Birth: {dob.strftime('%d-%m-%Y')}")
            st.write(f"Email: {email}")
            st.write(f"Phone: {phone}")
            st.write(f"Age: {age_num} years young")
            st.write(f"Weight: {weight_num} kg")
            st.write(f"Next year you'll be {age_num + 1} — keep rocking! 🚀")

        except ValueError:
            st.error("Please enter valid numbers for Age and Weight!")

st.caption("Your data is securely saved. Thank you! 💙")
