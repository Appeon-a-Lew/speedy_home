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

# Inject custom CSS for sidebar
def set_sidebar_style():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #b7d7de;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
# Call the function to apply the style
set_sidebar_style()



# Helper function for page navigation
def set_page(page_name):
    st.session_state["current_page"] = page_name

# Helper function to update the current step
def next_step(step):
    st.session_state["current_step"] = step

# Helper function for setting up the user type
def set_user_type(user_type):
    st.session_state["user_type"] = user_type
    st.session_state["step"] = 2



# Initialize session state for navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"
if "step" not in st.session_state:
    st.session_state["step"] = 1
if "user_type" not in st.session_state:
    st.session_state["user_type"] = None # Start at step 1


# Define pages
def home_page():
    st.title("Welcome to the Multilingual Housing Assistant")
    st.markdown(
        """
        **Our Mission**: Helping you navigate the German housing market with ease.  
        **What We Offer**:
        - Step-by-step guides tailored to your needs.
        - Smart financial tools and recommendations.
        - An AI assistant to answer all your housing questions.
        """)
    st.session_state["step"] = 1
    st.session_state["user_type"] = None
    # Buttons for navigation
    if st.button("Get Step-by-Step Guide"):
        set_page("Step-by-Step Guide")
        st.experimental_rerun()

    if st.button("Ask AI Chat Assistant"):
        set_page("AI Chat Assistant")
        st.experimental_rerun()


def ai_chat_assistant_page():
    st.title("AI Chat Assistant")
    st.session_state["step"] = 1
    st.session_state["user_type"] = None
    st.markdown("This feature is coming soon! Stay tuned.")
    if st.button("Back to Home"):
        set_page("Home")
        st.experimental_rerun()

# Step-by-Step Guide
def step_by_step_guide():
    st.title("Step-by-Step Guide")
    # Step 1: Ask user type

    if st.session_state["step"] == 1:
        st.header("What best describes you?")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Professional"):
                set_user_type("Professional")
                st.experimental_rerun()
        with col2:
            if st.button("Student"):
                set_user_type("Student")
                st.experimental_rerun()
        with col3:
            if st.button("Family"):
                set_user_type("Family")
                st.experimental_rerun()

    # Step 2: Tailored flow based on user type
    elif st.session_state["step"] == 2:
        user_type = st.session_state["user_type"]
        st.subheader(f"You selected: {user_type}")

        if user_type == "Professional":
            professional_flow()
        elif user_type == "Student":
            student_flow()
        elif user_type == "Family":
            family_flow()

        # Add a "Back" button
        if st.button("Back"):
            st.session_state["step"] = 1
            st.session_state["user_type"] = None
            st.experimental_rerun()


# Professional Flow
def professional_flow():
    st.title("Guide for Professionals")
    st.write("### Step 1: Understand Your Budget")
    budget = st.slider("Select your budget range (€)", 500, 5000, (1000, 3000))
    st.write(f"You selected: €{budget[0]} to €{budget[1]}")

    if st.button("Next"):
        st.write("### Step 2: Learn About Mortgages")
        st.markdown("Navigate to the Financial Tools page to explore mortgage calculators.")
        if st.button("Go to Financial Tools"):
            set_page("Financial Tools")
            st.experimental_rerun()


# Student Flow
def student_flow():
    st.title("Guide for Students")
    st.write("### Step 1: Choose Housing Type")
    housing_type = st.radio("Select your housing preference:", ["Normal Housing", "Shared Housing"])

    if housing_type == "Shared Housing":
        st.write("### Step 2: Set Your Preferences")
        max_people = st.slider("Maximum number of people:", 2, 6, 4)
        same_sex = st.checkbox("Same-sex preference")
        st.write(f"Preferences: Max {max_people} people, Same-sex: {same_sex}")
        if st.button("Show Matches"):
            st.write("### Mock Results")
            st.markdown("- **Roommate 1:** John Doe, Age 25, Male")
            st.markdown("- **Roommate 2:** Jane Smith, Age 22, Female")

    if st.button("Next"):
        st.write("### Learn Tenant Rights")
        st.markdown("Here’s a quick guide to your rights as a tenant...")


# Family Flow
def family_flow():
    st.title("Guide for Families")
    st.write("### Step 1: Plan Around Family Needs")
    st.write("Select features important to your family:")
    schools = st.checkbox("Proximity to schools")
    childcare = st.checkbox("Proximity to childcare")
    parks = st.checkbox("Proximity to parks")
    st.write("Selected preferences:", "Schools" if schools else "", "Childcare" if childcare else "",
             "Parks" if parks else "")

    if st.button("Explore Properties"):
        st.write("### Explore Family-Friendly Properties")
        st.markdown("- **Property 1:** 3-bedroom, near school and park")
        st.markdown("- **Property 2:** 2-bedroom, close to childcare and shopping")


# Financial Tools
def financial_tools():
    st.title("Financial Tools")
    st.header("Financial Planning Tools: Mortgage Calculator")
    st.session_state["step"] = 1
    st.session_state["user_type"] = None

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
    st.session_state["step"] = 1
    st.session_state["user_type"] = None
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
    st.session_state["step"] = 1
    st.session_state["user_type"] = None
    # Create map
    map = folium.Map(location=[48.1351, 11.582], zoom_start=12)
    folium.Marker([48.1351, 11.582], popup="Munich Center").add_to(map)

    # Display map
    st_folium(map)

# Quiz
def quiz():
    st.header("Gamified Financial Education Quiz")
    st.session_state["step"] = 1
    st.session_state["user_type"] = None
    question = st.radio("What is the maximum rental deposit allowed by German law?", ["2 months", "3 months", "4 months"])
    if st.button("Submit Answer"):
        if question == "3 months":
            st.success("Correct!")
        else:
            st.error("Wrong answer. The correct answer is '3 months.'")


# Create a dictionary of pages for easy management
pages = {
    "Home": home_page,
    "Step-by-Step Guide": step_by_step_guide,
    "AI Chat Assistant": ai_chat_assistant_page,
    "Financial Tools": financial_tools,
    "Smart Recommendations": smart_recommendations,
    "Location Visualizer": location_visualizer,
    "Quiz": quiz,

}

# Selectbox for navigation
page_selection = st.sidebar.selectbox("Select a page", options=list(pages.keys()), index=list(pages.keys()).index(st.session_state["current_page"]))

# Update session state if the selectbox changes
if page_selection != st.session_state["current_page"]:
    set_page(page_selection)
    st.experimental_rerun()  # Force immediate page update

# Render the current page
pages[st.session_state["current_page"]]()

# Render the current page
## Define translations for simplicity


# if st.session_state["current_page"] == "Home":
#     home_page()translations = {
#     "English": {
#         "welcome": "Welcome to the Step-by-Step Guide!",
#         "select_language": "Step 1: Select your language",
#         "select_user_type": "Step 2: Who are you?",
#         "professional": "Professional",
#         "student": "Student",
#         "family": "Family",
#     },
#     "German": {
#         "welcome": "Willkommen zum Schritt-für-Schritt-Leitfaden!",
#         "select_language": "Schritt 1: Wählen Sie Ihre Sprache",
#         "select_user_type": "Schritt 2: Wer sind Sie?",
#         "professional": "Berufstätiger",
#         "student": "Student",
#         "family": "Familie",
#     },
#     "Spanish": {
#         "welcome": "¡Bienvenido a la Guía Paso a Paso!",
#         "select_language": "Paso 1: Seleccione su idioma",
#         "select_user_type": "Paso 2: ¿Quién eres tú?",
#         "professional": "Profesional",
#         "student": "Estudiante",
#         "family": "Familia",
#     },
# }
# elif st.session_state["current_page"] == "Step-by-Step Guide":
#     step_by_step_guide()
# elif st.session_state["current_page"] == "AI Chat Assistant":
#     ai_chat_assistant_page()
# elif st.session_state["current_page"] == "Financial Tools":
#     financial_tools()
# elif st.session_state["current_page"] == "Smart Recommendations":
#     smart_recommendations()
# elif st.session_state["current_page"] == "Location Visualizer":
#     location_visualizer()
# elif st.session_state["current_page"] == "Quiz":
#     quiz()def step_by_step_guide():
#     st.header("Step-by-Step Guide")
#     tab1, tab2, tab3 = st.tabs(["Professional", "Student", "Family"])
#
#     with tab1:
#         st.subheader("Guide for Professionals")
#         st.write("1. Understand your budget")
#         st.write("2. Learn about mortgages")
#         st.write("3. Explore available properties")
#
#     with tab2:
#         st.subheader("Guide for Students")
#         st.write("1. Search for shared housing")
#         st.write("2. Understand tenant rights")
#         st.write("3. Apply for student council housing")
#
#     with tab3:
#         st.subheader("Guide for Families")
#         st.write("1. Plan for future needs (schools, childcare)")
#         st.write("2. Explore family-friendly neighborhoods")
#         st.write("3. Research mortgage options")


# Page Routing
# if page == "Home":
#    st.subheader("Welcome to the Multilingual Housing Assistant!")
#    translate_text()
#elif page == "Step-by-Step Guide":
#    step_by_step_guide()
#elif page == "Financial Tools":
#    financial_tools()
#elif page == "Smart Recommendations":
#    smart_recommendations()
#elif page == "Location Visualizer":
#    location_visualizer()
#elif page == "Quiz":
#    quiz()
#elif page == "AI Chat Assistant":
#    ai_chat_assistant_page()
# """
