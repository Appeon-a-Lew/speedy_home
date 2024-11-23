import streamlit as st
from googletrans import Translator
import numpy as np
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Initialize translator
translator = Translator()

# App Title
st.title("Multilingual Housing Assistant")
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page", ["Home", "Step-by-Step Guide", "Financial Tools", "Smart Recommendations", "Location Visualizer", "Quiz"])

# Multilingual Feature
def translate_text():
    language = st.selectbox("Select Language", ["English", "German", "Spanish"])
    input_text = st.text_input("Enter text to translate:")
    if input_text:
        translation = translator.translate(input_text, dest=language[:2].lower())
        st.write(f"Translation: {translation.text}")

# Step-by-Step Guide
def step_by_step_guide():
    st.header("Step-by-Step Guide")
    tab1, tab2, tab3 = st.tabs(["Professional", "Student", "Family"])

    with tab1:
        st.subheader("Guide for Professionals")
        st.write("1. Understand your budget")
        st.write("2. Learn about mortgages")
        st.write("3. Explore available properties")

    with tab2:
        st.subheader("Guide for Students")
        st.write("1. Search for shared housing")
        st.write("2. Understand tenant rights")
        st.write("3. Apply for student council housing")

    with tab3:
        st.subheader("Guide for Families")
        st.write("1. Plan for future needs (schools, childcare)")
        st.write("2. Explore family-friendly neighborhoods")
        st.write("3. Research mortgage options")

# Financial Tools
def financial_tools():
    st.header("Financial Planning Tools: Mortgage Calculator")

    # Inputs
    principal = st.number_input("Loan Amount (€)", value=100000)
    rate = st.number_input("Interest Rate (%)", value=3.0)
    years = st.number_input("Loan Term (Years)", value=20)

    if st.button("Calculate Monthly Payment"):
        r = rate / 100 / 12
        n = years * 12
        monthly_payment = (principal * r * (1 + r)**n) / ((1 + r)**n - 1)
        st.write(f"Monthly Payment: €{monthly_payment:.2f}")

        # Plot Payment Breakdown
        interest = np.cumsum([principal * r * (1 + r)**i / ((1 + r)**n - 1) for i in range(1, n + 1)])
        principal_paid = np.cumsum([monthly_payment - i for i in interest])
        plt.plot(range(n), interest, label="Interest")
        plt.plot(range(n), principal_paid, label="Principal")
        plt.legend()
        st.pyplot(plt)

# Smart Recommendations
def smart_recommendations():
    st.header("AI-Based Shared Housing Matching")

    # Dummy preferences data
    preferences = pd.DataFrame({
        'Quiet': [1, 0, 1],
        'Social': [0, 1, 1],
        'Pets': [1, 1, 0]
    }, index=["User A", "User B", "User C"])

    # Collect user input
    st.write("Answer a few questions to find the best match:")
    quiet = st.radio("Are you quiet?", [1, 0])
    social = st.radio("Are you social?", [1, 0])
    pets = st.radio("Do you like pets?", [1, 0])

    # AI Recommendation
    user_vector = [[quiet, social, pets]]
    similarities = cosine_similarity(user_vector, preferences.values)
    match_index = similarities[0].argmax()
    st.write(f"Best Match: {preferences.index[match_index]}")

# Location Visualizer
def location_visualizer():
    st.header("Interactive Location Visualizer")

    # Create map
    map = folium.Map(location=[48.1351, 11.582], zoom_start=12)
    folium.Marker([48.1351, 11.582], popup="Munich Center").add_to(map)

    # Display map
    st_folium(map)

# Quiz
def quiz():
    st.header("Gamified Financial Education Quiz")

    question = st.radio("What is the maximum rental deposit allowed by German law?", ["2 months", "3 months", "4 months"])
    if st.button("Submit Answer"):
        if question == "3 months":
            st.success("Correct!")
        else:
            st.error("Wrong answer. The correct answer is '3 months.'")

# Page Routing
if page == "Home":
    st.subheader("Welcome to the Multilingual Housing Assistant!")
    translate_text()
elif page == "Step-by-Step Guide":
    step_by_step_guide()
elif page == "Financial Tools":
    financial_tools()
elif page == "Smart Recommendations":
    smart_recommendations()
elif page == "Location Visualizer":
    location_visualizer()
elif page == "Quiz":
    quiz()

