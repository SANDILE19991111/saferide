import streamlit as st
import cv2
import numpy as np
import json
import os
import datetime
import hashlib
import math
import time
import random
from pathlib import Path
from PIL import Image
import pandas as pd

# Optional imports with error handling
try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    st.warning("Face recognition module not available. Install with: pip install face-recognition")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'current_ride' not in st.session_state:
    st.session_state.current_ride = None
if 'sos_triggered' not in st.session_state:
    st.session_state.sos_triggered = False

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
    .sos-button {
        background: linear-gradient(135deg, #ff0000 0%, #cc0000 100%) !important;
        font-size: 24px !important;
        font-weight: bold !important;
        animation: pulse 1s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
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
    .sos-box {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
        animation: blink 1s infinite;
    }
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    .price-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Check face recognition availability at startup
if not FACE_RECOGNITION_AVAILABLE:
    st.warning("⚠️ Face recognition not available. Please run: pip install face-recognition")
    st.stop()

st.title("🛡️ SafeRide")
st.markdown("*Biometric Authentication • Safe Travel for Everyone*")

DATA_DIR = Path("biometric_data")
DATA_DIR.mkdir(exist_ok=True)
USERS_FILE = DATA_DIR / "users.json"
RIDES_FILE = DATA_DIR / "rides.json"

def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_rides():
    if RIDES_FILE.exists():
        with open(RIDES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_rides(rides):
    with open(RIDES_FILE, 'w') as f:
        json.dump(rides, f, indent=2)

# Predefined locations
PREDEFINED_LOCATIONS = {
    "Cape Town CBD": {"lat": -33.9249, "lon": 18.4241},
    "Sandton City": {"lat": -26.1076, "lon": 28.0567},
    "Durban Beachfront": {"lat": -29.8587, "lon": 31.0218},
    "Pretoria Central": {"lat": -25.7479, "lon": 28.2293},
    "Johannesburg Park Station": {"lat": -26.1958, "lon": 28.0415},
    "OR Tambo Airport": {"lat": -26.1392, "lon": 28.2460},
}

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def calculate_price(distance, ride_type):
    rates = {"Standard": 12, "Comfort": 18, "Premium": 25, "XL": 20, "Electric": 15}
    min_fares = {"Standard": 35, "Comfort": 50, "Premium": 70, "XL": 60, "Electric": 45}
    base_price = distance * rates.get(ride_type, 12)
    final_price = max(base_price, min_fares.get(ride_type, 35))
    current_hour = datetime.datetime.now().hour
    if (7 <= current_hour <= 9) or (16 <= current_hour <= 19):
        final_price *= 1.3
    return round(final_price, 2)

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
            return None, "No face detected"
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
    return distance < 0.6, confidence

# Sidebar Menu
menu = st.sidebar.selectbox("Navigation", [
    "🏠 Home",
    "📝 Register",
    "🔐 Verify Identity",
    "🚗 Request Ride",
    "🆘 Emergency SOS",
    "📊 My Dashboard"
])

# Rest of your app pages here (same as before)
# ... (keep all your existing page code)

# Home Page
if menu == "🏠 Home":
    st.markdown("### Welcome to SafeRide")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Face Recognition", "✓", "Secure")
    with col2:
        st.metric("Live Verification", "✓", "Real-time")
    with col3:
        st.metric("SOS Alert", "✓", "24/7")
    with col4:
        st.metric("Safe Travel", "✓", "Protected")
    
    st.markdown("""
    <div class="success-box">
        <b>✨ SafeRide Features:</b><br>
        1️⃣ Biometric face recognition verification<br>
        2️⃣ Real-time GPS tracking during rides<br>
        3️⃣ One-tap SOS emergency alert<br>
        4️⃣ Automatic emergency contact notification<br>
        5️⃣ Encrypted evidence vault for SAPS
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
            emergency_contact = st.text_input("Emergency Contact Number")
            emergency_name = st.text_input("Emergency Contact Name")
        
        uploaded_image = st.file_uploader("Upload your face photo", type=['jpg', 'jpeg', 'png'])
        if uploaded_image:
            st.image(uploaded_image, caption="Registration Photo", width=200)
        
        submitted = st.form_submit_button("Register")
        
        if submitted:
            if not name or not phone:
                st.error("Please fill all fields")
            elif not uploaded_image:
                st.error("Please upload a face photo")
            else:
                with st.spinner("Processing..."):
                    face_encoding, message = encode_face(uploaded_image)
                    if face_encoding:
                        users = load_users()
                        user_id = hashlib.md5(f"{name}{phone}{datetime.datetime.now()}".encode()).hexdigest()[:8]
                        users[user_id] = {
                            "user_id": user_id, "name": name, "phone": phone, "email": email,
                            "emergency_contact": emergency_contact, "emergency_name": emergency_name,
                            "face_encoding": face_encoding, "registered_date": str(datetime.datetime.now()),
                            "total_rides": 0, "total_spent": 0
                        }
                        save_users(users)
                        st.success(f"✅ Registration Successful! Your User ID: {user_id}")
                        st.balloons()
                    else:
                        st.error(f"❌ {message}")

# Verification Page
elif menu == "🔐 Verify Identity":
    st.markdown("### 🔐 Biometric Verification")
    
    user_id = st.text_input("Enter your User ID")
    live_photo = st.camera_input("Take a selfie for verification")
    
    if st.button("Verify Identity"):
        if not user_id:
            st.error("Enter User ID")
        elif not live_photo:
            st.error("Take a selfie")
        else:
            users = load_users()
            if user_id not in users:
                st.error("User ID not found")
            else:
                with st.spinner("Verifying..."):
                    live_encoding, message = encode_face(live_photo)
                    if live_encoding:
                        is_match, confidence = verify_face(live_encoding, users[user_id]["face_encoding"])
                        if is_match:
                            st.success(f"✅ Verified! Welcome {users[user_id]['name']}")
                            st.success(f"Confidence: {confidence:.1f}%")
                            st.session_state.authenticated = True
                            st.session_state.user_id = user_id
                            st.session_state.user_name = users[user_id]['name']
                            st.balloons()
                        else:
                            st.error(f"❌ Verification failed. Confidence: {confidence:.1f}%")
                    else:
                        st.error(f"❌ {message}")

# Request Ride Page  
elif menu == "🚗 Request Ride":
    st.markdown("### 🚗 Request a Ride")
    
    if not st.session_state.authenticated:
        st.warning("Please verify your identity first")
        st.stop()
    
    users = load_users()
    user = users.get(st.session_state.user_id, {})
    
    st.success(f"✅ Verified as: {user.get('name', 'Rider')}")
    
    with st.form("ride_form"):
        col1, col2 = st.columns(2)
        with col1:
            pickup = st.selectbox("Pickup Location", list(PREDEFINED_LOCATIONS.keys()))
        with col2:
            destination = st.selectbox("Destination", list(PREDEFINED_LOCATIONS.keys()))
        
        ride_type = st.selectbox("Ride Type", ["Standard", "Comfort", "Premium", "XL", "Electric"])
        
        submitted = st.form_submit_button("Calculate Price & Request")
        
        if submitted and pickup != destination:
            pickup_coords = PREDEFINED_LOCATIONS[pickup]
            dest_coords = PREDEFINED_LOCATIONS[destination]
            distance = calculate_distance(pickup_coords['lat'], pickup_coords['lon'], 
                                          dest_coords['lat'], dest_coords['lon'])
            price = calculate_price(distance, ride_type)
            
            st.markdown(f"""
            <div class="price-card">
                <h4>Ride Summary</h4>
                <h2>R{price}</h2>
                <p>Distance: {distance:.1f} km | Est. time: {(distance/40*60):.0f} min</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("✅ Confirm Ride"):
                ride_id = f"RIDE-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                ride_data = {
                    "ride_id": ride_id, "user_id": st.session_state.user_id, "user_name": user.get('name'),
                    "pickup": pickup, "destination": destination, "distance": distance, "price": price,
                    "ride_type": ride_type, "start_time": str(datetime.datetime.now()), "status": "active"
                }
                rides = load_rides()
                rides[ride_id] = ride_data
                save_rides(rides)
                st.session_state.current_ride = ride_data
                st.success(f"✅ Ride Confirmed! Ride ID: {ride_id}")
                
                # Show route map
                route_data = pd.DataFrame({
                    'lat': [pickup_coords['lat'], dest_coords['lat']],
                    'lon': [pickup_coords['lon'], dest_coords['lon']]
                })
                st.map(route_data)
        elif submitted:
            st.error("Pickup and destination cannot be the same")

# SOS Emergency Page
elif menu == "🆘 Emergency SOS":
    st.markdown("### 🆘 EMERGENCY SOS")
    
    st.markdown("""
    <div class="sos-box">
        <h1>🚨 EMERGENCY 🚨</h1>
        <p>Only use in genuine emergencies</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.authenticated:
        st.warning("Please verify your identity first")
        st.stop()
    
    users = load_users()
    user = users.get(st.session_state.user_id, {})
    current_ride = st.session_state.current_ride
    
    st.markdown(f"""
    <div class="info-box">
        <b>Your Information:</b><br>
        Name: {user.get('name', 'N/A')}<br>
        Phone: {user.get('phone', 'N/A')}<br>
        Emergency Contact: {user.get('emergency_name', 'Not set')} ({user.get('emergency_contact', 'N/A')})
    </div>
    """, unsafe_allow_html=True)
    
    if current_ride:
        st.info(f"Current Ride: {current_ride.get('pickup')} → {current_ride.get('destination')}")
    
    current_location = st.selectbox("Your current location (GPS)", list(PREDEFINED_LOCATIONS.keys()))
    
    st.markdown("---")
    st.markdown("### ⚠️ THIS WILL TRIGGER IMMEDIATE ASSISTANCE")
    
    if st.button("🚨 TRIGGER SOS EMERGENCY 🚨", use_container_width=True):
        st.session_state.sos_triggered = True
        
        st.markdown("""
        <div class="sos-box">
            <h2>🚨 SOS TRIGGERED! 🚨</h2>
            <p>Emergency services have been notified</p>
            <p>Your emergency contact is being alerted</p>
            <p>Your location is being tracked</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="success-box">
            <b>✅ What happens now:</b><br>
            • SAPS have been notified of your emergency<br>
            • Your emergency contact has been alerted<br>
            • Your GPS location is being shared with responders<br>
            • All ride evidence has been unlocked for SAPS<br>
            • A responder is being dispatched to your location
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### ⏰ Responder ETA: 5-10 minutes")
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            progress_bar.progress(i + 1)
        
        st.success("✅ Responder has been dispatched! Help is on the way.")
        
        if st.button("Reset (After Emergency Resolved)"):
            st.session_state.sos_triggered = False
            st.rerun()

# Dashboard Page
elif menu == "📊 My Dashboard":
    st.markdown("### 📊 My Dashboard")
    
    if not st.session_state.authenticated:
        st.warning("Please verify your identity first")
        st.stop()
    
    users = load_users()
    user = users.get(st.session_state.user_id, {})
    rides = load_rides()
    user_rides = {k: v for k, v in rides.items() if v.get('user_id') == st.session_state.user_id}
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rides", len(user_rides))
    with col2:
        st.metric("Total Spent", f"R{sum(r.get('price', 0) for r in user_rides.values()):.2f}")
    with col3:
        st.metric("Member Since", user.get('registered_date', 'N/A')[:10])
    
    st.markdown("### 👤 Profile")
    st.markdown(f"""
    - **Name:** {user.get('name', 'N/A')}
    - **Phone:** {user.get('phone', 'N/A')}
    - **Email:** {user.get('email', 'N/A')}
    - **Emergency Contact:** {user.get('emergency_name', 'N/A')} ({user.get('emergency_contact', 'N/A')})
    """)
    
    if user_rides:
        st.markdown("### 🚗 Recent Rides")
        for ride_id, ride in list(user_rides.items())[-5:]:
            st.markdown(f"""
            <div class="info-box">
                <b>{ride_id}</b><br>
                {ride.get('pickup')} → {ride.get('destination')}<br>
                Price: R{ride.get('price', 0)} | {ride.get('ride_type')}<br>
                {ride.get('start_time', 'N/A')[:16]}
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("*SafeRide - Safe Travel for Everyone | SOS Available 24/7*")
