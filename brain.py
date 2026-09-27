from ai.openrouter import ask_openrouter
from commands import execute_command
from datetime import datetime
import time

from intent import detect_intent
from ai.personality import PERSONALITY

from skills.memory_skill import run as memory_skill
from skills.browser_skill import run as browser_skill
from skills.app_skill import run as app_skill
from skills.system_skill import run as system_skill
from skills.camera_skill import run as camera_skill
from skills.control_skill import run as control_skill
from skills.vision_skill import run as vision_skill
from skills.mouse_skill import run as mouse_skill
from skills.keyboard_skill import run as keyboard_skill
from skills.camera_presence_skill import run as camera_presence_skill
from memory import remember, recall

class Brain:

    def think(self, user_input):

        # ---------------- BASIC CLEANUP ----------------

        user_input = user_input.strip()

        if not user_input:
            return "I'm listening, Sir."

        user = user_input.lower().strip()

        # ---------------- INTENT DETECTION ----------------

        intent = detect_intent(user_input)

        print(f"🧭 INTENT: {intent}")

        # =================================================
        # PERSONAL MEMORY
        # =================================================

        if intent == "memory":

            import re

            # ---------------- NAME ----------------

            name_patterns = [
                r"my name is\s+(.+)",
                r"mera naam\s+(.+)",
                r"my name\s+(.+)",
            ]

            for pattern in name_patterns:

                match = re.search(pattern, user, re.IGNORECASE)

                if match:

                    name = match.group(1).strip()

                    # Remove common ending words
                    name = re.sub(
                        r"\s+(hai|h|he|is)$",
                        "",
                        name,
                        flags=re.IGNORECASE
                    ).strip()

                    if name:

                        remember("name", name)

                        return f"Okay Sir, I will remember that your name is {name}."

            # ---------------- REMEMBER COMMAND ----------------

            remember_patterns = [
                r"remember that (.+?) is (.+)",
                r"remember (.+?) is (.+)",
                r"yaad rakho (.+?) (?:hai|is) (.+)",
                r"yaad rakhna (.+?) (?:hai|is) (.+)",
            ]

            for pattern in remember_patterns:

                match = re.search(
                    pattern,
                    user,
                    re.IGNORECASE
                )

                if match:

                    key = match.group(1).strip()
                    value = match.group(2).strip()

                    if remember(key, value):

                        return f"Okay Sir, I will remember that {key} is {value}."

            # ---------------- NAME QUESTION ----------------

            name_question_patterns = [
                "what is my name",
                "what's my name",
                "mera naam kya hai",
                "mera name kya hai",
                "do you know my name",
                "kya tumhe mera naam pata hai",
            ]

            if any(
                phrase in user
                for phrase in name_question_patterns
            ):

                name = recall("name")

                if name:

                    return f"Your name is {name}, Sir."

                return "Sir, I don't have your name saved yet."

        # =================================================
        # SYSTEM
        # =================================================

        if intent == "system":

            result = system_skill(user_input)

            if result:
                return result

        # =================================================
        # APP
        # =================================================

        elif intent == "app":

            result = app_skill(user_input)

            if result:
                return result

            # fallback to command system
            result = execute_command(user_input)

            if result:
                return result

        # =================================================
        # BROWSER
        # =================================================

        elif intent == "browser":

            result = browser_skill(user_input)

            if result:
                return result

            result = execute_command(user_input)

            if result:
                return result

        # =================================================
        # MEMORY
        # =================================================

        elif intent == "memory":

            result = memory_skill(user_input)

            if result:
                return result

        # =================================================
        # CAMERA
        # =================================================

        elif intent == "camera":

            result = camera_skill(user_input)

            if result:
                return result

        # =================================================
        # VISION
        # =================================================

        elif intent == "vision":

            result = vision_skill(user_input)

            if result:
                return result

        # =================================================
        # MOUSE
        # =================================================

        elif intent == "mouse":

            result = mouse_skill(user_input)

            if result:
                return result

        # =================================================
        # KEYBOARD
        # =================================================

        elif intent == "keyboard":

            result = keyboard_skill(user_input)

            if result:
                return result

        # =================================================
        # CONTROL
        # =================================================

        elif intent == "control":

            result = control_skill(user_input)

            if result:
                return result

        # =================================================
        # COMMAND FALLBACK
        # =================================================

        # Commands which aren't specifically detected
        # by intent.py can still reach the command system.

        if intent in ["conversation", "information"]:

            result = execute_command(user_input)

            if result:
                return result

        # =================================================
        # GREETING
        # =================================================

        current_hour = datetime.now().hour

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
            return "Hello Sir! How can I help you?"

        # ---------------- GOOD MORNING ----------------

        if user == "good morning":

            if current_hour < 12:
                return "Good morning, Sir. How can I help you?"

            return "Sir, it's not morning right now. How can I help you?"

        # ---------------- GOOD AFTERNOON ----------------

        if user == "good afternoon":

            if 12 <= current_hour < 17:
                return "Good afternoon, Sir. How can I help you?"

            return "Sir, it's not afternoon right now. How can I help you?"

        # ---------------- GOOD EVENING ----------------

        if user == "good evening":

            if 17 <= current_hour < 24:
                return "Good evening, Sir. How can I help you?"

            return "Sir, it's not evening right now. How can I help you?"

        # ---------------- GOOD NIGHT ----------------

        if user == "good night":

            if current_hour >= 21 or current_hour < 5:
                return "Good night, Sir. Take care."

            return "Sir, it's not night yet. How can I help you?"

        # =================================================
        # GENERAL AI
        # =================================================

        prompt = f"""
You are Avan, a highly intelligent personal AI assistant.

The user should be addressed as "Sir".

Your personality:
{PERSONALITY}

IMPORTANT LANGUAGE RULES:

1. Understand Hindi, English and Hinglish.
2. If Sir speaks Hindi, reply naturally in Hindi.
3. If Sir speaks English, reply naturally in English.
4. If Sir speaks Hinglish, reply naturally in Hinglish.
5. Do not unnecessarily translate the user's language.
6. Match the user's language naturally.
7. Understand Hindi written using English letters.
8. Understand spelling mistakes and informal speech.

CONVERSATION RULES:

- Be intelligent, calm and helpful.
- Speak naturally like a futuristic personal AI assistant.
- Address the user as Sir when appropriate.
- Never call the user Boss.
- Do not say "As an AI language model".
- Do not give unnecessary long explanations unless asked.
- If the user asks a factual question, answer directly.
- If the user asks a technical question, explain clearly.
- If you don't know something, say so honestly.
- Do not pretend that you performed an action if you did not.

IMPORTANT:

Commands such as opening applications, controlling the computer,
mouse, keyboard, camera and system are handled by Avan's skills.
Do not pretend that you executed such commands yourself.

Examples:

User: "python kya hota hai?"
Answer naturally in Hindi/Hinglish.

User: "what is python?"
Answer in English.

User: "bhai python me calculator kaise banau?"
Answer naturally in Hinglish.

User: "भारत की राजधानी क्या है?"
Answer in Hindi.

User message:
{user_input}
"""

        # =================================================
        # ASK AI
        # =================================================

        start = time.time()

        print("🧠 Asking AI...")

        try:

            answer = ask_openrouter(prompt)

            elapsed = time.time() - start

            print(f"⏱️ AI response time: {elapsed:.2f} seconds")

            return answer

        except Exception as e:

            print(f"❌ AI Error: {e}")

            return "Sorry Sir, I couldn't process that request right now."