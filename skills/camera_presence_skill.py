import cv2

camera = None
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def run(command):

    global camera

    text = command.lower().strip()

    if (
        "camera monitor" in text
        or "presence check" in text
        or "monitor camera" in text
    ):

        if camera is not None:
            return "Camera monitoring is already running Boss."

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            camera.release()
            camera = None
            return "Sorry Boss, I couldn't access the camera."

        detected_once = False

        while True:

            success, frame = camera.read()

            if not success:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_detector.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(80, 80)
            )

            if len(faces) > 0 and not detected_once:

                print("👤 Person detected in front of camera.")
                detected_once = True

            if len(faces) == 0:
                detected_once = False

            for (x, y, w, h) in faces:

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

            cv2.imshow("Avan Presence Monitor", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        camera.release()
        camera = None
        cv2.destroyAllWindows()

        return "Camera monitoring stopped Boss."

    return None