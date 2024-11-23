import streamlit as st
#from googletrans import Translator
import numpy as np
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import  bot
# Initialize translator
#translator = Translator()

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
if "properties" not in st.session_state:
    st.session_state["properties"] = []
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
    st.markdown("Provide details about your property below:")
    st.session_state["step"] = 1
    st.session_state["user_type"] = None

    # Property details form
    property_type = st.selectbox("Is this property for Rent, Sale, or Shared Housing?", ["Rent", "Sale", "Shared Housing"])
    address = st.text_input("Address")
    size = st.number_input("Size (in sq. meters)", min_value=0)
    price = st.number_input("Price (€)", min_value=0)

    # Proximity details for family-friendly properties
    proximity_schools = st.radio("Is the property close to schools?", ["Yes", "No"]) == "Yes"
    proximity_parks = st.radio("Is the property close to parks?", ["Yes", "No"]) == "Yes"

    # Shared housing specific details
    shared_housing_details = {}
    if property_type == "Shared Housing":
        gender = st.radio("Your Gender", ["Male", "Female"])
        is_student = st.radio("Are you a student?", ["Yes", "No"]) == "Yes"
        current_people = st.number_input("Number of people currently living in the house", min_value=0, value=0)
        max_people = st.number_input("Maximum number of people allowed", min_value=current_people + 1)
        same_sex_pref = st.radio("Same-sex preference?", ["Yes", "No"])
        shared_housing_details = {
            "gender": gender,
            "is_student": is_student,
            "current_people": current_people,
            "max_people": max_people,
            "same_sex_pref": same_sex_pref,
        }
        preferences = "Students"
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
                "type": property_type,
                "address": address,
                "size": size,
                "price": price,
                "preferences": preferences,
                "proximity_schools": proximity_schools,
                "proximity_parks": proximity_parks,
                **shared_housing_details,
            }

            st.session_state["properties"].append(new_property)
            st.success("Property added successfully!")
        else:
            st.error("Please fill in all required fields.")

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

    for message in st.session_state["ai_messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Servus!"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state["ai_messages"].append({"role": "user", "content": prompt})

        response =  st.session_state["chat_bot"].ask(prompt=prompt)
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
    st.write("### Step 1: Are you looking to Rent or Buy?")
    choice = st.radio("Select your preference:", ["Rent", "Buy"])

    if choice:
        st.write(f"### Step 2: Filter {choice.lower()} options")

        # Adjust price range dynamically
        if choice == "Rent":
            price_label = "Price per Month (€)"
            price_min_default = 0
            price_max_default = 4000
        elif choice == "Buy":
            price_label = "Price (€)"
            price_min_default = 0
            price_max_default = 1_000_000

        # Filter inputs
        price_min = st.number_input(f"Minimum {price_label}", min_value=0, value=price_min_default)
        price_max = st.number_input(f"Maximum {price_label}", min_value=0, value=price_max_default)
        size_min = st.number_input("Minimum Size (sq. meters)", min_value=0, value=0)
        size_max = st.number_input("Maximum Size (sq. meters)", min_value=0, value=300)

        # Find matching properties
        if st.button("Find Matches"):
            if "properties" in st.session_state:
                # Filter properties
                matching_properties = [
                    prop for prop in st.session_state["properties"]
                    if prop["type"].lower() == choice.lower()  # Match Rent/Buy
                       and price_min <= prop["price"] <= price_max  # Match price range
                       and size_min <= prop["size"] <= size_max  # Match size range
                       and ("Professionals" in prop["preferences"] or "No preference" in prop["preferences"])
                    # Match preference
                ]

                # Display matches
                if matching_properties:
                    st.write(f"### Matching {choice.lower()} options:")
                    for prop in matching_properties:
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

        elif choice == "Shared Housing":
            # Shared Housing-specific filtering
            # Gender and Same-Gender Preference
            gender = st.radio("Your Gender", ["Male", "Female"])
            same_gender_pref = st.radio("Do you prefer same-gender housing?", ["Yes", "No"]) == "Yes"
            max_people = st.number_input("Maximum number of people wished", min_value=1, value=3)
            price_max = st.number_input("Maximum Price (€)", min_value=0, value=1000)

        # Find matches
        if st.button("Find Matches"):
            if "properties" in st.session_state:
                # Filter logic
                matching_properties = [
                    prop for prop in st.session_state["properties"]
                    if prop["type"].lower() == choice.lower()  # Match Rent/Shared Housing
                       and price_min <= prop["price"] <= price_max  # Match price
                       and (not same_gender_pref or prop.get("gender") == gender)  # Match same gender if required
                       and (not prop.get("same_gender_pref") or prop.get("gender") == gender)  # Match owner preference
                       and (choice != "Shared Housing" or prop.get("is_student", False))  # Ensure offerer is student
                       and (choice != "Shared Housing" or prop.get("current_people", 0) < prop.get("max_people", 1))
                    # Match people
                ]

                # Display matches
                if matching_properties:
                    st.write(f"### Matching {choice.lower()} options:")
                    for prop in matching_properties:
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
    choice = st.radio("Select your preference:", ["Rent", "Buy"])

    if choice:
        st.write(f"### Step 2: Filter {choice.lower()} options")

        # Collect family-specific preferences
        bedrooms = st.number_input("Minimum Number of Bedrooms", min_value=1, value=2)
        proximity_schools = st.radio("Do you need proximity to schools?", ["Yes", "No"]) == "Yes"
        proximity_parks = st.radio("Do you need proximity to parks?", ["Yes", "No"]) == "Yes"
        price_min = st.number_input("Minimum Price (€)", min_value=0, value=0)
        price_max = st.number_input("Maximum Price (€)", min_value=0, value=5000)
        size_min = st.number_input("Minimum Size (sq. meters)", min_value=0, value=50)
        size_max = st.number_input("Maximum Size (sq. meters)", min_value=0, value=300)

        # Find matches
        if st.button("Find Matches"):
            if "properties" in st.session_state:
                # Filter properties
                matching_properties = [
                    prop for prop in st.session_state["properties"]
                    if prop["type"].lower() == choice.lower()  # Match Rent/Buy
                    and price_min <= prop["price"] <= price_max  # Match price range
                    and size_min <= prop["size"] <= size_max  # Match size range
                    and ("Families" in prop["preferences"] or "No preference" in prop["preferences"])  # Match preference
                    and (not proximity_schools or prop["proximity_schools"])  # Match school proximity
                    and (not proximity_parks or prop["proximity_parks"])  # Match park proximity
                ]

                # Display matches
                if matching_properties:
                    st.write(f"### Matching {choice.lower()} options:")
                    for prop in matching_properties:
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
# Function to generate random coordinates near a district's center
def generate_coordinates(center, num_points, radius=0.01):
    latitudes = np.random.uniform(center[0] - radius, center[0] + radius, num_points)
    longitudes = np.random.uniform(center[1] - radius, center[1] + radius, num_points)
    return latitudes, longitudes

# Generate mock housing data
def generate_mock_data(houses_per_district=20):
    data = {
        'id': [],
        'price': [],
        'transportation': [],
        'shared_living': [],
        'lat': [],
        'lon': [],
        'region': []
    }

    for region, center in district_centers.items():
        lats, lons = generate_coordinates(center, houses_per_district)
        data['id'].extend(range(len(data['id']) + 1, len(data['id']) + houses_per_district + 1))
        data['price'].extend(np.random.randint(500, 3000, houses_per_district))
        data['transportation'].extend(np.random.randint(1, 10, houses_per_district))
        data['shared_living'].extend(np.random.choice([True, False], houses_per_district))
        data['lat'].extend(lats)
        data['lon'].extend(lons)
        data['region'].extend([region] * houses_per_district)
    
    return pd.DataFrame(data)

# Count houses per district
def count_houses_per_district(houses):
    district_counts = houses['region'].value_counts().reset_index()
    district_counts.columns = ['District', 'Number of Houses']
    return district_counts


@st.cache_data  # Cache ranking results to avoid recomputation
def rank_houses(houses, preferences):
    houses['score'] = (
        (1 - np.abs(houses['price'] - preferences['price']) / preferences['price']) * 0.5 +  # Weight: 50%
        (houses['transportation'] / 10) * 0.3 +  # Weight: 30%
        (houses['shared_living'] == preferences['shared_living']) * 0.2  # Weight: 20%
    )
    return houses.sort_values(by='score', ascending=False)


def count_houses_per_district_with_filter(houses, preferences):
    filtered_houses = houses[
        (houses['price'] <= preferences['price']) &
        (houses['transportation'] >= preferences['transportation']) &
        (houses['shared_living'] == preferences['shared_living'])
    ]
    district_counts = filtered_houses['region'].value_counts().reset_index()
    district_counts.columns = ['District', 'Number of Houses']
    return district_counts


# Main function for interactive visualization
def location_visualizer():
    st.header("Interactive Location Visualizer")


    # Initialize session state for user preferences and housing data
    if 'user_preferences' not in st.session_state:
        st.session_state['user_preferences'] = {
            'price': 1500,
            'transportation': 7,
            'shared_living': True
        }
    if 'houses' not in st.session_state:
        st.session_state['houses'] = generate_mock_data()

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

    # Load persistent housing data
    houses = st.session_state['houses']

    # Count houses per district after filtering
    district_counts = count_houses_per_district_with_filter(houses, st.session_state['user_preferences'])

    # Map Visualization
    st.header("Explore the Number of Houses Per District")
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
            icon=folium.DivIcon(html=f"""
                <div style="
                    font-size: 16px; 
                    font-weight: bold; 
                    color: black; 
                    text-align: center; 
                    background: white; 
                    border-radius: 50%; 
                    border: 2px solid blue; 
                    width: 30px; 
                    height: 30px; 
                    line-height: 30px;
                    ">
                    {count_text}
                </div>
            """)
        ).add_to(district_map)


    # Display map
    st_folium(district_map, width=800, height=600)

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