import streamlit as st
import cv2
import numpy as np
import face_recognition
import json
import os
import datetime
import hashlib
from pathlib import Path
from PIL import Image
import io

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

st.set_page_config(
    page_title="SafeRide Biometric",
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
</style>
""", unsafe_allow_html=True)

st.title("🛡️ SafeRide Biometric")
st.markdown("*Face Recognition Based Authentication*")

DATA_DIR = Path("biometric_data")
DATA_DIR.mkdir(exist_ok=True)
USERS_FILE = DATA_DIR / "users.json"

def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

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
    is_match = distance < 0.6
    return is_match, confidence

menu = st.sidebar.selectbox("Menu", [
    "🏠 Home",
    "📝 Register",
    "🔐 Verify",
    "🚗 Request Ride"
])

if menu == "🏠 Home":
    st.markdown("### Welcome to SafeRide Biometric")
    st.info("Register with your face photo, then verify with camera for each ride")

elif menu == "📝 Register":
    st.markdown("### Biometric Registration")
    
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    uploaded_image = st.file_uploader("Upload your face photo", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_image:
        st.image(uploaded_image, caption="Registration Photo", width=200)
    
    if st.button("Register"):
        if not name or not phone:
            st.error("Please fill all fields")
        elif not uploaded_image:
            st.error("Please upload a face photo")
        else:
            with st.spinner("Processing..."):
                face_encoding, message = encode_face(uploaded_image)
                if face_encoding:
                    users = load_users()
                    user_id = hashlib.md5(name.encode()).hexdigest()[:8]
                    users[user_id] = {
                        "user_id": user_id,
                        "name": name,
                        "phone": phone,
                        "face_encoding": face_encoding,
                        "registered_date": str(datetime.datetime.now())
                    }
                    save_users(users)
                    st.success(f"✅ Registration successful! Your User ID: {user_id}")
                    st.info("Save this User ID for verification")
                else:
                    st.error(f"❌ {message}")

elif menu == "🔐 Verify":
    st.markdown("### Biometric Verification")
    
    user_id = st.text_input("Enter your User ID")
    live_photo = st.camera_input("Take a selfie")
    
    if st.button("Verify"):
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
                        stored_encoding = users[user_id]["face_encoding"]
                        is_match, confidence = verify_face(live_encoding, stored_encoding)
                        
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

elif menu == "🚗 Request Ride":
    st.markdown("### Request a Ride")
    
    if not st.session_state.authenticated:
        st.warning("Please verify your identity first")
        st.stop()
    
    st.success(f"Verified as: {st.session_state.user_name}")
    
    pickup = st.text_input("Pickup Location")
    destination = st.text_input("Destination")
    
    if st.button("Request Ride"):
        if pickup and destination:
            st.success("✅ Ride requested! Driver assigned")
            st.map({"lat": [-26.2041], "lon": [28.0473]})
        else:
            st.error("Enter both locations")
