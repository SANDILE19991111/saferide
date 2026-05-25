import streamlit as st

st.set_page_config(page_title="SafeRide", page_icon="🛡️")

st.title("🛡️ SafeRide")
st.write("Your Safety Companion")

# Navigation
page = st.selectbox("Menu", [
    "Home",
    "Register", 
    "Verify",
    "Request Ride"
])

# Session state
if 'verified' not in st.session_state:
    st.session_state.verified = False
if 'rider_name' not in st.session_state:
    st.session_state.rider_name = ""

if page == "Home":
    st.write("### Welcome to SafeRide")
    st.write("SafeRide helps women travel safely with biometric verification.")

elif page == "Register":
    st.subheader("Register as a Rider")
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    if st.button("Register"):
        if name:
            st.success(f"Welcome {name}! Registration successful.")
            st.session_state.rider_name = name
        else:
            st.error("Please enter your name")

elif page == "Verify":
    st.subheader("Verify Your Identity")
    if st.button("Verify Now"):
        st.balloons()
        st.success("Identity verified successfully!")
        st.session_state.verified = True

elif page == "Request Ride":
    st.subheader("Request a Ride")
    
    if not st.session_state.verified:
        st.warning("⚠️ Please verify your identity first.")
        st.info("Go to 'Verify' page first.")
        st.stop()
    
    st.success(f"Verified as: {st.session_state.rider_name}")
    
    pickup = st.text_input("Pickup Location")
    destination = st.text_input("Destination")
    
    if st.button("Request Ride Now"):
        if pickup and destination:
            ride_id = "RIDE-" + str(hash(pickup + destination))[-6:]
            st.success(f"✅ Ride {ride_id} requested!")
            st.info("Driver: Thabo (Toyota Corolla)")
            st.info("ETA: 5-7 minutes")
            st.map({"lat": [-26.2041], "lon": [28.0473]})
        else:
            st.error("Please enter both locations")
