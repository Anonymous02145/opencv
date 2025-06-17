import os
import cv2
import json
import hashlib
from datetime import datetime
import face_recognition
from pyzbar.pyzbar import decode
from skimage.metrics import structural_similarity as ssim

# Paths
face_store_path = os.path.expanduser("~/Documents/stegnography/faces/")
hash_store_path = os.path.expanduser("~/Documents/stegnography/hashes/")
temp_path = os.path.expanduser("~/Documents/stegnography/temp/")
log_file_path = os.path.expanduser("~/Documents/logs/logs.log")

# Ensure folders exist
os.makedirs(temp_path, exist_ok=True)
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

def capture_face_only():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Face Verification")

    face_img_path = os.path.join(temp_path, "temp_face.png")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("❌ Failed to capture frame.")
            break

        face_locations = face_recognition.face_locations(frame)
        for (top, right, bottom, left) in face_locations:
            for point in [(left, top), (right, top), (left, bottom), (right, bottom)]:
                cv2.circle(frame, point, 4, (0, 255, 0), -1)

        cv2.imshow("Face Verification", frame)
        if cv2.waitKey(1) % 256 == 32:  # SPACE key
            if not face_locations:
                print("⚠️ No face detected. Try again.")
                continue
            top, right, bottom, left = face_locations[0]
            face_image = frame[top:bottom, left:right]
            cv2.imwrite(face_img_path, face_image)
            break

    cam.release()
    cv2.destroyAllWindows()
    return face_img_path

def get_face_encoding(img_path):
    try:
        image = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            print("❌ No face encoding found.")
            return None
        return hashlib.sha256(encodings[0].tobytes()).hexdigest()
    except Exception as e:
        print("❌ Encoding error:", e)
        return None

def compare(img_path1, img_path2):
    img1 = cv2.imread(img_path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img_path2, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        print("❌ Error reading images.")
        return False

    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    score, _ = ssim(img1, img2, full=True)
    print(f"🔍 Face similarity score: {score:.2f}")
    return score > 0.7

def scan_qr():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Scan QR Code")

    print("📷 Show your QR code to the camera...")
    while True:
        ret, frame = cam.read()
        if not ret:
            print("❌ Frame read error.")
            break

        barcodes = decode(frame)
        for barcode in barcodes:
            try:
                qr_data = json.loads(barcode.data.decode("utf-8"))
                cam.release()
                cv2.destroyAllWindows()
                return qr_data
            except Exception as e:
                print("❌ QR decode error:", e)

        cv2.imshow("Scan QR Code", frame)
        if cv2.waitKey(1) == 27:  # ESC key
            break

    cam.release()
    cv2.destroyAllWindows()
    return None

def log_success(username, qr_data):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "timestamp": now,
        "username": username,
        "qr_data": qr_data
    }

    try:
        with open(log_file_path, "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")
        print(f"✅ Logged successfully at {now}")
    except Exception as e:
        print("❌ Logging error:", e)

def auth(username):
    hash_file = os.path.join(hash_store_path, "hash.json")
    face_file = os.path.join(face_store_path, f"{username}.png")

    if not os.path.exists(hash_file) or not os.path.exists(face_file):
        print("❌ Required files not found.")
        return False

    with open(hash_file, "r") as f:
        stored_hashes = json.load(f)

    if username not in stored_hashes:
        print("❌ Username not found in database.")
        return False

    print("🔐 Capturing face for verification...")
    live_img = capture_face_only()
    live_hash = get_face_encoding(live_img)
    if not live_hash:
        print("❌ Failed to generate face hash.")
        return False

    if live_hash != stored_hashes[username]:
        print("❌ Face hash mismatch.")
        return False

    if not compare(face_file, live_img):
        print("❌ Face similarity too low.")
        return False

    print("✅ Face verification passed!")
    print("🔍 Now scanning QR code...")

    qr_data = scan_qr()
    if not qr_data:
        print("❌ QR scan failed.")
        return False

    print("✅ QR scanned successfully.")
    log_success(username, qr_data)
    return True

# Entry Point
if __name__ == "__main__":
    username = input("Enter your username for verification: ").strip()
    if username:
        auth(username)
    else:
        print("⚠️ Username cannot be empty.")
