## Speedy Home App

This is the **Speedy Home** application, a multilingual housing assistant designed to help users navigate the German housing and mortgage processes with ease. The app includes financial tools, AI-powered recommendations, location visualizations, and step-by-step guides.

---

## Setup Instructions

Follow these steps to set up the project environment and run the app locally.

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/your-username/speedy_home.git
cd speedy_home
 speedy_home
```
### 2. Create and Activate the Virtual environment
Create a Python virtual environment called speedy to isolate project dependencies.
**On macOS/Linux:**
```bash 
python3 -m venv speedy
source speedy/bin/Activate
```

**On Windows:** 
```bash 
python -m venv speedy
speedy\Scripts\activate
```

### 3. Install Dependencies

With the virtual environment activated, install the required libraries:

```bash
pip install -r requirements.txt
```

### 4. Run and Deactivate 

Start the Streamlit app:
```bash
streamlit run app.py
```
The app will open in your default web browser. If it doesn’t, navigate to the URL displayed in your terminal (usually http://localhost:8501).

When you're done, deactivate the virtual environment:
```bash
deactivate
```

## Features 

- Multilingual Platform: Translate housing-related terms into different languages.
- Step-by-Step Guides: Tailored guides for different user profiles (e.g., professionals, students, families).
- Financial Tools: Mortgage calculator with visualization.
- Smart Recommendations: AI-based roommate or property matching.
- Interactive Location Visualizations: View properties and nearby amenities on a map.
- Gamified Education: Learn housing regulations with quizzes.

## Development Notes
