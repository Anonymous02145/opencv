import cv2
import os
import hashlib
import json
import face_recognition
from skimage.metrics import structural_similarity as ssim

face_store_path = os.path.expanduser("~/Documents/stegnography/faces/")
hash_store_path = os.path.expanduser("~/Documents/stegnography/hashes/")
temp_path = os.path.expanduser("~/Documents/stegnography/temp/")
os.makedirs(temp_path, exist_ok=True)

def capture_face_only():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Verification")

    face_img_path = os.path.join(temp_path, "temp_face.png")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture frame")
            break

        face_locations = face_recognition.face_locations(frame)

        for (top, right, bottom, left) in face_locations:
            # Draw green dots on corners
            dot_color = (0, 255, 0)
            points = [(left, top), (right, top), (left, bottom), (right, bottom)]
            for point in points:
                cv2.circle(frame, point, 4, dot_color, -1)

        cv2.imshow("Verification", frame)
        key = cv2.waitKey(1)

        if key % 256 == 32:  # SPACE key
            if len(face_locations) == 0:
                print("No face detected, try again.")
                continue

            # Take first face only
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
            print("No face encoding found.")
            return None
        face_encoding = encodings[0]
        return hashlib.sha256(face_encoding.tobytes()).hexdigest()
    except Exception as e:
        print("Encoding error:", e)
        return None

def compare(img_path1, img_path2):
    img1 = cv2.imread(img_path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img_path2, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        print("Error reading images")
        return False

    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    score, _ = ssim(img1, img2, full=True)
    print(f"Similarity score: {score:.2f}")

    return score > 0.7

def auth(username):
    hash_file = os.path.join(hash_store_path, "hash.json")
    face_file = os.path.join(face_store_path, f"{username}.png")

    if not os.path.exists(hash_file):
        print("Hash file not found!")
        return False
    if not os.path.exists(face_file):
        print("Stored face image not found!")
        return False

    with open(hash_file, "r") as f:
        stored_hashes = json.load(f)

    if username not in stored_hashes:
        print("Username not found!")
        return False

    # Capture live face
    new_img = capture_face_only()
    new_hash = get_face_encoding(new_img)

    if new_hash is None:
        print("Failed to generate hash")
        return False

    if new_hash != stored_hashes[username]:
        print("Hash mismatch. Unauthorized.")
        return False

    if not compare(face_file, new_img):
        print("Images don't match closely enough.")
        return False

    print("✅ Verification successful!")
    return True

# Main entry
if __name__ == "__main__":
    username = input("Enter your username for verification: ").strip()
    if username:
        auth(username)
    else:
        print("Username cannot be empty.")
