import segno
import json
import os

class QR:
    def __init__(self, name, dob, native):
        self.name = name
        self.dob = dob
        self.native = native 

    def to_qr(self):
        return {
            "name": self.name,
            "DOB": self.dob,
            "native": self.native
        }

    def qr(self, path=os.path.expanduser("~/Documents/qr.json.png")):
        json_data = json.dumps(self.to_qr(), indent=4)
        qr_code = segno.make(json_data)
        qr_code.save(path, scale=10)
        print(f"✅ QR code saved to: {path}")

# Take user input
def main():
    name = input("Enter your name: ").strip()
    dob = input("Enter your date of birth (YYYY-MM-DD): ").strip()
    native = input("Enter your native place: ").strip()

    qr_object = QR(name, dob, native)
    qr_object.qr()

if __name__ == "__main__":
    main()
