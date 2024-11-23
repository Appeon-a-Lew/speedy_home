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

# Profile button at the top of the sidebar
st.sidebar.markdown("### 👤 Profile")
if st.sidebar.button("Go to Profile"):
    st.session_state["current_page"] = "Profile"
    st.experimental_rerun()

# Add a divider for better organization
st.sidebar.markdown("---")

# Helper function for page navigation
def set_page(page_name):
    st.session_state["current_page"] = page_name
    st.experimental_rerun()


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
    st.session_state["user_type"] = None
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = {
        "email": "",
        "name": "",
        "surname": "",
        "phone": "",
        "address": "",
        "age": "",
        "job": "",
    }




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

    if st.button("Ask AI Chat Assistant"):
        set_page("AI Chat Assistant")

    if st.button("FAQ"):
        set_page("FAQ")


# Profile Page
def profile_page():
    st.title("Profile")
    st.markdown(
        f"""
        <div style="background-color: #b7d7de; padding: 15px; border-radius: 5px;">
            <h2 style="margin: 0;">Edit Your Profile</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.session_state["step"] = 1
    st.session_state["user_type"] = None

    # User profile form
    user_profile = st.session_state["user_profile"]
    user_profile["email"] = st.text_input("Email", user_profile["email"])
    user_profile["name"] = st.text_input("Name", user_profile["name"])
    user_profile["surname"] = st.text_input("Surname", user_profile["surname"])
    user_profile["phone"] = st.text_input("Phone Number", user_profile["phone"])
    user_profile["address"] = st.text_input("Current Address", user_profile["address"])
    user_profile["age"] = st.selectbox("Age", range(18, 101),
        index=(user_profile["age"] - 18) if isinstance(user_profile["age"], int) else 0
    )
    user_profile["job"] = st.selectbox(
        "Are you a student or a professional?",
        ["", "Student", "Professional"],
        index=["", "Student", "Professional"].index(user_profile["job"]),
    )

    # Save button
    if st.button("Save Profile"):
        st.success("Profile updated successfully!")
        st.session_state["user_profile"] = user_profile

    if st.button("Open Chat"):
        set_page("Chat")

    # Button for landlords to offer a house
    if st.button("Offer a House"):
        st.session_state["current_page"] = "Offer a House"
        st.experimental_rerun()

    # Back button
    if st.button("Back to Home"):
        st.session_state["current_page"] = "Home"
        st.experimental_rerun()

# Placeholder for Offer a House Page
def offer_a_house_page():
    st.title("Offer a House")
    st.markdown("This feature is coming soon!")
    st.session_state["step"] = 1
    st.session_state["user_type"] = None

# Chat Page
def chat_page():
    st.title("Chat")
    st.markdown("Send messages to other users.")

    # Select recipient (hardcoded user list for demo purposes)
    recipients = ["John Doe", "Jane Smith", "Alex Brown"]
    recipient = st.selectbox("Select recipient", recipients)

    # Message input
    message = st.text_area("Type your message")

    # Send button
    if st.button("Send"):
        if recipient and message:
            # Save the message in session state
            st.session_state["chat_messages"].append({
                "recipient": recipient,
                "message": message,
                "timestamp": "Just now",  # Mock timestamp
            })
            st.success("Message sent!")
        else:
            st.error("Please select a recipient and type a message.")

    # Display chat history for the selected recipient
    st.markdown(f"### Chat History with {recipient}")
    messages = [
        msg for msg in st.session_state["chat_messages"]
        if msg["recipient"] == recipient
    ]

    # Better UI for chat history
    if messages:
        for msg in messages:
            st.markdown(
                f"""
                <div style="margin-bottom: 10px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background-color: #b7d7de;">
                    <strong>{recipient}</strong> <span style="font-size: 0.8em; color: #555;">({msg['timestamp']})</span>
                    <div style="margin-top: 5px;">{msg['message']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.write("No messages with this recipient yet.")

    # Back to Profile button
    if st.button("Back to Profile"):
        set_page("Profile")



def ai_chat_assistant_page():
    st.title("AI Chat Assistant")
    st.session_state["step"] = 1
    st.session_state["user_type"] = None
    st.markdown("This feature is coming soon! Stay tuned.")
    if st.button("Back to Home"):
        set_page("Home")

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

def faq_page():
    st.title("Frequently Asked Questions (FAQ)")
    st.markdown("Find answers to common questions below.")
    st.session_state["step"] = 1
    st.session_state["user_type"] = None

    # Search box
    query = st.text_input("Search FAQs", "").lower()

    # FAQ data
    faqs = {
        "General": [
            {"question": "What is this platform for?", "answer": "This platform helps you navigate the housing market in Germany with tools and guides tailored to your needs."},
            {"question": "Who can use this platform?", "answer": "Anyone looking for housing in Germany, including professionals, students, and families."},
        ],
        "Housing Terms": [
            {"question": "What is a mortgage?", "answer": "A mortgage is a loan used to purchase a property, secured against the property itself."},
            {"question": "What is 'Vorfälligkeitsentschädigung'?", "answer": "It is a prepayment penalty charged by banks if you pay off your loan early."},
        ],
        "Platform Features": [
            {"question": "How do I edit my profile?", "answer": "Go to the Profile page from the sidebar or click the Profile button at the top of the sidebar."},
            {"question": "How do I use the Step-by-Step Guide?", "answer": "Navigate to the Step-by-Step Guide page and follow the prompts tailored to your profile."},
        ],
    }

    # Display FAQs dynamically based on search query
    for category, items in faqs.items():
        filtered_items = [item for item in items if query in item["question"].lower()]
        if filtered_items:
            st.subheader(category)
            for item in filtered_items:
                with st.expander(item["question"]):
                    st.write(item["answer"])

    # If no results match the query
    if query and all(not [item for item in items if query in item["question"].lower()] for items in faqs.values()):
        st.warning("No FAQs found matching your search. Try a different query.")



# Create a dictionary of pages for easy management
pages = {
    "Home": home_page,
    "Step-by-Step Guide": step_by_step_guide,
    "AI Chat Assistant": ai_chat_assistant_page,
    "Financial Tools": financial_tools,
    "Smart Recommendations": smart_recommendations,
    "Location Visualizer": location_visualizer,
    "Quiz": quiz,
    "Profile": profile_page,
    "Offer a House": offer_a_house_page,
    "FAQ": faq_page,
    "Chat": chat_page,

}

# Selectbox for navigation
page_selection = st.sidebar.selectbox("Select a page", options=list(pages.keys()), index=list(pages.keys()).index(st.session_state["current_page"]))

# Update session state if the selectbox changes
if page_selection != st.session_state["current_page"]:
    set_page(page_selection)

# Render the current page
pages[st.session_state["current_page"]]()