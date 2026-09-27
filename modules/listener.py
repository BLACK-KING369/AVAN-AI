try:
    import speech_recognition as sr
except ImportError:
    sr = None

import wave
import tempfile
import os

try:
    import sounddevice as sd
except ImportError:
    sd = None

try:
    import numpy as np
except ImportError:
    np = None

# ==========================================
# AVAN STATUS CONNECTION
# ==========================================

try:
    from avan_status_client import set_status, set_command
except ImportError:

    def set_status(status):
        print(f"[STATUS] {status}")

    def set_command(command):
        print(f"[COMMAND] {command}")


# ==========================================
# SPEECH CONFIG
# ==========================================

recognizer = sr.Recognizer() if sr is not None else None

SAMPLE_RATE = 16000
CHANNELS = 1
RECORD_SECONDS = 8


# ==========================================
# MICROPHONE
# ==========================================

def find_microphone():

    try:

        if sd is None:
            print("❌ sounddevice is not installed.")
            return None

        devices = sd.query_devices()

        for i, device in enumerate(devices):

            name = device["name"].lower()

            if (
                device["max_input_channels"] > 0
                and "stereo mix" not in name
                and "virtual" not in name
            ):

                print(
                    f"🎤 Selected microphone: {device['name']}"
                )

                return i

        return None

    except Exception as e:

        print(
            f"❌ Microphone detection error: {e}"
        )

        return None


# ==========================================
# LISTEN
# ==========================================

def listen():

    microphone_index = find_microphone()

    if microphone_index is None:

        set_status("ERROR")

        print(
            "❌ No suitable microphone found Sir."
        )

        return None

    if sr is None or recognizer is None:

        set_status("ERROR")

        print(
            "❌ SpeechRecognition is not installed."
        )

        return None

    temp_file = None

    try:

        # ----------------------------------
        # LISTENING
        # ----------------------------------

        set_status("LISTENING")

        print(
            "🎤 Listening... Speak now Sir."
        )

        recording = sd.rec(
            int(
                RECORD_SECONDS
                * SAMPLE_RATE
            ),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
            device=microphone_index
        )

        sd.wait()

        # ----------------------------------
        # THINKING / PROCESSING
        # ----------------------------------

        set_status("THINKING")

        print(
            "🧠 Processing..."
        )

        # ----------------------------------
        # TEMP WAV
        # ----------------------------------

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp:

            temp_file = temp.name

        # ----------------------------------
        # SAVE WAV
        # ----------------------------------

        with wave.open(
            temp_file,
            "wb"
        ) as wav_file:

            wav_file.setnchannels(
                CHANNELS
            )

            wav_file.setsampwidth(
                2
            )

            wav_file.setframerate(
                SAMPLE_RATE
            )

            wav_file.writeframes(
                recording.tobytes()
            )

        # ----------------------------------
        # READ AUDIO
        # ----------------------------------

        with sr.AudioFile(
            temp_file
        ) as source:

            audio = recognizer.record(
                source
            )

        # ----------------------------------
        # GOOGLE SPEECH RECOGNITION
        # ----------------------------------

        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print(
            f"🗣 You : {text}"
        )

        # ----------------------------------
        # SEND COMMAND TO AVAN STATUS
        # ----------------------------------

        set_command(text)

        # Brain will take over now
        set_status("THINKING")

        return text

    # ======================================
    # SPEECH NOT UNDERSTOOD
    # ======================================

    except sr.UnknownValueError:

        set_status("IDLE")

        print(
            "⚠️ I couldn't understand you Sir."
        )

        return None

    # ======================================
    # GOOGLE SERVICE ERROR
    # ======================================

    except sr.RequestError as e:

        set_status("ERROR")

        print(
            f"❌ Speech recognition service error: {e}"
        )

        return None

    # ======================================
    # OTHER ERROR
    # ======================================

    except Exception as e:

        set_status("ERROR")

        print(
            f"❌ Listener error: {e}"
        )

        return None

    # ======================================
    # CLEAN TEMP FILE
    # ======================================

    finally:

        if (
            temp_file
            and os.path.exists(temp_file)
        ):

            try:

                os.remove(
                    temp_file
                )

            except Exception:

                pass