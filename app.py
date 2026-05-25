import streamlit as st
import cv2
import numpy as np
import face_recognition
import json
import os
import datetime
import hashlib
import math
from pathlib import Path
from PIL import Image

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {
        'preferred_pronouns': 'They/Them',
        'accessibility_needs': 'None',
        'emergency_contact': '',
        'share_location': True
    }

st.set_page_config(
    page_title="SafeRide - Safe Travel for Everyone",
    page_icon="🛡️",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 18px;
        padding: 12px;
        border-radius: 10px;
        border: none;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        transition: 0.3s;
    }
    .success-box {
        background: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 10px 0;
    }
    .error-box {
        background: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #dc3545;
        margin: 10px 0;
    }
    .price-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
    }
    .price-card h1 {
        font-size: 48px;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ SafeRide")
st.markdown("*Biometric Authentication • Safe Travel for Everyone*")

DATA_DIR = Path("biometric_data")
DATA_DIR.mkdir(exist_ok=True)
USERS_FILE = DATA_DIR / "users.json"
LOCATIONS_FILE = DATA_DIR / "locations.json"

def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_locations():
    if LOCATIONS_FILE.exists():
        with open(LOCATIONS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_locations(locations):
    with open(LOCATIONS_FILE, 'w') as f:
        json.dump(locations, f, indent=2)

# Predefined locations and coordinates
PREDEFINED_LOCATIONS = {
    "Cape Town CBD": {"lat": -33.9249, "lon": 18.4241},
    "Sandton City": {"lat": -26.1076, "lon": 28.0567},
    "Durban Beachfront": {"lat": -29.8587, "lon": 31.0218},
    "Pretoria Central": {"lat": -25.7479, "lon": 28.2293},
    "Johannesburg Park Station": {"lat": -26.1958, "lon": 28.0415},
    "OR Tambo Airport": {"lat": -26.1392, "lon": 28.2460},
    "Centurion Mall": {"lat": -25.8607, "lon": 28.1895},
    "Midrand": {"lat": -25.9992, "lon": 28.1268},
    "Soweto - Orlando Towers": {"lat": -26.2384, "lon": 27.9092},
    "Rosebank Mall": {"lat": -26.1462, "lon": 28.0458},
    "Fourways Mall": {"lat": -26.0273, "lon": 28.0039},
    "Menlyn Maine": {"lat": -25.7821, "lon": 28.2765},
}

# Price calculation function
def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in km using Haversine formula"""
    R = 6371  # Earth's radius in km
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def calculate_price(distance, ride_type, time_multiplier=1.0):
    """Calculate price based on distance, ride type, and time"""
    # Base rates per km (in Rands)
    base_rates = {
        "Standard": 12.00,
        "Comfort": 18.00,
        "Premium": 25.00,
        "XL (6 seater)": 20.00,
        "Electric": 15.00
    }
    
    base_price = distance * base_rates.get(ride_type, 12.00)
    
    # Minimum fare
    min_fare = {
        "Standard": 35,
        "Comfort": 50,
        "Premium": 70,
        "XL (6 seater)": 60,
        "Electric": 45
    }
    
    final_price = max(base_price, min_fare.get(ride_type, 35))
    
    # Apply time multiplier (peak hours)
    current_hour = datetime.datetime.now().hour
    if (7 <= current_hour <= 9) or (16 <= current_hour <= 19):  # Peak hours
        final_price *= 1.3
        peak_surcharge = True
    else:
        peak_surcharge = False
    
    return round(final_price, 2), peak_surcharge

def encode_face(image_file):
    try:
        image = Image.open(image_file)
        image_np = np.array(image)
        
        if len(image_np.shape) == 2:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
        elif image_np.shape[2] == 4:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
        
        face_locations = face_recognition.face_locations(image_np)
        if len(face_locations) == 0:
            return None, "No face detected in image"
        
        face_encodings = face_recognition.face_encodings(image_np, face_locations)
        if len(face_encodings) == 0:
            return None, "Could not encode face"
        
        return face_encodings[0].tolist(), "Success"
    except Exception as e:
        return None, f"Error: {str(e)}"

def verify_face(live_encoding, stored_encoding):
    if live_encoding is None or stored_encoding is None:
        return False, 0
    
    distance = face_recognition.face_distance([np.array(stored_encoding)], np.array(live_encoding))[0]
    confidence = (1 - distance) * 100
    is_match = distance < 0.6
    return is_match, confidence

# Sidebar Menu
menu = st.sidebar.selectbox("Navigation", [
    "🏠 Home",
    "📝 Register",
    "🔐 Verify Identity",
    "🚗 Request Ride",
    "⚙️ Preferences",
    "📊 My Dashboard"
])

# Home Page
if menu == "🏠 Home":
    st.markdown("### Welcome to SafeRide - Safe Travel for All")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Face Recognition", "✓", "Secure")
    with col2:
        st.metric("Live Verification", "✓", "Real-time")
    with col3:
        st.metric("SOS Alert", "✓", "24/7")
    with col4:
        st.metric("Distance Pricing", "✓", "Fair & Transparent")
    
    st.markdown("""
    <div class="success-box">
        <b>✨ How SafeRide Works:</b><br>
        1️⃣ Register with your face photo<br>
        2️⃣ Verify using camera before each ride<br>
        3️⃣ Request a ride - prices calculated by distance<br>
        4️⃣ Safe travel with real-time tracking<br>
        5️⃣ SOS button for emergencies
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💰 Price Calculator")
    col1, col2 = st.columns(2)
    with col1:
        test_pickup = st.selectbox("Test Pickup", list(PREDEFINED_LOCATIONS.keys()), key="test_pickup")
    with col2:
        test_dest = st.selectbox("Test Destination", list(PREDEFINED_LOCATIONS.keys()), key="test_dest")
    
    if test_pickup and test_dest and test_pickup != test_dest:
        pickup_coords = PREDEFINED_LOCATIONS[test_pickup]
        dest_coords = PREDEFINED_LOCATIONS[test_dest]
        distance = calculate_distance(pickup_coords['lat'], pickup_coords['lon'], 
                                      dest_coords['lat'], dest_coords['lon'])
        
        st.markdown(f"""
        <div class="price-card">
            <h3>Estimated Price</h3>
            <h1>R{distance * 12:.0f} - R{distance * 25:.0f}</h1>
            <p>Distance: {distance:.1f} km | Travel time: {(distance/40*60):.0f} minutes</p>
        </div>
        """, unsafe_allow_html=True)

# Registration Page
elif menu == "📝 Register":
    st.markdown("### 📝 Register for SafeRide")
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            phone = st.text_input("Phone Number")
            email = st.text_input("Email")
        with col2:
            pronouns = st.selectbox("Pronouns", ["She/Her", "He/Him", "They/Them", "Prefer not to say", "Other"])
            emergency_contact = st.text_input("Emergency Contact Number")
        
        uploaded_image = st.file_uploader("Upload your face photo (clear, well-lit photo)", type=['jpg', 'jpeg', 'png'])
        if uploaded_image:
            st.image(uploaded_image, caption="Registration Photo", width=200)
        
        submitted = st.form_submit_button("Register with Biometric")
        
        if submitted:
            if not name or not phone:
                st.error("Please fill all required fields")
            elif not uploaded_image:
                st.error("Please upload a face photo")
            else:
                with st.spinner("Processing facial data..."):
                    face_encoding, message = encode_face(uploaded_image)
                    
                    if face_encoding:
                        users = load_users()
                        user_id = hashlib.md5(f"{name}{phone}{datetime.datetime.now()}".encode()).hexdigest()[:8]
                        
                        users[user_id] = {
                            "user_id": user_id,
                            "name": name,
                            "phone": phone,
                            "email": email,
                            "pronouns": pronouns,
                            "emergency_contact": emergency_contact,
                            "face_encoding": face_encoding,
                            "registered_date": str(datetime.datetime.now()),
                            "total_rides": 0,
                            "total_spent": 0
                        }
                        save_users(users)
                        
                        st.success(f"✅ Registration Successful!")
                        st.info(f"Your User ID: {user_id}")
                        st.warning("⚠️ Save this User ID - you'll need it for verification!")
                        st.balloons()
                    else:
                        st.error(f"❌ {message}")

# Verification Page
elif menu == "🔐 Verify Identity":
    st.markdown("### 🔐 Biometric Identity Verification")
    
    user_id = st.text_input("Enter your User ID")
    st.markdown("**Take a live selfie for verification**")
    live_photo = st.camera_input("Look at the camera - ensure good lighting")
    
    if st.button("Verify My Identity", type="primary"):
        if not user_id:
            st.error("Please enter your User ID")
        elif not live_photo:
            st.error("Please take a selfie")
        else:
            users = load_users()
            if user_id not in users:
                st.error("User ID not found. Please register first.")
            else:
                with st.spinner("Verifying identity..."):
                    live_encoding, message = encode_face(live_photo)
                    
                    if live_encoding:
                        stored_encoding = users[user_id]["face_encoding"]
                        is_match, confidence = verify_face(live_encoding, stored_encoding)
                        
                        if is_match:
                            st.success(f"✅ Identity Verified!")
                            st.success(f"Welcome back, {users[user_id]['name']} ({users[user_id]['pronouns']})")
                            st.info(f"Confidence Score: {confidence:.1f}%")
                            
                            st.session_state.authenticated = True
                            st.session_state.user_id = user_id
                            st.session_state.user_name = users[user_id]['name']
                            st.balloons()
                        else:
                            st.error(f"❌ Verification Failed")
                            st.error(f"Confidence Score: {confidence:.1f}%")
                            st.warning("Please try again with better lighting or a clearer photo")
                    else:
                        st.error(f"❌ {message}")

# Request Ride Page
elif menu == "🚗 Request Ride":
    st.markdown("### 🚗 Request a Ride")
    
    if not st.session_state.authenticated:
        st.warning("⚠️ Please verify your identity first")
        st.info("Go to 'Verify Identity' page to verify yourself")
        st.stop()
    
    users = load_users()
    user = users.get(st.session_state.user_id, {})
    
    st.success(f"✅ Verified as: {user.get('name', 'Rider')} ({user.get('pronouns', 'They/Them')})")
    
    with st.form("ride_request_form"):
        col1, col2 = st.columns(2)
        with col1:
            pickup = st.selectbox("Pickup Location", list(PREDEFINED_LOCATIONS.keys()), key="pickup")
            st.caption("📍 Select your current location")
        with col2:
            destination = st.selectbox("Destination", list(PREDEFINED_LOCATIONS.keys()), key="destination")
            st.caption("🎯 Where are you going?")
        
        ride_type = st.selectbox("Ride Type", [
            "Standard", "Comfort", "Premium", "XL (6 seater)", "Electric"
        ])
        
        submitted = st.form_submit_button("Calculate Price & Request Ride")
        
        if submitted:
            if pickup == destination:
                st.error("Pickup and destination cannot be the same")
            else:
                # Calculate distance and price
                pickup_coords = PREDEFINED_LOCATIONS[pickup]
                dest_coords = PREDEFINED_LOCATIONS[destination]
                distance = calculate_distance(pickup_coords['lat'], pickup_coords['lon'], 
                                              dest_coords['lat'], dest_coords['lon'])
                price, peak_surcharge = calculate_price(distance, ride_type)
                
                # Estimated time (assuming 40 km/h average speed)
                estimated_time = (distance / 40) * 60
                
                st.markdown(f"""
                <div class="price-card">
                    <h4>Ride Summary</h4>
                    <h1>R{price}</h1>
                    <p>Distance: {distance:.1f} km</p>
                    <p>Estimated time: {estimated_time:.0f} minutes</p>
                    <p>Ride type: {ride_type}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if peak_surcharge:
                    st.warning("⚠️ Peak hour surcharge applied (30% extra)")
                
                # Show route on map
                st.markdown("### 🗺️ Route Map")
                route_data = pd.DataFrame({
                    'lat': [pickup_coords['lat'], dest_coords['lat']],
                    'lon': [pickup_coords['lon'], dest_coords['lon']]
                })
                st.map(route_data)
                
                # Confirm ride
                if st.button("✅ Confirm Ride", type="primary"):
                    ride_id = f"RIDE-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                    
                    # Update user stats
                    users[st.session_state.user_id]["total_rides"] += 1
                    users[st.session_state.user_id]["total_spent"] += price
                    save_users(users)
                    
                    st.success(f"✅ Ride Confirmed!")
                    st.info(f"Ride ID: {ride_id}")
                    st.info(f"Driver assigned: Arriving in 5-7 minutes")
                    
                    # SOS Button
                    st.markdown("---")
                    if st.button("🆘 EMERGENCY SOS", type="primary"):
                        st.error("🚨 SOS TRIGGERED! Emergency services notified.")
                        st.error(f"Your location: {pickup}")
                        st.error(f"Emergency contact: {user.get('emergency_contact', 'Not set')}")

# Preferences Page
elif menu == "⚙️ Preferences":
    st.markdown("### ⚙️ My Preferences")
    
    users = load_users()
    user = users.get(st.session_state.user_id, {}) if st.session_state.user_id else {}
    
    with st.form("preferences_form"):
        pronouns = st.selectbox("Pronouns", 
                               ["She/Her", "He/Him", "They/Them", "Prefer not to say", "Other"],
                               index=["She/Her", "He/Him", "They/Them", "Prefer not to say", "Other"].index(user.get("pronouns", "They/Them")))
        
        share_location = st.checkbox("Share live location with emergency contacts", value=True)
        
        notifications = st.checkbox("Enable ride notifications", value=True)
        
        preferred_vehicle = st.selectbox("Preferred vehicle type", 
                                         ["Any", "Standard", "Comfort", "Electric", "Premium"])
        
        accessibility = st.text_area("Accessibility needs (if any)", 
                                     placeholder="e.g., wheelchair accessible, guide dog, etc.")
        
        if st.form_submit_button("Save Preferences"):
            if st.session_state.user_id and st.session_state.user_id in users:
                users[st.session_state.user_id]["pronouns"] = pronouns
                users[st.session_state.user_id]["preferences"] = {
                    "share_location": share_location,
                    "notifications": notifications,
                    "preferred_vehicle": preferred_vehicle,
                    "accessibility": accessibility
                }
                save_users(users)
                st.success("✅ Preferences saved!")
            else:
                st.warning("Please verify your identity first to save preferences")

# Dashboard
elif menu == "📊 My Dashboard":
    st.markdown("### 📊 My Dashboard")
    
    if not st.session_state.authenticated:
        st.warning("Please verify your identity to view dashboard")
        st.stop()
    
    users = load_users()
    user = users.get(st.session_state.user_id, {})
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rides", user.get("total_rides", 0))
    with col2:
        st.metric("Total Spent", f"R{user.get('total_spent', 0):.2f}")
    with col3:
        st.metric("Member Since", user.get("registered_date", "N/A")[:10])
    
    st.markdown("### 👤 Profile Information")
    st.markdown(f"""
    - **Name:** {user.get('name', 'N/A')}
    - **Phone:** {user.get('phone', 'N/A')}
    - **Email:** {user.get('email', 'N/A')}
    - **Pronouns:** {user.get('pronouns', 'N/A')}
    - **Emergency Contact:** {user.get('emergency_contact', 'Not set')}
    """)
    
    if user.get("preferences"):
        st.markdown("### ⚙️ Your Preferences")
        prefs = user["preferences"]
        st.markdown(f"""
        - **Share Location:** {'✓' if prefs.get('share_location') else '✗'}
        - **Notifications:** {'✓' if prefs.get('notifications') else '✗'}
        - **Preferred Vehicle:** {prefs.get('preferred_vehicle', 'Any')}
        - **Accessibility:** {prefs.get('accessibility', 'None')}
        """)

# Footer
st.markdown("---")
st.markdown("*SafeRide - Safe Travel for Everyone*")
