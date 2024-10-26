import streamlit as st
import pandas as pd
from geopy.distance import geodesic
import random
import geocoder

# Function to get current location
def get_current_location():
    location = geocoder.ip('me')
    if location.latlng:
        return location.latlng[0], location.latlng[1]
    else:
        st.warning("Unable to retrieve location. Please enter manually.")
        return None, None

# Load hospital data
data = pd.read_csv("hospitals_with_lat_long.csv")
hospital_data = pd.DataFrame(data)

# Streamlit app layout
st.title("Ambulance Alert System")

# Patient Info Section
st.header("Patient Information")
injury_type = st.selectbox("Select Injury Type", ["Head Injury", "Severe Blood Loss", "Heart Stroke", "Airway Obstruction", "Fire Burns"])
if st.button("Submit Patient Info"):
    st.write(f"Injury Type: {injury_type}")

# Initialize variables
user_latitude, user_longitude = None, None

# Get User's Current Location
st.header("Calculate Nearest Hospital")
if st.button("Get Current Location"):
    user_latitude, user_longitude = get_current_location()
    if user_latitude and user_longitude:
        st.write("Current Latitude:", user_latitude)
        st.write("Current Longitude:", user_longitude)
else:
    # Allow manual input if unable to get location automatically
    user_latitude = st.number_input("Enter your current Latitude", value=12.9715987)
    user_longitude = st.number_input("Enter your current Longitude", value=80.243569)

# Ensure the location is properly set
if user_latitude is not None and user_longitude is not None:
    current_location = (user_latitude, user_longitude)

    # Calculate the Nearest Hospital
    if st.button("Find Nearest Hospital"):
        # Calculate distances to each hospital
        hospital_data['Distance_km'] = hospital_data.apply(
            lambda row: geodesic(current_location, (row['Latitude'], row['Longitude'])).km, axis=1
        )

        # Find the nearest hospital
        nearest_hospital = hospital_data.loc[hospital_data['Distance_km'].idxmin()]
        st.write("Nearest Hospital:", nearest_hospital['Hospital'])
        st.write("Distance:", round(nearest_hospital['Distance_km'], 2), "km")

    # Simulate Route Navigation (Mock)
    if st.button("Navigate to Nearest Hospital"):
        shortest_route = random.choice(["Route 1: Main St -> Elm St", "Route 2: Oak St -> Pine St"])
        st.write(f"Suggested Route: {shortest_route}")

    # Performance Credit
    st.header("Driver Performance")
    if st.button("Complete Trip"):
        st.success(f"Credit added")
else:
    st.warning("Please provide your current location.")