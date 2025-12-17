import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import requests
from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

st.title("🌟 BMI Calculator App 💪")

st.write("Enter your details to get your BMI + personalized tips! Your data is saved securely.")

name = st.text_input("Full Name", placeholder="Your full name")
dob = st.date_input("Date of Birth", min_value=datetime(1900, 1, 1), max_value=datetime.today())
email = st.text_input("Email Address", placeholder="example@gmail.com")
phone = st.text_input("Phone (with country code)", placeholder="+91 9876543210")
age = st.text_input("Age (optional)", placeholder="e.g., 39")
height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=70.0)

if st.button("Calculate My BMI! 🚀", type="primary"):
    if not name or not email or not phone:
        st.error("Name, Email, and Phone are required!")
    else:
        try:
            height_m = height_cm / 100
            bmi = round(weight / (height_m ** 2), 1)

            # BMI Category
            if bmi < 18.5:
                category = "Underweight 🙁"
                tip = "Time to add some healthy calories! Try nuts, avocados, and strength training. 🥜"
            elif bmi < 25:
                category = "Normal Weight 🎉"
                tip = "Awesome! Keep up the balanced diet and exercise. You're on fire! 🔥"
            elif bmi < 30:
                category = "Overweight ⚠️"
                tip = "Small changes add up—try walking more and portion control. You've got this! 🏃"
            else:
                category = "Obese 😔"
                tip = "Focus on sustainable habits. Consult a doctor for personalized guidance. 💙"

            # Fun effects
            st.balloons()
            lottie = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")  # Fun hello/fitness animation
            if lottie:
                st_lottie(lottie, height=200)

            st.success(f"Hello {name}! Your BMI is **{bmi}** → {category}")
            st.info(tip)
            st.write(f"Height: {height_cm} cm | Weight: {weight} kg")
            if age:
                st.write(f"Age: {age} years young – next year even stronger! 🚀")

            # Save to Google Sheets
            conn = st.connection("gsheets",url=st.secrets[GSHEETS_URL])
            try:
                existing = conn.read()
            except:
                existing = pd.DataFrame()

            new_row = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Name": name,
                "DOB": dob.strftime("%Y-%m-%d"),
                "Email": email,
                "Phone": phone,
                "Age": age or "",
                "Height (cm)": height_cm,
                "Weight (kg)": weight,
                "BMI": bmi
            }])
            updated = pd.concat([existing, new_row], ignore_index=True)
            conn.update(data=updated)

            st.success("Your details & BMI saved to sheet! Thank you 📊")

        except Exception as e:
            st.error("Enter valid height/weight numbers!")

st.caption("Share this app & help others track fitness! Made with ❤️ by you.")
