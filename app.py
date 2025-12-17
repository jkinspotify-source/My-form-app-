import streamlit as st

st.title("Personal Details Form 💪")

st.write("Please enter your details below:")

name = st.text_input("Name", placeholder="Type your name here")
age = st.text_input("Age", placeholder="Type your age here (e.g., 39)")
weight = st.text_input("Weight (kg)", placeholder="Type your weight here (e.g., 70)")

if st.button("Submit", type="primary"):
    try:
        age_num = int(age)
        weight_num = float(weight)
        st.success(f"Hello {name}! 👋")
        st.write(f"You are {age_num} years young and full of energy!")
        st.write(f"Your weight is {weight_num} kg")
        st.write(f"Next year you'll be {age_num + 1} — keep rocking! 🚀")
    except:
        st.error("Please enter valid numbers for age and weight!")
