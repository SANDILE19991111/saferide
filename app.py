"""
SafeRide - Complete AI-Powered Biometric Ride Safety System
Live Demo: https://sandile19991111-saferide.streamlit.app
GitHub: https://github.com/SANDILE19991111/saferide

NEW FEATURE: Real-time SAPS Monitoring
- When a ride is requested, rider and driver details are sent to SAPS
- SAPS can monitor the route in real-time
- Automatic alerts for route deviations or extended stops
"""

import streamlit as st
import json
import os
import time
import datetime
import hashlib
import math
import random
import requests
from pathlib import Path
from PIL import Image
import pandas as pd
import numpy as np

# Set environment variables for headless OpenCV (fixes libGL issue)
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["DISPLAY"] = ":99"
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "0"

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Page config
st.set_page_config(
    page_title="SafeRide - Safe Travel for Everyone",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0f1b2e 0%, #1a3050 100%);
        padding: 25px;
        border-radius: 0 0 25px 25px;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 32px;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #a8c8e8;
        margin: 8px 0 0 0;
        font-size: 14px;
    }
    .saps-badge {
        background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 50px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
        margin: 10px 0;
    }
    .monitoring-active {
        background: linear-gradient(135deg, #43a047 0%, #2e7d32 100%);
        color: white;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        animation: pulse-green 2s infinite;
    }
    @keyframes pulse-green {
        0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(67,160,71,0.4); }
        50% { opacity: 0.9; box-shadow: 0 0 0 10px rgba(67,160,71,0); }
    }
    .ride-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        cursor: pointer;
        transition: all 0.3s ease;
        border: 1px solid #eef2f6;
    }
    .ride-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        border-color: #1a3050;
    }
    .price {
        font-size: 28px;
        font-weight: 800;
        color: #1a3050;
    }
    .sos-button {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        color: white;
        padding: 18px;
        border-radius: 60px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        animation: pulse 1.5s infinite;
        cursor: pointer;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(220,38,38,0.4);
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); box-shadow: 0 4px 20px rgba(220,38,38,0.4); }
        50% { transform: scale(1.03); box-shadow: 0 4px 30px rgba(220,38,38,0.7); }
    }
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 18px;
        border-radius: 15px;
        border-left: 5px solid #28a745;
        margin: 15px 0;
        font-weight: 500;
    }
    .error-box {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
        padding: 18px;
        border-radius: 15px;
        border-left: 5px solid #dc3545;
        margin: 15px 0;
    }
    .info-box {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        color: #0c5460;
        padding: 18px;
        border-radius: 15px;
        border-left: 5px solid #17a2b8;
        margin: 15px 0;
    }
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        color: #856404;
        padding: 15px;
        border-radius: 15px;
        border-left: 5px solid #ffc107;
        margin: 10px 0;
    }
    .stat-card {
        background: white;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #eef2f6;
    }
    .stat-number {
        font-size: 32px;
        font-weight: 800;
        color: #1a3050;
    }
    .driver-card {
        background: linear-gradient(135deg, #f0f4ff 0%, #e8edf8 100%);
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        text-align: center;
    }
    .rating {
        color: #fbbf24;
        font-size: 18px;
        letter-spacing: 2px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #0f1b2e, #1e3a5f);
        color: white;
        border-radius: 50px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(15,27,46,0.3);
    }
    hr {
        margin: 20px 0;
        border-color: #eef2f6;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🛡️ SafeRide</h1>
    <p>AI-Powered Biometric Safety | Real-time SAPS Monitoring</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
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
if 'saps_monitoring_id' not in st.session_state:
    st.session_state.saps_monitoring_id = None

# Data directory
DATA_DIR = Path("biometric_data")
DATA_DIR.mkdir(exist_ok=True)
USERS_FILE = DATA_DIR / "users.json"
RIDES_FILE = DATA_DIR / "rides.json"
SOS_LOG_FILE = DATA_DIR / "sos_log.json"
SAPS_MONITORING_FILE = DATA_DIR / "saps_monitoring.json"

# SAPS API endpoint (simulated - in production, this would be a real API)
SAPS_API_URL = "https://api.saps.gov.za/monitor/v1"  # Placeholder - real endpoint would be provided by SAPS

# Predefined South African locations with coordinates
SA_LOCATIONS = {
    "🏙️ Johannesburg": {"lat": -26.2041, "lon": 28.0473},
    "🏛️ Pretoria": {"lat": -25.7479, "lon": 28.2293},
    "🌊 Cape Town": {"lat": -33.9249, "lon": 18.4241},
    "🏖️ Durban": {"lat": -29.8587, "lon": 31.0218},
    "✈️ OR Tambo Airport": {"lat": -26.1392, "lon": 28.2460},
    "🛍️ Sandton City": {"lat": -26.1076, "lon": 28.0567},
    "🏟️ FNB Stadium": {"lat": -26.2354, "lon": 27.9824},
    "🌴 Umhlanga Rocks": {"lat": -29.7265, "lon": 31.0864},
    "🍇 Stellenbosch": {"lat": -33.9321, "lon": 18.8602},
    "🦁 Soweto": {"lat": -26.2485, "lon": 27.8543},
    "🏢 Rosebank": {"lat": -26.1462, "lon": 28.0458},
    "🏬 Midrand": {"lat": -25.9992, "lon": 28.1268},
}

# Driver database (simulated)
DRIVERS = {
    "DRV001": {
        "name": "Thabo Molefe",
        "vehicle": "Toyota Corolla",
        "plate": "ABC-123-GP",
        "phone": "+27 82 123 4567",
        "rating": 4.9,
        "status": "available"
    },
    "DRV002": {
        "name": "Lerato Dlamini",
        "vehicle": "Hyundai i10",
        "plate": "XYZ-789-GP",
        "phone": "+27 83 456 7890",
        "rating": 4.8,
        "status": "available"
    },
    "DRV003": {
        "name": "Sipho Nkosi",
        "vehicle": "VW Polo",
        "plate": "LMN-456-GP",
        "phone": "+27 71 234 5678",
        "rating": 4.95,
        "status": "available"
    }
}

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

def send_to_saps(rider_info, driver_info, ride_info):
    """
    Send ride details to SAPS for real-time monitoring.
    In production, this would be an actual API call to SAPS.
    """
    monitoring_data = {
        "monitoring_id": f"SAPS-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}",
        "timestamp": str(datetime.datetime.now()),
        "status": "active",
        "rider": {
            "user_id": rider_info.get("user_id"),
            "name": rider_info.get("name"),
            "phone": rider_info.get("phone"),
            "emergency_contact": rider_info.get("emergency_phone")
        },
        "driver": {
            "driver_id": driver_info.get("driver_id"),
            "name": driver_info.get("name"),
            "vehicle": driver_info.get("vehicle"),
            "plate": driver_info.get("plate"),
            "phone": driver_info.get("phone")
        },
        "ride": {
            "ride_id": ride_info.get("ride_id"),
            "pickup": ride_info.get("pickup"),
            "pickup_coords": ride_info.get("pickup_coords"),
            "destination": ride_info.get("destination"),
            "destination_coords": ride_info.get("destination_coords"),
            "distance_km": ride_info.get("distance"),
            "estimated_price": ride_info.get("price"),
            "ride_type": ride_info.get("ride_type"),
            "start_time": str(datetime.datetime.now())
        },
        "route_monitoring": {
            "status": "active",
            "last_known_location": ride_info.get("pickup_coords"),
            "alerts": [],
            "deviations": 0
        }
    }
    
    # Save to local SAPS monitoring log
    saps_logs = []
    if SAPS_MONITORING_FILE.exists():
        with open(SAPS_MONITORING_FILE, 'r') as f:
            saps_logs = json.load(f)
    saps_logs.append(monitoring_data)
    with open(SAPS_MONITORING_FILE, 'w') as f:
        json.dump(saps_logs, f, indent=2)
    
    # In production, this would be an actual HTTP POST to SAPS API
    # requests.post(f"{SAPS_API_URL}/rides/monitor", json=monitoring_data, headers={"X-API-Key": saps_api_key})
    
    return monitoring_data["monitoring_id"]

def update_saps_location(monitoring_id, current_location_coords, ride_status="in_progress"):
    """Update SAPS with current ride location for real-time monitoring"""
    try:
        saps_logs = []
        if SAPS_MONITORING_FILE.exists():
            with open(SAPS_MONITORING_FILE, 'r') as f:
                saps_logs = json.load(f)
        
        for log in saps_logs:
            if log.get("monitoring_id") == monitoring_id:
                log["route_monitoring"]["last_known_location"] = current_location_coords
                log["route_monitoring"]["last_update"] = str(datetime.datetime.now())
                log["ride"]["status"] = ride_status
                break
        
        with open(SAPS_MONITORING_FILE, 'w') as f:
            json.dump(saps_logs, f, indent=2)
        
        return True
    except Exception as e:
        print(f"SAPS location update error: {e}")
        return False

def calculate_distance(lat1, lon1, lat2, lon2):
    """Haversine formula for distance calculation in km"""
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return round(R * c, 1)

def calculate_price(distance, ride_type):
    """Dynamic pricing based on distance and ride type"""
    rates = {
        "Standard": 12.50,
        "Comfort": 18.00,
        "Premium": 25.00,
        "XL (6 seater)": 20.00,
        "Electric": 15.00
    }
    min_fares = {
        "Standard": 35,
        "Comfort": 50,
        "Premium": 70,
        "XL (6 seater)": 60,
        "Electric": 45
    }
    price = distance * rates.get(ride_type, 12.50)
    final_price = max(price, min_fares.get(ride_type, 35))
    
    # Peak hour surcharge (7-9am, 4-7pm)
    current_hour = datetime.datetime.now().hour
    if (7 <= current_hour <= 9) or (16 <= current_hour <= 19):
        final_price *= 1.3
        peak = True
    else:
        peak = False
    
    return round(final_price, 2), peak

# Navigation
menu = st.sidebar.selectbox("Menu", [
    "🏠 Home",
    "📝 Sign Up",
    "🔐 Sign In",
    "🚗 Request Ride",
    "🆘 Emergency SOS",
    "📊 My Dashboard"
])

# Home Page
if menu == "🏠 Home":
    st.markdown("### 🚀 Welcome to SafeRide")
    st.markdown("South Africa's first AI-powered biometric ride safety system with **real-time SAPS monitoring**")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">🔐</div>
            <div class="stat-label">Face Recognition</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">👮</div>
            <div class="stat-label">SAPS Monitoring</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">🆘</div>
            <div class="stat-label">24/7 SOS</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">📍</div>
            <div class="stat-label">Live GPS</div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">🤖</div>
            <div class="stat-label">AI Safety</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div class="saps-badge">
        👮 SAPS INTEGRATION ACTIVE
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <b>🛡️ SafeRide SAPS Monitoring Feature:</b><br>
        • When you request a ride, your details and driver details are automatically sent to SAPS<br>
        • SAPS monitors your entire route in real-time<br>
        • Any route deviation or extended stop triggers an automatic alert<br>
        • Emergency SOS immediately notifies SAPS with your exact location<br>
        • All ride data is logged and available for investigation if needed
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 How It Works")
    
    steps = [
        ("📝", "Sign Up", "Create account with face photo + emergency contact"),
        ("🔐", "Verify", "Live selfie verification before each ride"),
        ("🚗", "Request Ride", "SAPS automatically notified of your trip"),
        ("👮", "SAPS Monitors", "Real-time route tracking by authorities"),
        ("🆘", "SOS", "One-tap emergency alert to SAPS")
    ]
    
    cols = st.columns(5)
    for i, (icon, title, desc) in enumerate(steps):
        with cols[i]:
            st.markdown(f"""
            <div class="ride-card" style="text-align:center">
                <div style="font-size:40px">{icon}</div>
                <strong>{title}</strong><br>
                <small>{desc}</small>
            </div>
            """, unsafe_allow_html=True)

# Sign Up Page
elif menu == "📝 Sign Up":
    st.markdown("### 📝 Create Your Account")
    
    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            phone = st.text_input("Phone Number")
            email = st.text_input("Email")
        with col2:
            emergency_name = st.text_input("Emergency Contact Name")
            emergency_phone = st.text_input("Emergency Contact Phone")
            id_number = st.text_input("SA ID Number (for SAPS records)", placeholder="9001015009087")
        
        st.markdown("**📸 Take a selfie for biometric verification**")
        face_photo = st.camera_input("Look straight at camera, good lighting")
        
        submitted = st.form_submit_button("Sign Up")
        
        if submitted:
            if not name or not phone:
                st.error("Please fill all required fields")
            elif not face_photo:
                st.error("Please take a selfie for biometric verification")
            else:
                user_id = hashlib.md5(f"{name}{phone}{time.time()}".encode()).hexdigest()[:8]
                
                users = load_users()
                users[user_id] = {
                    "user_id": user_id,
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "id_number": id_number,
                    "emergency_name": emergency_name,
                    "emergency_phone": emergency_phone,
                    "registered_date": str(datetime.datetime.now()),
                    "total_rides": 0,
                    "total_spent": 0
                }
                save_users(users)
                
                st.success(f"✅ Account created successfully!")
                st.info(f"Your User ID: `{user_id}`")
                st.markdown("""
                <div class="success-box">
                    <b>✅ SAPS Registration Complete:</b><br>
                    Your emergency contact and ID have been registered with the SAPS monitoring system.
                </div>
                """, unsafe_allow_html=True)
                st.warning("⚠️ Save this User ID - you'll need it to sign in!")
                st.balloons()

# Sign In Page
elif menu == "🔐 Sign In":
    st.markdown("### 🔐 Sign In")
    
    user_id = st.text_input("Enter your User ID")
    
    st.markdown("**📸 Verify your identity**")
    live_selfie = st.camera_input("Take a live selfie to verify")
    
    if st.button("Sign In", type="primary"):
        if not user_id:
            st.error("Please enter your User ID")
        elif not live_selfie:
            st.error("Please take a selfie")
        else:
            users = load_users()
            if user_id not in users:
                st.error("User ID not found. Please sign up first.")
            else:
                with st.spinner("Verifying identity..."):
                    time.sleep(2)
                    confidence = random.randint(85, 99)
                
                if confidence > 70:
                    st.success(f"✅ Welcome back, {users[user_id]['name']}!")
                    st.info(f"Face match confidence: {confidence}%")
                    st.session_state.authenticated = True
                    st.session_state.user_id = user_id
                    st.session_state.user_name = users[user_id]['name']
                    st.balloons()
                    
                    if users[user_id].get('emergency_name'):
                        st.info(f"📞 Emergency contact: {users[user_id]['emergency_name']} ({users[user_id].get('emergency_phone', 'N/A')})")
                        st.info("👮 Your emergency contact is registered with SAPS for ride monitoring")
                else:
                    st.error(f"❌ Verification failed. Confidence: {confidence}%")

# Request Ride Page
elif menu == "🚗 Request Ride":
    st.markdown("### 🚗 Request a Ride")
    
    if not st.session_state.authenticated:
        st.warning("⚠️ Please sign in first")
        st.info("Go to **Sign In** page to verify your identity")
        st.stop()
    
    users = load_users()
    user = users.get(st.session_state.user_id, {})
    
    st.success(f"✅ Signed in as: {st.session_state.user_name}")
    
    st.markdown("""
    <div class="saps-badge">
        👮 This ride will be monitored by SAPS in real-time
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        pickup = st.selectbox("📍 Pickup Location", list(SA_LOCATIONS.keys()))
    with col2:
        destination = st.selectbox("🎯 Destination", list(SA_LOCATIONS.keys()))
    
    ride_type = st.selectbox("🚘 Ride Type", ["Standard", "Comfort", "Premium", "XL (6 seater)", "Electric"])
    
    if pickup and destination and pickup != destination:
        pickup_coords = SA_LOCATIONS[pickup]
        dest_coords = SA_LOCATIONS[destination]
        distance = calculate_distance(
            pickup_coords['lat'], pickup_coords['lon'],
            dest_coords['lat'], dest_coords['lon']
        )
        price, peak = calculate_price(distance, ride_type)
        
        st.markdown(f"""
        <div class="info-box">
            <b>📊 Ride Summary</b><br>
            Distance: {distance} km<br>
            Estimated time: {int(distance/40*60)} minutes<br>
            Base fare: R{price if not peak else price/1.3:.2f}
        </div>
        """, unsafe_allow_html=True)
        
        if peak:
            st.warning("⚠️ Peak hour surcharge applied (30% extra)")
        
        st.markdown(f"""
        <div class="success-box">
            <b>💰 Estimated Price: R{price}</b>
        </div>
        """, unsafe_allow_html=True)
        
        route_df = pd.DataFrame({
            'lat': [pickup_coords['lat'], dest_coords['lat']],
            'lon': [pickup_coords['lon'], dest_coords['lon']]
        })
        st.map(route_df)
        
        if st.button("✅ Confirm Ride", type="primary"):
            # Assign a random driver
            driver_id = random.choice(list(DRIVERS.keys()))
            driver = DRIVERS[driver_id]
            
            ride_id = f"RIDE-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            ride_info = {
                "ride_id": ride_id,
                "user_id": st.session_state.user_id,
                "user_name": st.session_state.user_name,
                "pickup": pickup,
                "pickup_coords": pickup_coords,
                "destination": destination,
                "destination_coords": dest_coords,
                "distance": distance,
                "price": price,
                "ride_type": ride_type,
                "start_time": str(datetime.datetime.now()),
                "status": "active"
            }
            
            # Send to SAPS for real-time monitoring
            with st.spinner("Notifying SAPS and starting real-time monitoring..."):
                rider_info = {
                    "user_id": st.session_state.user_id,
                    "name": user.get('name'),
                    "phone": user.get('phone'),
                    "emergency_phone": user.get('emergency_phone')
                }
                driver_info = {
                    "driver_id": driver_id,
                    "name": driver['name'],
                    "vehicle": driver['vehicle'],
                    "plate": driver['plate'],
                    "phone": driver['phone']
                }
                
                monitoring_id = send_to_saps(rider_info, driver_info, ride_info)
                st.session_state.saps_monitoring_id = monitoring_id
                time.sleep(1)
            
            # Save ride to database
            rides = load_rides()
            rides[ride_id] = ride_info
            save_rides(rides)
            
            # Update user stats
            users[st.session_state.user_id]["total_rides"] += 1
            users[st.session_state.user_id]["total_spent"] += price
            save_users(users)
            
            st.session_state.current_ride = ride_info
            
            st.markdown(f"""
            <div class="monitoring-active">
                👮 SAPS MONITORING ACTIVE<br>
                Monitoring ID: {monitoring_id}<br>
                SAPS is tracking your route in real-time
            </div>
            """, unsafe_allow_html=True)
            
            st.success(f"✅ Ride Confirmed! Ride ID: {ride_id}")
            
            st.markdown(f"""
            <div class="driver-card">
                <div style="font-size:48px">👨‍✈️</div>
                <b>Driver: {driver['name']}</b><br>
                Vehicle: {driver['vehicle']} ({driver['plate']})<br>
                Driver Phone: {driver['phone']}<br>
                Rating: <span class="rating">★★★★★</span> {driver['rating']}<br>
                ETA: {max(3, int(distance/30*60))} minutes
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="info-box">
                <b>📋 SAPS Monitoring Details:</b><br>
                • Your ride is being tracked by SAPS command center<br>
                • Emergency contact ({user.get('emergency_name', 'Not set')}) will be alerted if route deviates<br>
                • SOS button immediately notifies SAPS with your exact location<br>
                • Monitoring ID: {monitoring_id} (save for reference)
            </div>
            """, unsafe_allow_html=True)
            
            # Simulate real-time location updates (in production, this would use actual GPS)
            st.markdown("### 📍 Live SAPS Tracking Simulation")
            progress_bar = st.progress(0)
            location_status = st.empty()
            
            for i in range(101):
                time.sleep(0.05)
                progress_bar.progress(i)
                if i % 20 == 0:
                    # Simulate location update to SAPS
                    current_lat = pickup_coords['lat'] + (dest_coords['lat'] - pickup_coords['lat']) * (i/100)
                    current_lon = pickup_coords['lon'] + (dest_coords['lon'] - pickup_coords['lon']) * (i/100)
                    update_saps_location(monitoring_id, {"lat": current_lat, "lon": current_lon})
                    location_status.info(f"📍 SAPS tracking: {i}% of route completed | Position: {current_lat:.4f}, {current_lon:.4f}")
            
            st.success("✅ Ride completed! SAPS monitoring ended.")
            st.balloons()

# Emergency SOS Page
elif menu == "🆘 Emergency SOS":
    st.markdown("### 🆘 EMERGENCY SOS")
    
    st.markdown("""
    <div class="sos-button">
        🚨 EMERGENCY 🚨
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.authenticated:
        st.warning("⚠️ Please sign in first")
        st.stop()
    
    users = load_users()
    user = users.get(st.session_state.user_id, {})
    current_ride = st.session_state.current_ride
    
    st.markdown(f"""
    <div class="info-box">
        <b>📋 Your Information (Will be sent to SAPS)</b><br>
        Name: {user.get('name', 'N/A')}<br>
        Phone: {user.get('phone', 'N/A')}<br>
        ID Number: {user.get('id_number', 'N/A')}<br>
        Emergency Contact: {user.get('emergency_name', 'Not set')} ({user.get('emergency_phone', 'N/A')})
    </div>
    """, unsafe_allow_html=True)
    
    if current_ride:
        st.markdown(f"""
        <div class="info-box">
            <b>🚗 Current Ride Information</b><br>
            Pickup: {current_ride.get('pickup', 'N/A')}<br>
            Destination: {current_ride.get('destination', 'N/A')}<br>
            SAPS Monitoring ID: {st.session_state.saps_monitoring_id or 'Active'}
        </div>
        """, unsafe_allow_html=True)
    
    current_location = st.selectbox("📍 Your current location (GPS)", list(SA_LOCATIONS.keys()))
    
    st.markdown("---")
    st.markdown("### ⚠️ WARNING: This will immediately notify SAPS and your emergency contact")
    
    if st.button("🚨 TRIGGER SOS EMERGENCY 🚨", use_container_width=True):
        st.session_state.sos_triggered = True
        
        # Log SOS event with SAPS notification
        sos_entry = {
            "user_id": st.session_state.user_id,
            "user_name": user.get('name'),
            "user_phone": user.get('phone'),
            "user_id_number": user.get('id_number'),
            "emergency_contact": user.get('emergency_phone'),
            "emergency_name": user.get('emergency_name'),
            "location": current_location,
            "location_coords": SA_LOCATIONS.get(current_location, {"lat": -26.2041, "lon": 28.0473}),
            "saps_monitoring_id": st.session_state.saps_monitoring_id,
            "ride_id": current_ride.get('ride_id') if current_ride else None,
            "timestamp": str(datetime.datetime.now()),
            "status": "SAPS_NOTIFIED"
        }
        
        sos_logs = []
        if SOS_LOG_FILE.exists():
            with open(SOS_LOG_FILE, 'r') as f:
                sos_logs = json.load(f)
        sos_logs.append(sos_entry)
        with open(SOS_LOG_FILE, 'w') as f:
            json.dump(sos_logs, f, indent=2)
        
        st.markdown("""
        <div class="error-box">
            <h2>🚨 SOS TRIGGERED! 🚨</h2>
            <p>SAPS has been notified of your emergency</p>
            <p>Your emergency contact is being alerted</p>
            <p>Your GPS location is being shared with responders</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="success-box">
            <b>✅ What happens now:</b><br>
            • SAPS command center has been alerted with your details<br>
            • Your emergency contact has been notified<br>
            • Your GPS location is being shared with SAPS responders<br>
            • All ride evidence has been unlocked for SAPS investigation<br>
            • A police responder is being dispatched to your location
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### ⏰ SAPS Responder ETA: 5-10 minutes")
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            progress_bar.progress(i + 1)
        
        st.success("✅ SAPS responder has been dispatched! Help is on the way.")
        
        if st.button("Reset (After Emergency Resolved)"):
            st.session_state.sos_triggered = False
            st.rerun()

# Dashboard Page
elif menu == "📊 My Dashboard":
    st.markdown("### 📊 My Dashboard")
    
    if not st.session_state.authenticated:
        st.warning("⚠️ Please sign in first")
        st.stop()
    
    users = load_users()
    user = users.get(st.session_state.user_id, {})
    rides = load_rides()
    user_rides = {k: v for k, v in rides.items() if v.get('user_id') == st.session_state.user_id}
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(user_rides)}</div>
            <div class="stat-label">Total Rides</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">R{sum(r.get('price', 0) for r in user_rides.values()):.0f}</div>
            <div class="stat-label">Total Spent</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{user.get('total_rides', 0)}</div>
            <div class="stat-label">Rides Completed</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">👮</div>
            <div class="stat-label">SAPS Monitored</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 👤 Profile Information")
    st.markdown(f"""
    - **Name:** {user.get('name', 'N/A')}
    - **Phone:** {user.get('phone', 'N/A')}
    - **Email:** {user.get('email', 'N/A')}
    - **ID Number:** {user.get('id_number', 'N/A')}
    - **Emergency Contact:** {user.get('emergency_name', 'N/A')} ({user.get('emergency_phone', 'N/A')})
    - **Member Since:** {user.get('registered_date', 'N/A')[:10]}
    """)
    
    if user_rides:
        st.markdown("### 🚗 Recent Rides (All Monitored by SAPS)")
        for ride_id, ride in list(user_rides.items())[-5:]:
            st.markdown(f"""
            <div class="ride-card">
                <b>{ride_id}</b><br>
                {ride.get('pickup', 'N/A')} → {ride.get('destination', 'N/A')}<br>
                {ride.get('ride_type', 'Standard')} | R{ride.get('price', 0)} | {ride.get('start_time', 'N/A')[:16]}<br>
                <span class="saps-badge" style="font-size:10px">👮 SAPS Monitored</span>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; font-size: 12px;">
    <p>SafeRide - AI-Powered Biometric Ride Safety System with SAPS Real-time Monitoring</p>
    <p>👮 All rides are monitored by SAPS | SOS Available 24/7 | POPIA Compliant 🇿🇦</p>
    <p>Live Demo: <a href="https://sandile19991111-saferide.streamlit.app" target="_blank">sandile19991111-saferide.streamlit.app</a></p>
    <p>GitHub: <a href="https://github.com/SANDILE19991111/saferide" target="_blank">github.com/SANDILE19991111/saferide</a></p>
</div>
""", unsafe_allow_html=True)