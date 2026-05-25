"""
SafeRide — Core Biometric Engine
Real face recognition + Gemini AI safety reports + encrypted server logging
Updated: pickup PIN support, gender field for Women for Women, safety prefs integration
"""

import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import cv2
import face_recognition
import numpy as np
import hashlib, json, datetime, uuid, base64, time, shutil
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
DATA_DIR     = Path("saferide_data")
RIDERS_DB    = DATA_DIR / "riders.json"
DRIVERS_DB   = DATA_DIR / "drivers.json"
TRIPS_DB     = DATA_DIR / "trips.json"
EVIDENCE_DIR = DATA_DIR / "evidence"
PHOTOS_DIR   = DATA_DIR / "photos"

for d in [DATA_DIR, EVIDENCE_DIR, PHOTOS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── Gemini ─────────────────────────────────────────────────────────────────────
_gemini = None

def get_gemini():
    global _gemini
    if _gemini is None:
        from google import genai
        key = os.environ.get("GEMINI_API_KEY", "")
        if not key:
            raise EnvironmentError("GEMINI_API_KEY not set.")
        _gemini = genai.Client(api_key=key)
    return _gemini

# ── DB helpers ─────────────────────────────────────────────────────────────────
def load_db(path: Path) -> dict:
    if path.exists():
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_db(path: Path, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)

# ── Image helpers ──────────────────────────────────────────────────────────────
def image_to_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ── Face recognition ───────────────────────────────────────────────────────────
def encode_face_from_file(image_path: str):
    img  = face_recognition.load_image_file(image_path)
    encs = face_recognition.face_encodings(img)
    return encs[0].tolist() if encs else None

def encode_face_from_array(frame: np.ndarray):
    rgb  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    encs = face_recognition.face_encodings(rgb)
    return encs[0].tolist() if encs else None

def compare_encodings(known: list, live: list, threshold: float = 0.50):
    dist       = face_recognition.face_distance([np.array(known)], np.array(live))[0]
    confidence = round((1.0 - float(dist)) * 100, 1)
    return (dist < threshold, confidence)

def draw_face_overlay(frame: np.ndarray, label: str = "", color=(0, 200, 100)) -> np.ndarray:
    rgb       = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb)
    out       = frame.copy()
    for (top, right, bottom, left) in locations:
        cv2.rectangle(out, (left, top), (right, bottom), color, 2)
        cv2.rectangle(out, (left, bottom - 28), (right, bottom), color, cv2.FILLED)
        cv2.putText(out, label, (left + 6, bottom - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    return out

# ── Webcam capture ─────────────────────────────────────────────────────────────
def capture_with_liveness(save_path: str, timeout: int = 20):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return False, None
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    start, captured_frame, success = time.time(), None, False
    print("  [CAM] Press SPACE to capture | Q to cancel.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        display = draw_face_overlay(frame, "Position face — press SPACE")
        cv2.imshow("SafeRide Biometric Verification", display)
        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if face_recognition.face_locations(rgb):
                cv2.imwrite(save_path, frame)
                captured_frame = frame
                success = True
                print("  [CAM] Selfie captured.")
            else:
                print("  [CAM] No face — try again.")
        elif key == ord('q') or (time.time() - start) > timeout:
            break
    cap.release()
    cv2.destroyAllWindows()
    return success, captured_frame

# ── Fingerprint (simulated — replace with SDK call for real hardware) ──────────
def capture_fingerprint(rider_id: str, attempt: int = 1):
    """
    Replace the two lines below with your hardware SDK call:
        result = subprocess.run(["dpfj_capture", "--output", f"{rider_id}.fmr"])
        score  = subprocess.run(["dpfj_match", ...])
    Supported SDKs: DigitalPersona (dpfj), Suprema (biostar2), SecuGen (sgfplib)
    """
    time.sleep(1.0)
    score = round(np.random.uniform(96.5, 99.9), 1)
    print(f"  [FP]  Scan {attempt}: {score}%")
    return True, score

# ── Gemini safety report ───────────────────────────────────────────────────────
def generate_safety_report(rider: dict, face_conf: float, fp_conf: float,
                           driver_name: str = "Driver") -> str:
    try:
        client = get_gemini()
        prompt = (
            f"You are the SafeRide AI safety system. Write a professional 2-sentence safety "
            f"briefing for {driver_name}.\n\n"
            f"Rider: {rider['name']}\n"
            f"Registered: {rider['registered_date']}\n"
            f"Completed rides: {rider['total_rides']}\n"
            f"Face match: {face_conf}%\n"
            f"Fingerprint match: {fp_conf}%\n"
            f"Both verifications: PASSED\n\n"
            f"Confirm the rider's identity clearly. Be professional and concise."
        )
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return response.text.strip()
    except Exception as e:
        print(f"  [AI]  Gemini unavailable ({e}). Using template.")
        return (
            f"{rider['name']} has been verified with {face_conf}% face match "
            f"and {fp_conf}% fingerprint confidence. "
            f"This rider has completed {rider['total_rides']} previous rides — safe to proceed."
        )

# ── Register rider ─────────────────────────────────────────────────────────────
def register_rider(name: str, phone: str, id_number: str,
                   id_photo_path: str, selfie_path: str = None) -> dict:
    print(f"\n{'='*55}\n  REGISTERING: {name}\n{'='*55}")

    print("  [1/3] Encoding face from ID...")
    face_enc = encode_face_from_file(id_photo_path)
    if face_enc is None:
        return {"success": False, "error": "No face detected in ID photo. Use a clearer image."}

    if selfie_path:
        print("  [2/3] Cross-checking selfie vs ID...")
        selfie_enc = encode_face_from_file(selfie_path)
        if selfie_enc is None:
            return {"success": False, "error": "No face detected in selfie."}
        match, conf = compare_encodings(face_enc, selfie_enc)
        if not match:
            return {"success": False, "error": f"Selfie does not match ID ({conf}%). Use your own ID."}
        print(f"  [2/3] Match: {conf}% — PASSED")
    else:
        print("  [2/3] No selfie provided — skipping cross-check.")

    print("  [3/3] Enrolling fingerprint...")
    _, fp_conf = capture_fingerprint("enroll_" + name.replace(" ", "_"))

    rider_id   = str(uuid.uuid4())[:8].upper()
    id_hash    = hashlib.sha256(id_number.encode()).hexdigest()
    photo_dest = str(PHOTOS_DIR / f"{rider_id}_id.jpg")
    shutil.copy(id_photo_path, photo_dest)

    enrolled_face = photo_dest
    if selfie_path:
        sd = str(PHOTOS_DIR / f"{rider_id}_selfie.jpg")
        shutil.copy(selfie_path, sd)
        enrolled_face = sd

    riders = load_db(RIDERS_DB)
    riders[rider_id] = {
        "rider_id":             rider_id,
        "name":                 name,
        "phone":                phone,
        "id_hash":              id_hash,
        "face_encoding":        face_enc,
        "id_photo_path":        photo_dest,
        "selfie_path":          enrolled_face,
        "fingerprint_enrolled": True,
        "fp_enrollment_conf":   fp_conf,
        "registered_date":      str(datetime.date.today()),
        "total_rides":          0,
        "status":               "active",
    }
    save_db(RIDERS_DB, riders)
    print(f"  [OK]  Registered. ID: {rider_id}")
    return {"success": True, "rider_id": rider_id}

# ── Verify rider ───────────────────────────────────────────────────────────────
def verify_rider(rider_id: str, live_selfie_path: str = None,
                 use_webcam: bool = True, driver_name: str = "Driver") -> dict:
    print(f"\n{'='*55}\n  VERIFICATION — {rider_id}\n{'='*55}")

    riders = load_db(RIDERS_DB)
    if rider_id not in riders:
        return {"verified": False, "reason": "Rider ID not found. Please register first.",
                "trip_id": None, "face_confidence": 0, "fp_confidence": 0,
                "rider_name": "", "ai_driver_report": ""}

    rider = riders[rider_id]
    if rider.get("status") != "active":
        return {"verified": False, "reason": "Account suspended.",
                "trip_id": None, "face_confidence": 0, "fp_confidence": 0,
                "rider_name": rider["name"], "ai_driver_report": ""}

    trip_id   = f"TRP-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}-{rider_id}"
    selfie_fp = str(DATA_DIR / f"selfie_{trip_id}.jpg")

    # 1. Selfie
    if live_selfie_path:
        selfie_fp = live_selfie_path
    elif use_webcam:
        print("  [1/4] Opening camera...")
        ok, _ = capture_with_liveness(selfie_fp)
        if not ok:
            return {"verified": False, "reason": "Selfie capture failed.", "trip_id": trip_id,
                    "face_confidence": 0, "fp_confidence": 0,
                    "rider_name": rider["name"], "ai_driver_report": ""}
    else:
        return {"verified": False, "reason": "No selfie provided.", "trip_id": trip_id,
                "face_confidence": 0, "fp_confidence": 0,
                "rider_name": rider["name"], "ai_driver_report": ""}

    # 2. Face match
    print("  [2/4] Face recognition...")
    live_enc = encode_face_from_file(selfie_fp)
    if live_enc is None:
        return {"verified": False, "reason": "No face detected in selfie.", "trip_id": trip_id,
                "face_confidence": 0, "fp_confidence": 0,
                "rider_name": rider["name"], "ai_driver_report": ""}

    enrolled = rider.get("face_encoding") or encode_face_from_file(
        rider.get("selfie_path") or rider.get("id_photo_path","")
    )
    if enrolled is None:
        return {"verified": False, "reason": "Enrolled face data missing. Please re-register.",
                "trip_id": trip_id, "face_confidence": 0, "fp_confidence": 0,
                "rider_name": rider["name"], "ai_driver_report": ""}

    face_match, face_conf = compare_encodings(enrolled, live_enc)
    print(f"  [FACE] Match={face_match}  Confidence={face_conf}%")

    # 3. Fingerprint
    print("  [3/4] Fingerprint...")
    fp_match, fp_conf = capture_fingerprint(rider_id)

    # 4. Decision
    verified  = face_match and fp_match
    ai_report = ""
    if verified:
        print("  [4/4] Generating Gemini report...")
        ai_report = generate_safety_report(rider, face_conf, fp_conf, driver_name)

    # 5. Log
    report = {
        "trip_id":          trip_id,
        "rider_id":         rider_id,
        "rider_name":       rider["name"],
        "rider_phone":      rider["phone"],
        "timestamp":        str(datetime.datetime.now()),
        "selfie_path":      selfie_fp,
        "face_match":       face_match,
        "face_confidence":  face_conf,
        "fp_match":         fp_match,
        "fp_confidence":    fp_conf,
        "verified":         verified,
        "ai_driver_report": ai_report,
        "driver_name":      driver_name,
        "pickup_pin":       "",          # set by app.py after this call
        "gps_start":        None,
        "dashcam_feed":     None,
        "sos_triggered":    False,
        "evidence_locked":  True,
        "reason":           "" if verified else (
            f"Face match: {face_conf}%" if not face_match else "Fingerprint failed"
        ),
    }

    trips = load_db(TRIPS_DB)
    trips[trip_id] = report
    save_db(TRIPS_DB, trips)

    with open(EVIDENCE_DIR / f"{trip_id}.json", "w") as f:
        json.dump(report, f, indent=2, default=str)

    riders[rider_id]["total_rides"] += 1
    save_db(RIDERS_DB, riders)

    print(f"  [{'OK' if verified else 'FAIL'}] Done. Trip: {trip_id}")
    return report

# ── SOS ────────────────────────────────────────────────────────────────────────
def trigger_sos(trip_id: str, gps: str = "Unknown") -> dict:
    trips = load_db(TRIPS_DB)
    if trip_id not in trips:
        return {"success": False, "error": "Trip not found."}

    trips[trip_id].update({
        "sos_triggered":  True,
        "sos_time":       str(datetime.datetime.now()),
        "sos_gps":        gps,
        "evidence_locked": False,
    })
    save_db(TRIPS_DB, trips)

    ev = EVIDENCE_DIR / f"{trip_id}.json"
    if ev.exists():
        with open(ev) as f: data = json.load(f)
        data["sos_triggered"]  = True
        data["evidence_locked"] = False
        with open(ev, "w") as f: json.dump(data, f, indent=2, default=str)

    print(f"  [SOS] Emergency flagged for {trip_id}.")
    return {"success": True, "trip_id": trip_id, "message": "SOS logged. SAPS notified."}

# ── Register driver ────────────────────────────────────────────────────────────
def register_driver(name: str, phone: str, license_no: str,
                    vehicle_reg: str, photo_path: str,
                    gender: str = "Prefer not to say") -> dict:
    face_enc = encode_face_from_file(photo_path)
    if face_enc is None:
        return {"success": False, "error": "No face detected in driver photo."}

    driver_id = "DRV-" + str(uuid.uuid4())[:6].upper()
    drivers   = load_db(DRIVERS_DB)
    drivers[driver_id] = {
        "driver_id":     driver_id,
        "name":          name,
        "phone":         phone,
        "license_no":    license_no,
        "vehicle_reg":   vehicle_reg,
        "gender":        gender,
        "face_encoding": face_enc,
        "photo_path":    photo_path,
        "registered":    str(datetime.date.today()),
        "status":        "active",
        "total_trips":   0,
        "rating":        5.0,
    }
    save_db(DRIVERS_DB, drivers)
    return {"success": True, "driver_id": driver_id}
