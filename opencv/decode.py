import cv2

def read():

    cam = cv2.videoCapture(0)
    
    detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cam.read()

        if not ret:
            print("failed to read")
            break
        
        data, ddbox, _ = detector.detectAndDecode(frame)
        
        if data:
            cam.release()
            cam.destroyAllWindows()
            return data

        # if ddbox is not None:
        #     for i in range(len(ddbox)):
        #         pt1 = tuple(ddbox[i][0])
        #         pt2 = tuple(ddbox[(i + 1) % len(ddbox)][0])
        # cv2.putText(frame, data, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (225, 0, 0), 2)

        cv2.imshow("Scanning.....", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
