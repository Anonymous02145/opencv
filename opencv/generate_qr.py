import segno
import pillow
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
        json_data = json.dumps(self.to_qr())
        gen = segno.make(json_data)
        gen.save(path, scale=10)
        
