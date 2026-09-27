from brain import Brain
from config import OPENROUTER_API_KEY
from modules.listener import listen
from modules.speaker import speak

# ==========================================
# AVAN STATUS
# ==========================================

try:
    from avan_status_client import set_status, set_command
except ImportError:

    def set_status(status):
        print(f"[STATUS] {status}")

    def set_command(command):
        print(f"[COMMAND] {command}")


# ==========================================
# API CHECK
# ==========================================

if OPENROUTER_API_KEY:
    print("✅ OpenRouter API Key Loaded Successfully")
else:
    print("❌ OpenRouter API Key Not Found!")


# ==========================================
# BRAIN
# ==========================================

brain = Brain()


# ==========================================
# START
# ==========================================

print("=" * 50)
print("🤖 AVAN AI")
print("=" * 50)
print("🎤 Voice mode activated")
print("Say 'Bye Avan' to close Avan.")
print("=" * 50)

set_status("IDLE")


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    try:

        # ----------------------------------
        # LISTEN
        # ----------------------------------

        user = listen()

        if not user:
            set_status("IDLE")
            continue

        command = user.lower().strip()

        set_command(user)

        # ----------------------------------
        # EXIT
        # ----------------------------------

        exit_words = [
            "exit",
            "bye",
            "bye avan",
            "goodbye",
            "goodbye avan",
            "good bye",
            "good bye avan",
            "close avan",
            "stop avan",
            "stop avan ai",
            "quit"
        ]

        if command in exit_words:

            print("\nAvanAI : Goodbye Sir.")

            set_status("SPEAKING")

            speak("Goodbye Sir.")

            set_status("IDLE")

            break

        # ----------------------------------
        # THINK
        # ----------------------------------

        set_status("THINKING")

        print("\n🧠 Avan is thinking...")

        answer = brain.think(user)

        print(
            f"\n🤖 AvanAI : {answer}"
        )

        # ----------------------------------
        # SPEAK
        # ----------------------------------

        set_status("SPEAKING")

        speak(answer)

        # ----------------------------------
        # READY
        # ----------------------------------

        set_status("IDLE")

    except KeyboardInterrupt:

        print("\n\n🛑 Avan stopped.")

        set_status("IDLE")

        break

    except Exception as e:

        print(
            f"\n❌ Avan Error: {e}"
        )

        set_status("ERROR")

        try:
            speak(
                "Sorry Sir, something went wrong."
            )
        except Exception:
            pass

        set_status("IDLE")