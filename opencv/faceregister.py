import cv2
import hashlib
import json
import os
import face_recognition

face_store_path = os.path.expanduser("~/Documents/stegnography/faces/")
hash_store_path = os.path.expanduser("~/Documents/stegnography/hashes/")
os.makedirs(face_store_path, exist_ok=True)
os.makedirs(hash_store_path, exist_ok=True)

def capture(username):
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Capture for registration")
    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                print(" Failed to capture frame.")
                break

            cv2.imshow("Capture for registration", frame)
            k = cv2.waitKey(1)

            if k % 256 == 32:  # SPACE key
                # path = os.path.join(face_store_path, f"{username}.png") these are needed if we are not using face recognition module
                # cv2.imwrite(path, frame)
                # print(" Face image registered:", path)
                # break
                face_location = face_recognition.face_locations(frame)
                if len(face_location) == 0:
                    print("No face found try again ")
                    continue
                top, right, bottom, left = face_location[0]

                face_image = frame[top:bottom, left:right]

                face_encoding = face_recognition.face_encodings(frame, known_face_locations=face_location)[0]
                face_image_path = os.path.join(face_store_path, f"{username}.png")
                cv2.imwrite(face_image_path, face_image)

                encoding_bytes = face_encoding.tobytes()
    except KeyboardInterrupt:
        print(KeyboardInterrupt)        

    cam.release()
    cv2.destroyAllWindows()
    return path
    return encoding_bytes

def hash_img(img_path, bytes):
    try:
        # with open(img_path, "rb") as _file:
        #     _data = _file.read()
            return hashlib.sha256(bytes).hexdigest()
    except Exception as e:
        print(" Error while hashing image:", e)
        return None

def save(username, hash_token):
    hash_file = os.path.join(hash_store_path, "hash.json")

    # Load existing hashes or create new dict
    if os.path.exists(hash_file):
        try:
            with open(hash_file, "r") as f:
                face_hashes = json.load(f)
        except json.JSONDecodeError:
            face_hashes = {}
    else:
        face_hashes = {}

    # Save new hash
    face_hashes[username] = hash_token
    with open(hash_file, "w") as f:
        json.dump(face_hashes, f, indent=4)
    print(" Hash saved for", username)

if __name__ == '__main__':
    username = input("\n Enter the username: ").strip()
    if username:
        img_path = capture(username)
        hash_token = hash_img(img_path)
        if hash_token:
            save(username, hash_token)
    else:
        print(" Username cannot be empty.")
