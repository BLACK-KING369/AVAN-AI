from memory import remember, recall


def run(command):

    text = command.lower().strip()

    # Save Name
    if text.startswith("my name is"):

        name = command[10:].strip()

        remember("name", name)

        return f"Okay Boss, I'll remember your name is {name}."


    # Favourite Color
    if text.startswith("my favourite color is"):

        color = command[21:].strip()

        remember("favorite_color", color)

        return f"Okay Boss, I'll remember your favourite color is {color}."


    # City
    if text.startswith("i live in"):

        city = command[9:].strip()

        remember("city", city)

        return f"Okay Boss, I'll remember that you live in {city}."


    # College
    if text.startswith("my college is"):

        college = command[13:].strip()

        remember("college", college)

        return f"Okay Boss, I'll remember your college is {college}."


    # Recall Name
    if "what is my name" in text:

        name = recall("name")

        if name:
            return f"Your name is {name}, Boss."

        return "I don't know your name yet, Boss."


    # Recall Favourite Color
    if "what is my favourite color" in text:

        color = recall("favorite_color")

        if color:
            return f"Your favourite color is {color}, Boss."

        return "You haven't told me your favourite color yet, Boss."


    # Recall City
    if "where do i live" in text:

        city = recall("city")

        if city:
            return f"You live in {city}, Boss."

        return "You haven't told me where you live yet, Boss."


    # Recall College
    if "what is my college" in text:

        college = recall("college")

        if college:
            return f"Your college is {college}, Boss."

        return "You haven't told me your college yet, Boss."

    return None