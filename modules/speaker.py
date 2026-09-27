import asyncio
import edge_tts
import os
from playsound3 import playsound

# ==========================================
# AVAN STATUS CONNECTION
# ==========================================

try:
    from avan_status_client import set_status
except ImportError:

    def set_status(status):
        print(f"[STATUS] {status}")


# ==========================================
# VOICE SETTINGS
# ==========================================

VOICE = "en-US-JennyNeural"
AUDIO_FILE = "voice.mp3"


# ==========================================
# GENERATE VOICE
# ==========================================

async def _generate_voice(text):

    communicate = edge_tts.Communicate(
        text,
        VOICE
    )

    await communicate.save(
        AUDIO_FILE
    )


# ==========================================
# SPEAK
# ==========================================

def speak(text):

    try:

        # ----------------------------------
        # HUD → SPEAKING
        # ----------------------------------

        set_status("SPEAKING")

        print("🔊 Avan is speaking...")

        # ----------------------------------
        # Generate voice
        # ----------------------------------

        asyncio.run(
            _generate_voice(text)
        )

        print(
            "✅ Voice Generated Successfully"
        )

        # ----------------------------------
        # Play voice
        # ----------------------------------

        audio_path = os.path.abspath(
            AUDIO_FILE
        )

        playsound(
            audio_path
        )

        print(
            "🔊 Avan finished speaking"
        )

        # ----------------------------------
        # HUD → IDLE
        # ----------------------------------

        set_status("IDLE")

    except Exception as e:

        print(
            f"❌ Voice Error: {e}"
        )

        # ----------------------------------
        # HUD → ERROR
        # ----------------------------------

        set_status("ERROR")