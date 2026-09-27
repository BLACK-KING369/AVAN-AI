from ai.openrouter import ask_openrouter
from commands import execute_command
from datetime import datetime

from memory import remember, recall
from intent import detect_intent
from ai.personality import PERSONALITY

from skills.memory_skill import run as memory_skill
from skills.browser_skill import run as browser_skill
from skills.app_skill import run as app_skill
from skills.system_skill import run as system_skill
import time
from skills.camera_skill import run as camera_skill

from skills.control_skill import run as control_skill
from skills.vision_skill import run as vision_skill
from skills.mouse_skill import run as mouse_skill
from skills.keyboard_skill import run as keyboard_skill

from skills.camera_presence_skill import run as camera_presence_skill

class Brain:

    def think(self, user_input):

        # ---------------- BASIC CLEANUP ----------------

        user_input = user_input.strip()

        if not user_input:
            return "I'm listening, Boss."


        user = user_input.lower().strip()

        intent = detect_intent(user_input)

        print(f"🧭 INTENT: {intent}")

        
        # ---------------- SYSTEM CONTROL ----------------

        result = system_skill(user_input)

        if result:
         return result

# ---------------- CAMERA PRESENCE ----------------

        result = camera_presence_skill(user_input)

        if result:
          return result
        # ---------------- MOUSE CONTROL ----------------

        result = mouse_skill(user_input)

        if result:
         return result

        # ---------------- KEYBOARD CONTROL ----------------

        result = keyboard_skill(user_input)

        if result:
         return result
 
       
        # ---------------- CONTROL SYSTEM ----------------

        result = control_skill(user_input)

        if result:
         return result

 # ---------------- VISION CONTROL ----------------

        result = vision_skill(user_input)

        if result:
          return result

        # ---------------- CAMERA CONTROL ----------------

        result = camera_skill(user_input)

        if result:
         return result

        # ---------------- APP CONTROL ----------------

        result = app_skill(user_input)

        if result:
                      return result



        # ---------------- TIME ----------------

        current_hour = datetime.now().hour


        # ---------------- GREETING SYSTEM ----------------

        wake_words = [
            "hello",
            "hi",
            "hey",
            "avan",
            "hello avan",
            "hi avan",
            "hey avan",
            "wake up avan"
        ]

        if user in wake_words:
            return "Hello Boss! How can I help you?"


        # Good Morning

        if user == "good morning":

            if current_hour < 12:
                return "Good morning, Boss. How can I help you?"

            return "Boss, it's not morning right now. How can I help you?"


        # Good Afternoon

        if user == "good afternoon":

            if 12 <= current_hour < 17:
                return "Good afternoon, Boss. How can I help you?"

            return "Boss, it's not afternoon right now. How can I help you?"


        # Good Evening

        if user == "good evening":

            if 17 <= current_hour < 24:
                return "Good evening, Boss. How can I help you?"


            return "Boss, it's not evening right now. How can I help you?"


        # Good Night

        if user == "good night":

            if current_hour >= 21 or current_hour < 5:
                return "Good night, Boss. Take care."

            return "Boss, it's not night yet. How can I help you?"


        # ---------------- MEMORY SKILL ----------------

        result = memory_skill(user_input)

        if result:
            return result


        # ---------------- COMMAND SYSTEM ----------------

        # Only actual commands should reach this system.
        result = execute_command(user_input)

        if result:
            return result


        # ---------------- BROWSER SKILL ----------------

        result = browser_skill(user_input)

        if result:
            return result


        # ---------------- AI BRAIN ----------------

        prompt = f"""
You are Avan, a highly intelligent personal AI assistant.

Your user is Boss.

Your personality:
{PERSONALITY}

IMPORTANT LANGUAGE RULES:

1. Automatically understand Hindi, English and Hinglish.
2. If Boss speaks Hindi, reply naturally in Hindi.
3. If Boss speaks English, reply in English.
4. If Boss speaks Hinglish, reply naturally in Hinglish.
5. Do NOT translate the user's language unnecessarily.
6. Match Boss's language style naturally.

CONVERSATION RULES:

- Be intelligent, calm and helpful.
- Speak naturally like a futuristic personal AI assistant.
- Address the user as "Boss" when appropriate.
- Don't say "As an AI language model".
- Don't give unnecessary long explanations unless Boss asks for detail.
- If Boss asks a factual question, answer it directly.
- If Boss asks a technical question, explain clearly.
- If Boss asks something you don't know, honestly say so.
- Understand spelling mistakes and informal speech.
- Understand Hindi written using English letters.

Examples:

Boss: "python kya hota hai?"
Answer in Hindi/Hinglish.

Boss: "what is python?"
Answer in English.

Boss: "bhai python me calculator kaise banau?"
Answer naturally in Hinglish.

Boss: "भारत की राजधानी क्या है?"
Answer in Hindi.

Boss: "open youtube"
This should normally be handled by Avan's command system, not by you.

Now answer Boss's message naturally.

Boss says:
{user_input}
"""

                # ---------------- AI BRAIN ----------------

        start = time.time()

        print("🧠 Asking AI...")

        answer = ask_openrouter(prompt)

        elapsed = time.time() - start

        print(f"⏱️ AI response time: {elapsed:.2f} seconds")

        return answer