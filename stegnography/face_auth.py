import cv2 
import os
import hashlib
import json
import face_recognition
from skimage.metrics import structural_similarity as ssim


def capture():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Verification")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture frame")
            break

        cv2.imshow("Verification", frame)
        key = cv2.waitKey(1)

        if key % 256 == 32:  # Space key
            temp = os.path.expanduser("~/Documents/stegnography/temp/temp.png")
            cv2.imwrite(temp, frame)
            break

    cam.release()
    cv2.destroyAllWindows()
    return temp

def get_face_encoding(img_path):
    image = face_recognition.load_image_file(img_path)
    encoding = face_recognition.face_encodings(image)[0]

    if len(encoding) == 0:
        print("No face found in image ")
        return None
    
    face_encoding = encoding[0]
    encoded_bytes = face_encoding.tobytes()

    return hashlib.sha256(encoded_bytes).hexdigest()

def compare(img_path1, img_path2):
    img1 = cv2.imread(img_path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img_path2, cv2.IMREAD_GRAYSCALE)

    if img1 is None or im2 is None:
        print("error reading images")
        return False

    img2 = cv2.resize(img2, (img1.shape[1], img.shape[0]))

    score, diff = ssim(img1, img2, full=True)
    print(f"similarity score {score}")

    return score > 0.7

def auth(username):

    path = os.path.expanduser("~/Documents/stegnography/hashes/hash.json")
    
    if not os.path.exists(path):
         print("Hash file not found!")
         return {}

    with open(path, "r") as f:
         stored = json.load(f)

    if username not in stored :
        print("USer not found")
        return False
    
    stored_hash = stored[username]
    new_file = capture()

    new_hash = get_face_encoding(new_file)

    if new_hash is None:
        print("failed to get hash")
        return False
    
    if new_hash != stored_hash:
        print("Unauthorized")
        return False 

    stored_img = os.path.expanduser(f"~/Documents/stegnography/faces/{username}.png")

    if not compare(stored_img, new_file):
        print("images do not match closly enough")
        return False

    print("Verification done")
    return True
    
username = input("Enter your username for verification")
auth(username)
# def get_image_hash(img_path):
#     with open(img_path, "rb") as f:
#         data = f.read()
#         return hashlib.sha256(data).hexdigest()

# def load_hashes():
#     path = os.path.expanduser("~/Documents/stegnography/hashes/hash.json")
    
#     if not os.path.exists(path):
#         print("Hash file not found!")
#         return {}

#     with open(path, "r") as f:
#         return json.load(f)

# def auth():
#     img_path = capture()
#     new_hash = get_image_hash(img_path)
#     stored_hashes = load_hashes()

#     for username, saved_hash in stored_hashes.items():
#         if new_hash == saved_hash:
#             print(f"Authenticated: {username}")
#             return True

#     print("Non-authenticated person")
#     return False

# if __name__ == '__main__':
# auth()

