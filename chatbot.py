import re
from datetime import datetime


def normalize(text: str) -> str:
    """
    Step 1 of Decision Flow: Normalization.
    Converts input to lowercase, removes punctuation, and strips extra whitespace
    so that '  HELLO!!! ' and 'hello' are treated identically.
    """
    text = text.lower()
    # Remove any character that is NOT a word character (\w) or whitespace (\s)
    text = re.sub(r"[^\w\s]", "", text)
    # Collapse multiple spaces into a single space and strip leading/trailing spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Step 2 of Decision Flow: Ordered Keyword Rules.
# Stored as a list of (keywords, response) tuples so matching order is guaranteed.
# Note: Since normalize() strips apostrophes, "what's" becomes "whats".
RULES = [
    (
        ["hi", "hello", "hey"],
        "Hello! How can I help you today?",
    ),
    (
        ["how are you", "how is it going", "how are things"],
        "I'm doing great, thank you for asking! Ready to chat with you.",
    ),
    (
        ["whats your name", "what is your name", "who are you"],
        "I am CodeOrbit Bot, a rule-based chatbot built with Python!",
    ),
    (
        ["help", "what can you do"],
        "I can greet you, remember your name (try 'My name is ...'), tell the current time/date, and answer basic questions!",
    ),
    (
        ["time", "date", "what time is it", "today"],
        lambda: f"The current date and time is {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}.",
    ),
    (
        ["thanks", "thank you", "thx"],
        "You're very welcome! Happy to help.",
    ),
    (
        ["who made you", "who created you", "creator"],
        "I was built by Daniel as part of the CodeOrbit AI Internship!",
    ),
    (
        ["bye", "goodbye", "exit", "see you"],
        "Goodbye! Have a productive day ahead!",
    ),
]

FALLBACK_RESPONSE = (
    "Sorry, I didn't understand. Try asking about 'what can you do', "
    "the current 'time', or introducing yourself with 'My name is [Your Name]'."
)


def get_response(user_input: str) -> str:
    """
    Determines the bot's reply using a strict 4-stage pipeline:
    1. Normalization: Clean the raw user input.
    2. Regex Rule First: Check specific pattern rules (e.g., capturing the user's name)
       before general keyword rules so they aren't shadowed.
    3. Keyword Rules in Order: Loop through RULES top-to-bottom using whole-word
       boundary matching (\b). The first rule that matches wins immediately.
    4. Fallback Last: If no rule matches, return a helpful default reply.
    """
    # 1. Normalize the input
    clean_text = normalize(user_input)

    # Handle empty input (e.g., user just hits Enter or types only spaces/punctuation)
    if not clean_text:
        return "It looks like you didn't type anything! Please enter a message so we can chat."

    # 2. Check the Regex Rule FIRST ("my name is X")
    name_match = re.search(r"\bmy name is (\w+)\b", clean_text, re.IGNORECASE)
    if name_match:
        captured_name = name_match.group(1).capitalize()
        return f"Nice to meet you, {captured_name}!"

    # 3. Loop through Keyword Rules IN ORDER and return the first whole-word match
    for keywords, response in RULES:
        for kw in keywords:
            # \b ensures whole-word matching so "this" never triggers "hi"
            if re.search(rf"\b{re.escape(kw)}\b", clean_text):
                # If the response is a function (like our datetime rule), call it
                if callable(response):
                    return response()
                return response

    # 4. Fallback LAST when nothing else matched
    return FALLBACK_RESPONSE


def main() -> None:
    """Main interactive chat loop."""
    print("====================================================")
    print(" Welcome to CodeOrbit Rule-Based Chatbot! ")
    print(" Type a message to chat, or 'bye' / 'exit' to quit.")
    print("====================================================")

    while True:
        try:
            user_input = input("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye! Exiting chat.")
            break

        clean_text = normalize(user_input)

        # Print the bot's response
        reply = get_response(user_input)
        print(f"Bot: {reply}")

        # Exit cleanly if the user typed 'bye' or 'exit'
        if clean_text in ("bye", "exit"):
            break


if __name__ == "__main__":
    main()