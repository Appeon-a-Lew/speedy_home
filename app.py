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

