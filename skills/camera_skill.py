import cv2
import os
import time


camera = None


def run(command):

    global camera

    text = command.lower()


    # ---------------- OPEN CAMERA ----------------

    if (
        "open camera" in text
        or "camera kholo" in text
        or "camera open" in text
    ):

        camera = cv2.VideoCapture(0)

        if camera.isOpened():

            while True:

                ret, frame = camera.read()

                if not ret:
                    break

                cv2.imshow(
                    "Avan Camera",
                    frame
                )

                if cv2.waitKey(1) == ord("q"):
                    break


            camera.release()
            cv2.destroyAllWindows()

            return "Camera closed Boss."

        else:

            return "Sorry Boss, camera not found."


    # ---------------- TAKE PHOTO ----------------

    if (
        "take photo" in text
        or "photo lo" in text
        or "meri photo lo" in text
    ):

        cam = cv2.VideoCapture(0)

        ret, frame = cam.read()

        if ret:

            desktop = os.path.join(
                os.path.expanduser("~"),
                "OneDrive",
                "Desktop"
            )

            filename = (
                "Avan_photo_"
                + str(int(time.time()))
                + ".jpg"
            )

            path = os.path.join(
                desktop,
                filename
            )

            cv2.imwrite(
                path,
                frame
            )

            cam.release()

            return "Photo captured Boss."

        return "Camera error Boss."


    return None