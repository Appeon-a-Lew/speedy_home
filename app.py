
import streamlit as st
#import googletrans
import numpy as np
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import bot

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
    st.rerun()

# Add a divider for better organization
st.sidebar.markdown("---")

# Helper function for page navigation
def set_page(page_name):
    st.session_state["current_page"] = page_name
    st.rerun()

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
if "chat_bot" not in st.session_state:
    st.session_state["chat_bot"] = bot.Bot()
if "ai_messages" not in st.session_state:
    st.session_state["ai_messages"] = []
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = {
        "email": "",
        "name": "",
        "surname": "",
        "phone": "",
        "address": "",
        "age": "",
        "job": "",
        "monthly_income": 0,
        "gender": ""
    }

# Define district coordinates
district_centers = {
    'Altstadt-Lehel': [48.1371, 11.5753],
    'Ludwigsvorstadt-Isarvorstadt': [48.1299, 11.5657],
    'Maxvorstadt': [48.1517, 11.5675],
    'Schwabing-West': [48.1597, 11.5542],
    'Au-Haidhausen': [48.1288, 11.5934],
    'Sendling': [48.1115, 11.5465],
    'Sendling-Westpark': [48.1202, 11.5191],
    'Schwanthalerhöhe': [48.1364, 11.5395],
    'Neuhausen-Nymphenburg': [48.1540, 11.5216],
    'Moosach': [48.1742, 11.4985],
    'Milbertshofen-Am Hart': [48.1925, 11.5692],
    'Schwabing-Freimann': [48.1723, 11.5887],
    'Bogenhausen': [48.1530, 11.6097],
    'Berg am Laim': [48.1266, 11.6351],
    'Trudering-Riem': [48.1210, 11.6574],
    'Ramersdorf-Perlach': [48.0988, 11.6229],
    'Obergiesing-Fasangarten': [48.1002, 11.6015],
    'Untergiesing-Harlaching': [48.0986, 11.5799],
    'Thalkirchen-Obersendling-Forstenried-Fürstenried-Solln': [48.0965, 11.5232],
    'Hadern': [48.1148, 11.4837],
    'Pasing-Obermenzing': [48.1446, 11.4623],
    'Aubing-Lochhausen-Langwied': [48.1661, 11.4022],
    'Allach-Untermenzing': [48.1795, 11.4715],
    'Feldmoching-Hasenbergl': [48.1942, 11.5420],
    'Laim': [48.1338, 11.5103],
}
if "homes" not in st.session_state:
    st.session_state["homes"] = []

# Function to generate random coordinates near a district's center
def generate_coordinates(center, num_points, radius=0.01):
    latitudes = np.random.uniform(center[0] - radius, center[0] + radius, num_points)
    longitudes = np.random.uniform(center[1] - radius, center[1] + radius, num_points)
    return latitudes, longitudes

# Generate mock housing data
def generate_mock_data(houses_per_district=40):
    data = {
        'id': [],
        'price': [],
        'transportation': [],
        'shared_living': [],
        'lat': [],
        'lon': [],
        'region': [],
        'address': [],
        'type': [],
        'size': [],
        'preferences': [],
        'proximity_schools': [],
        'proximity_parks': [],
        'owner_name': [],
        'gender': [],
        'is_student': [],
        'current_people': [],
        'max_people': [],
        'same_sex_pref': [],
    }

    preferences_options = ['Students', 'Professionals', 'Families', 'No preference']

    for region, center in district_centers.items():
        lats, lons = generate_coordinates(center, houses_per_district)
        data['id'].extend(range(len(data['id']) + 1, len(data['id']) + houses_per_district + 1))
        data['price'].extend(np.random.randint(500, 3000, houses_per_district))
        data['transportation'].extend(np.random.randint(1, 10, houses_per_district))
        data['shared_living'].extend(np.random.choice([True, False], houses_per_district))
        data['lat'].extend(lats)
        data['lon'].extend(lons)
        data['region'].extend([region] * houses_per_district)
        data['address'].extend([f"{region} Street {i}" for i in range(houses_per_district)])
        data['type'].extend(np.random.choice(['Rent', 'Sale', 'Shared Housing'], houses_per_district))
        data['size'].extend(np.random.randint(30, 200, houses_per_district))
        data['preferences'].extend([np.random.choice(preferences_options, size=np.random.randint(1, len(preferences_options)+1), replace=False).tolist() for _ in range(houses_per_district)])
        data['proximity_schools'].extend(np.random.choice([True, False], houses_per_district))
        data['proximity_parks'].extend(np.random.choice([True, False], houses_per_district))
        data['owner_name'].extend([f"Owner {i}" for i in range(houses_per_district)])
        data['gender'].extend(np.random.choice(['Male', 'Female', 'Divers', None], houses_per_district))
        data['is_student'].extend(np.random.choice([True, False], houses_per_district))
        data['current_people'].extend(np.random.randint(1, 5, houses_per_district))
        data['max_people'].extend(np.random.randint(2, 6, houses_per_district))
        data['same_sex_pref'].extend(np.random.choice(['Yes', 'No'], houses_per_district))

    return pd.DataFrame(data)

if 'houses' not in st.session_state:
    st.session_state['houses'] = generate_mock_data()

# Count houses per district
def count_houses_per_district(houses):
    district_counts = houses['region'].value_counts().reset_index()
    district_counts.columns = ['District', 'Number of Houses']
    return district_counts

# Home Page
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
    user_profile["gender"] = st.multiselect(
            "Gender",
            ["Male", "Female", "Divers"]
        )    
    user_profile["age"] = st.selectbox("Age", range(18, 101),
        index=(user_profile["age"] - 18) if isinstance(user_profile["age"], int) else 0
    )
    user_profile["job"] = st.selectbox(
        "Are you a student or a professional?",
        ["", "Student", "Professional"],
        index=["", "Student", "Professional"].index(user_profile["job"]) if user_profile["job"] in ["", "Student", "Professional"] else 0,
    ) 
    user_profile["monthly_income"] = st.number_input("Monthly Income (€)", min_value=0, value=int(user_profile.get("monthly_income", 0)))

    # Save button
    if st.button("Save Profile"):
        st.success("Profile updated successfully!")
        st.session_state["user_profile"] = user_profile

    if st.button("Open Chat"):
        set_page("Chat")

    # Button for landlords to offer a house
    if st.button("Offer a House"):
        st.session_state["current_page"] = "Offer a House"
        st.rerun()

    # Back button
    if st.button("Back to Home"):
        st.session_state["current_page"] = "Home"
        st.rerun()

# Offer a House Page
def offer_a_house_page():
    st.title("Offer a House")
    st.markdown("Provide details about your property below:")
    st.session_state["step"] = 1
    st.session_state["user_type"] = None

    # Property details form
    property_type = st.selectbox("Is this property for Rent, Sale, or Shared Housing?", ["Rent", "Sale", "Shared Housing"])
    owner_name = st.text_input("Owner Name")
    address = st.text_input("Address")
    size = st.number_input("Size (in sq. meters)", min_value=0)
    price = st.number_input("Price (€)", min_value=0)

    # Proximity details for family-friendly properties
    proximity_schools = st.radio("Is the property close to schools?", ["Yes", "No"]) == "Yes"
    proximity_parks = st.radio("Is the property close to parks?", ["Yes", "No"]) == "Yes"

    # Shared housing specific details
    shared_housing_details = {}
    if property_type == "Shared Housing":
        gender = st.radio("Your Gender", ["Male", "Female", "Divers"])
        is_student = st.radio("Are you a student?", ["Yes", "No"]) == "Yes"
        current_people = st.number_input("Number of people currently living in the house", min_value=0, value=0)
        max_people = st.number_input("Maximum number of people allowed", min_value=int(current_people) + 1)
        same_sex_pref = st.radio("Same-sex preference?", ["Yes", "No"])
        shared_housing_details = {
            "gender": gender,
            "is_student": is_student,
            "current_people": current_people,
            "max_people": max_people,
            "same_sex_pref": same_sex_pref,
        }
        preferences = ["Students"]
    else:
        preferences = st.multiselect(
            "Preferences",
            ["Students", "Professionals", "Families", "No preference"]
        )

    # Save to database button
    if st.button("Submit"):
        if address and size and price:
            # Create new property entry
            new_property = {
                "id": st.session_state['houses']['id'].max() + 1 if len(st.session_state['houses']) > 0 else 1,
                "price": price,
                "transportation": np.random.randint(1, 10),
                "shared_living": property_type == 'Shared Housing',
                "lat": np.random.uniform(48.1, 48.2),
                "lon": np.random.uniform(11.5, 11.7),
                "region": 'Unknown',
                "address": address,
                "type": property_type,
                "size": size,
                "preferences": preferences,
                "proximity_schools": proximity_schools,
                "proximity_parks": proximity_parks,
                "owner_name": owner_name,
                "gender": shared_housing_details.get('gender', None),
                "is_student": shared_housing_details.get('is_student', None),
                "current_people": shared_housing_details.get('current_people', None),
                "max_people": shared_housing_details.get('max_people', None),
                "same_sex_pref": shared_housing_details.get('same_sex_pref', None),
            }

            new_property_df = pd.DataFrame([new_property])
            st.session_state['houses'] = pd.concat([st.session_state['houses'], new_property_df], ignore_index=True)
            st.success("Property added successfully!")
        else:
            st.error("Please fill in all required fields.")
    if st.button("Back to Home"):
        set_page("Home")

# Chat Page
def chat_page():
    st.title("Chat")
    st.markdown("Send messages to other users.")

    # Select recipient (hardcoded user list for demo purposes)
    recipients = ["Marc the Guru", "John Doe", "Jane Smith", "Alex Brown", "T. Hofmann"]
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

# AI Chat Assistant Page
def ai_chat_assistant_page():
    st.title("AI Chat Assistant")
    st.session_state["step"] = 1
    st.session_state["user_type"] = None

    for message in st.session_state["ai_messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Servus!"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state["ai_messages"].append({"role": "user", "content": prompt})


        homess = st.session_state["homes"]

        response =  st.session_state["chat_bot"].ask(prompt=prompt,language = "English", context = homess, user = st.session_state["user_profile"])
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state["ai_messages"].append({"role": "assistant", "content": response})

    if st.button("Reset Chat"):
        st.session_state["ai_messages"].clear()
        set_page("AI Chat Assistant")

    if st.button("Back to Home"):
        set_page("Home")

# Step-by-Step Guide
def step_by_step_guide():
    st.title("Step-by-Step Guide")
    # Step 1: Ask user type

    if st.session_state["step"] == 1:
        st.header("What best describes you?")
        col1, col2, col3 , col4= st.columns(4)
        with col1:
            if st.button("Professional"):
                set_user_type("Professional")
                st.rerun()
        with col2:
            if st.button("Student"):
                set_user_type("Student")
                st.rerun()
        with col3:
            if st.button("Family"):
                set_user_type("Family")
                st.rerun()
        with col4:
           if st.button("Back to Home"):
                set_page("Home")


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
        
# Professional Flow
def professional_flow():
    st.title("Guide for Professionals")
    st.write("### Step 1: Are you looking to Rent or Buy?")
    choice = st.radio("Select your preference:", ["Rent", "Sale"])

    if choice:
        st.write(f"### Step 2: Filter {choice.lower()} options")

        # Adjust price range dynamically
        if choice == "Rent":
            price_label = "Price per Month (€)"
            price_min_default = 0
            price_max_default = 4000
        elif choice == "Sale":
            price_label = "Price (€)"
            price_min_default = 0
            price_max_default = 1_000_000

        # Filter inputs
        price_min = st.number_input(f"Minimum {price_label}", min_value=0, value=price_min_default)
        price_max = st.number_input(f"Maximum {price_label}", min_value=0, value=price_max_default)
        size_min = st.number_input("Minimum Size (sq. meters)", min_value=0, value=0)
        size_max = st.number_input("Maximum Size (sq. meters)", min_value=0, value=300)
        if st.button("Back"):
            st.session_state["step"] = 1
            st.session_state["user_type"] = None
            st.rerun()


        # Find matching properties
        if st.button("Find Matches"):
            if "houses" in st.session_state:
                houses_df = st.session_state['houses']
                # Filter properties
                matching_properties = houses_df[
                    (houses_df['type'].str.lower() == choice.lower())
                    & (houses_df['price'] >= price_min)
                    & (houses_df['price'] <= price_max)
                    & (houses_df['size'] >= size_min)
                    & (houses_df['size'] <= size_max)
                    & (houses_df['preferences'].apply(lambda x: 'Professionals' in x or 'No preference' in x))
                ]

                # Display matches

                if not matching_properties.empty:
                    cnt = 0
                    st.write(f"### Matching {choice.lower()} options:")
                    for idx, prop in matching_properties.iterrows():
                        st.markdown(
                            f"""
                                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px; background-color: #f9f9f9;">
                                    <strong>Type:</strong> {prop["type"]}<br>
                                    <strong>Address:</strong> {prop["address"]}<br>
                                    <strong>Size:</strong> {prop["size"]} sq. meters<br>
                                    <strong>Price:</strong> €{prop["price"]}<br>
                                    <strong>Preferences:</strong> {", ".join(prop["preferences"])}
                                </div>
                                """,
                            unsafe_allow_html=True,
                        )
                        if st.button(f"MJ {cnt}"):
                            st.session_state["chat_messages"].append({"recipient" : "John Doe", "message" : "Niggalodeaon", "timestamp" : "Just Now"})
                        cnt+=1
                            
                else:
                    st.warning(f"No {choice.lower()} options found matching your criteria.")
            else:
                st.error("No properties available in the database.")

# Student Flow
def student_flow():
    st.title("Guide for Students")
    st.write("### Step 1: Are you looking for Rent or Shared Housing?")
    choice = st.radio("Select your preference:", ["Rent", "Shared Housing"])

    if choice:
        st.write(f"### Step 2: Filter {choice.lower()} options")

        if choice == "Rent":
            # Rent-specific filtering
            price_min = st.number_input("Minimum Price (€)", min_value=0, value=0)
            price_max = st.number_input("Maximum Price (€)", min_value=0, value=2000)
            size_min = st.number_input("Minimum Size (sq. meters)", min_value=0, value=0)
            size_max = st.number_input("Maximum Size (sq. meters)", min_value=0, value=100)
            my_same_gender_pref = False 

        elif choice == "Shared Housing":
            # Shared Housing-specific filtering
            # Gender and Same-Gender Preference
            gender = st.radio("Your Gender", ["Male", "Female", "Divers"])
            my_same_gender_pref = st.radio("Do you prefer same-gender housing?", ["Yes", "No"]) == "Yes"
            max_people = st.number_input("Maximum number of people wished", min_value=1, value=3)
            price_max = st.number_input("Maximum Price (€)", min_value=0, value=1000)
        if st.button("Back"):
            st.session_state["step"] = 1
            st.session_state["user_type"] = None
            st.rerun()

        # Find matches
        if st.button("Find Matches"):
            if "houses" in st.session_state:
                houses_df = st.session_state['houses']
                # Filter logic
                if choice == "Rent":
                    matching_properties = houses_df[
                        (houses_df['type'].str.lower() == choice.lower())
                        & (houses_df['price'] >= price_min)
                        & (houses_df['price'] <= price_max)
                        & (houses_df['size'] >= size_min)
                        & (houses_df['size'] <= size_max)
                        & (houses_df['preferences'].apply(lambda x: 'Students' in x or 'No preference' in x))
                    ]
                elif choice == "Shared Housing":
                    matching_properties = houses_df[
                        (houses_df['type'].str.lower() == choice.lower())
                        & (houses_df['price'] <= price_max)
                        & ((houses_df['gender'] == gender) | (houses_df['same_sex_pref'] == 'No'))
                        & ((houses_df['same_sex_pref'] == 'No') | (houses_df['gender'] == gender))
                        & (houses_df['is_student'] == True)
                        & (houses_df['current_people'] < houses_df['max_people'])
                        & (houses_df['preferences'].apply(lambda x: 'Students' in x or 'No preference' in x))
                    ]

                # Display matches
                if not matching_properties.empty:
                    st.write(f"### Matching {choice.lower()} options:")
                    for idx, prop in matching_properties.iterrows():
                        st.markdown(
                            f"""
                                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px; background-color: #f9f9f9;">
                                    <strong>Type:</strong> {prop["type"]}<br>
                                    <strong>Address:</strong> {prop["address"]}<br>
                                    <strong>Size:</strong> {prop["size"]} sq. meters<br>
                                    <strong>Price:</strong> €{prop["price"]}<br>
                                    <strong>Preferences:</strong> {", ".join(prop["preferences"])}
                                </div>
                                """,
                            unsafe_allow_html=True,
                        )
                else:
                    st.warning(f"No {choice.lower()} options found matching your criteria.")
            else:
                st.error("No properties available in the database.")

# Family Flow
def family_flow():
    st.title("Guide for Families")
    st.write("### Step 1: Are you looking for Rent or Buy?")
    choice = st.radio("Select your preference:", ["Rent", "Sale"])

    if choice:
        st.write(f"### Step 2: Filter {choice.lower()} options")

        # Collect family-specific preferences
        proximity_schools = st.radio("Do you need proximity to schools?", ["Yes", "No"]) == "Yes"
        proximity_parks = st.radio("Do you need proximity to parks?", ["Yes", "No"]) == "Yes"
        price_min = st.number_input("Minimum Price (€)", min_value=0, value=0)
        price_max = st.number_input("Maximum Price (€)", min_value=0, value=5000)
        size_min = st.number_input("Minimum Size (sq. meters)", min_value=0, value=50)
        size_max = st.number_input("Maximum Size (sq. meters)", min_value=0, value=300)
        if st.button("Back"):
            st.session_state["step"] = 1
            st.session_state["user_type"] = None
            st.rerun()

        # Find matches
        if st.button("Find Matches"):
            if "houses" in st.session_state:
                houses_df = st.session_state['houses']
                # Filter properties
                matching_properties = houses_df[
                    (houses_df['type'].str.lower() == choice.lower())
                    & (houses_df['price'] >= price_min)
                    & (houses_df['price'] <= price_max)
                    & (houses_df['size'] >= size_min)
                    & (houses_df['size'] <= size_max)
                    & (houses_df['preferences'].apply(lambda x: 'Families' in x or 'No preference' in x))
                    & ((~proximity_schools) | (houses_df['proximity_schools'] == True))
                    & ((~proximity_parks) | (houses_df['proximity_parks'] == True))
                ]

                # Display matches
                if not matching_properties.empty:
                    st.write(f"### Matching {choice.lower()} options:")
                    for idx, prop in matching_properties.iterrows():
                        st.markdown(
                            f"""
                            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px; background-color: #f9f9f9;">
                                <strong>Type:</strong> {prop["type"]}<br>
                                <strong>Address:</strong> {prop["address"]}<br>
                                <strong>Size:</strong> {prop["size"]} sq. meters<br>
                                <strong>Price:</strong> €{prop["price"]}<br>
                                <strong>Preferences:</strong> {", ".join(prop["preferences"])}<br>
                                <strong>Proximity to Schools:</strong> {"Yes" if prop["proximity_schools"] else "No"}<br>
                                <strong>Proximity to Parks:</strong> {"Yes" if prop["proximity_parks"] else "No"}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                else:
                    st.warning(f"No {choice.lower()} options found matching your criteria.")
            else:
                st.error("No properties available in the database.")

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

# Function to assess if the user can get the selected house
def assess_user_for_house(user_profile, house):
    # Simple assessment logic:
    # User must have monthly income at least twice the rent price
    # User must be above 18 years old
    required_income = house['price'] * 2
    user_income = user_profile.get('monthly_income', 0)
    user_age = user_profile.get('age', 0)

    if user_income >= required_income and user_age >= 18:
        st.session_state["homes"].append(str(house))
        print(st.session_state["homes"])
        return True
    else:
        return False

# Location Visualizer
def location_visualizer():
    st.header("Interactive Location Visualizer")

    # Initialize session state for user preferences and housing data
    if 'user_preferences' not in st.session_state:
        st.session_state['user_preferences'] = {
            'price': 1500,
            'transportation': 7,
            'shared_living': True
        }
    if 'selected_district' not in st.session_state:
        st.session_state['selected_district'] = None
    if 'selected_house' not in st.session_state:
        st.session_state['selected_house'] = None

    # Sidebar: User Preferences
    st.sidebar.header("Set Your Preferences")
    price = st.sidebar.slider("Preferred Price (€)", 500, 3000, st.session_state['user_preferences']['price'])
    transportation = st.sidebar.slider("Proximity to Transportation (1=Far, 10=Close)", 1, 10, st.session_state['user_preferences']['transportation'])
    shared_living = st.sidebar.radio("Shared Living?", [False, True], index=int(st.session_state['user_preferences']['shared_living']))

    # Update session state preferences only if they change
    if (price, transportation, shared_living) != (
        st.session_state['user_preferences']['price'],
        st.session_state['user_preferences']['transportation'],
        st.session_state['user_preferences']['shared_living']
    ):
        st.session_state['user_preferences'] = {
            'price': price,
            'transportation': transportation,
            'shared_living': shared_living
        }
        # Reset selected district and house when preferences change
        st.session_state['selected_district'] = None
        st.session_state['selected_house'] = None

    # Load persistent housing data
    houses = st.session_state['houses']

    # Filter houses based on user preferences
    filtered_houses = houses[
        (houses['price'] <= st.session_state['user_preferences']['price']) &
        (houses['transportation'] >= st.session_state['user_preferences']['transportation']) &
        (houses['shared_living'] == st.session_state['user_preferences']['shared_living'])
    ]

    # Count houses per district after filtering
    district_counts = filtered_houses['region'].value_counts().reset_index()
    district_counts.columns = ['District', 'Number of Houses']

    # Map Visualization
    st.header("Explore the Number of Houses Per District")

    if st.session_state['selected_district'] is None:
        # Show the districts with counts
        district_map = folium.Map(location=[48.1374, 11.5755], zoom_start=12)

        # Add district counts directly as numbers on the markers
        for district, center in district_centers.items():
            count = district_counts.loc[district_counts['District'] == district, 'Number of Houses']
            count_text = count.values[0] if not count.empty else 0  # Show 0 if no houses match

            # Add CircleMarker with count as its text
            folium.CircleMarker(
                location=center,
                radius=15,  # Adjust size for the marker
                color='blue',
                fill=True,
                fill_color='blue',
                fill_opacity=0.6,
                popup=f"{district}<br>Number of Houses: {count_text}",
                tooltip=f"{district}: {count_text}",
            ).add_to(district_map)

            # Add the count as a larger, more readable text overlay
            folium.Marker(
                location=center,
                icon=folium.DivIcon(
                    icon_size=(35, 35),  # Set the size of the icon
                    icon_anchor=(17.5, 17.5),  # Center the icon
                    html=f"""
                        <div style="
                            font-size: 18px; 
                            font-weight: bold; 
                            color: black; 
                            text-align: center; 
                            background: white; 
                            border-radius: 50%; 
                            border: 2px solid blue; 
                            width: 35px; 
                            height: 35px; 
                            line-height: 35px;
                        ">
                            {count_text}
                        </div>
                        """
                )
            ).add_to(district_map)
        # Display map and capture interaction
        map_output = st_folium(district_map, width=800, height=600)

        # Handle district marker clicks
        if map_output and map_output['last_object_clicked']:
            # Get the location of the click
            clicked_lat = map_output['last_object_clicked']['lat']
            clicked_lng = map_output['last_object_clicked']['lng']

            # Identify which district was clicked
            for district, center in district_centers.items():
                dist = np.linalg.norm(np.array([clicked_lat, clicked_lng]) - np.array(center))
                if dist < 0.01:  # Adjust threshold as needed
                    st.session_state['selected_district'] = district
                    break
    else:
        house_images = [
            "https://pictures.immobilienscout24.de/dims3/S3/legacy_thumbnail/800x600/format/webp/quality/73/http://s3-eu-west-1.amazonaws.com/pda-pro-pictures-projectpictures-8hecgpgpb9fo/59977873/b3e639e2-8b5d-419b-b3f4-a13ef1b06b44.jpg",
            "https://pictures.immobilienscout24.de/listings/b1b0fe30-24fa-45eb-b339-6cc380bc12a4-1862446778.jpg/ORIG/legacy_thumbnail/420x315/format/webp/quality/73",
            "https://pictures.immobilienscout24.de/listings/31470eae-6ddc-4c30-a35a-128c2799c3a9-1862590404.jpg/ORIG/legacy_thumbnail/420x315/format/webp/quality/73",
            "https://pictures.immobilienscout24.de/listings/a7eafd80-0384-4b80-99b0-805efd4f19e7-1790699901.jpg/ORIG/legacy_thumbnail/420x315/format/webp/quality/73",
            "https://pictures.immobilienscout24.de/listings/7f3366f9-e056-44c6-9a9a-16ea57045902-1409219300.jpg/ORIG/legacy_thumbnail/420x315/format/webp/quality/73",
            "https://pictures.immobilienscout24.de/listings/5cbbb3b2-5b7b-4a79-84ad-4113467fe69f-1859079993.jpg/ORIG/legacy_thumbnail/420x315/format/webp/quality/73",
            "https://pictures.immobilienscout24.de/listings/cd5b168f-d60a-4e26-9bfa-a61910b223fe-1861893232.jpg/ORIG/legacy_thumbnail/420x315/format/webp/quality/73",
            "https://pictures.immobilienscout24.de/listings/a75f94ae-e032-48db-a1f6-65b16178c51b-1859861946.jpg/ORIG/legacy_thumbnail/420x315/format/webp/quality/73",
            "https://pictures.immobilienscout24.de/listings/662e6141-31f9-4d61-8f21-66cdd8b0dacd-1845492399.jpg/ORIG/legacy_thumbnail/420x315/format/webp/quality/73",
            "https://pictures.immobilienscout24.de/listings/772d8c24-910a-4ca2-99ab-98b49d990862-1838047478.jpg/ORIG/legacy_thumbnail/420x315/format/webp/quality/73",
            "https://pictures.immobilienscout24.de/listings/b924fca7-1d32-4035-aea5-8752ab50eead-1810315289.jpg/ORIG/legacy_thumbnail/420x315/format/webp/quality/73",
            "https://pictures.immobilienscout24.de/listings/f8fa991e-1f0b-4d9b-ab1c-26f4462fafec-1860463939.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/851fb9e7-da7a-4001-93d9-f1c4d3edede9-1857806205.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/9fcc1164-fa48-4b85-accc-6452a3ab5b54-1858257537.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/b99693e0-e70b-48f5-824a-122935e66ba8-1854421902.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/9f8a3908-823d-4ceb-9c52-63ee816652c1-1860936626.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/441c2204-0ead-40c9-9f6f-18bf296881b1-1491910987.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/336f39ea-5064-4b2f-8e56-f78375561445-1851651912.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/42d03a56-1bb0-4ecb-8f6e-b8a5d60ab03d-1846082319.jpeg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/3072b6f1-fe9e-40af-be27-8f5c49b708e1-1859322008.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/32ef8af0-4602-46fe-b800-8c244ef1fd44-1858950053.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/5ddbaf57-0077-42d9-95c5-d269d9eb1f24-1857854473.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/b554d22f-a028-42fd-965e-e876f3e41ad4-1856810703.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/413b43ba-c4bb-4c56-80f5-17364fbd719f-1853173455.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/e995aa19-8bc2-4221-8ca0-e355575d6065-1856184726.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/bd627363-aaa8-42ea-9717-f9264dbf58e9-1861202025.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/8840f5c5-acca-4fec-9703-7674dcd4a040-1860846507.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/99e2cae4-a748-4384-9940-e9e51ec30a2a-1860344126.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/5a97271b-6055-40cd-aa0f-997280a7b71f-1860203449.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/98b1e9d1-4d70-4d2c-aaf7-69628f22839a-1859327566.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/0a21fe69-72c6-4fec-aac6-a8bc4a59c6e8-1854786018.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/4f071de9-dfd1-4239-ac45-afaf39fb7811-1851392403.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/3e105cc3-c939-4477-8c13-f1b82a73d992-1848432677.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/3e105cc3-c939-4477-8c13-f1b82a73d992-1848432677.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/df620cd6-dab3-47e7-9e68-d0fa806db4b1-1853516841.png/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
            "https://pictures.immobilienscout24.de/listings/a27cff34-0e19-48cc-b24a-9ee7db8974bf-1829425500.jpg/ORIG/legacy_thumbnail/420x315/format/jpg/quality/80",
        ]        # Show the houses in the selected district
        selected_district = st.session_state['selected_district']
        district_center = district_centers[selected_district]
        district_map = folium.Map(location=district_center, zoom_start=14)

        # Filter houses in the selected district
        district_houses = filtered_houses[filtered_houses['region'] == selected_district]

        # Add house markers with popup including details
        for _, house in district_houses.iterrows():
            # Prepare the HTML content for the popup
            popup_html = f"""
                <b>House ID:</b> {house['id']}<br>
                <b>Price:</b> €{house['price']}<br>
                <b>Transport Score:</b> {house['transportation']}<br>
                <b>Shared Living:</b> {'Yes' if house['shared_living'] else 'No'}<br>
                <b>Address:</b> {house['address'] if 'address' in house else 'N/A'}<br>
            """

            popup = folium.Popup(popup_html, max_width=300)

            folium.Marker(
                location=[house['lat'], house['lon']],
                popup=popup,
                tooltip=f"House ID: {house['id']}"
            ).add_to(district_map)

        # Display map
        map_output = st_folium(district_map, width=800, height=600)

        # Handle house marker clicks
        if map_output and map_output['last_object_clicked']:
            # Get the location of the click
            clicked_lat = map_output['last_object_clicked']['lat']
            clicked_lng = map_output['last_object_clicked']['lng']

            # Find the house that was clicked
            for _, house in district_houses.iterrows():
                dist = np.linalg.norm(np.array([clicked_lat, clicked_lng]) - np.array([house['lat'], house['lon']]))
                if dist < 0.0001:  # Adjust threshold as needed
                    st.session_state['selected_house'] = house['id']
                    break

        # Display house details and assessment if a house is selected
        if st.session_state['selected_house']:
            selected_house = houses[houses['id'] == st.session_state['selected_house']].iloc[0]
            st.subheader("House Details")
            st.write(f"**House ID:** {selected_house['id']}")
            st.write(f"**Price:** €{selected_house['price']}")
            st.write(f"**Transport Score:** {selected_house['transportation']}")
            st.write(f"**Shared Living:** {'Yes' if selected_house['shared_living'] else 'No'}")
            st.write(f"**Address:** {selected_house['address'] if 'address' in selected_house else 'N/A'}")
            st.write("**Picture:**")
            image_index = selected_house['id'] % len(house_images)  # Cycle through images
            st.image(house_images[image_index], caption="House Image") # Replace with actual image URL

            # Assess button
            if st.button("Assess"):
                assessment = assess_user_for_house(st.session_state['user_profile'], selected_house)
                if assessment:
                    st.success('Congratulations! You meet the requirements for this house.', icon="✅")  
                else:
                    st.error("We're sorry, but you do not meet the requirements for this house.")

            # Option to go back to the map view
            if st.button("Back to Map"):
                st.session_state['selected_house'] = None
                st.rerun()

        # Option to go back to district view
        if st.button("Back to Districts"):
            st.session_state['selected_district'] = None
            st.session_state['selected_house'] = None
            st.rerun()

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

# FAQ Page
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

