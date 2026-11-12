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
    # Decision Branch 1: Greeting intent -> warm welcome and prompt for next action
    (
        ["hi", "hello", "hey"],
        "Hello! How can I help you today?",
    ),
    # Decision Branch 2: Conversational check-in FAQ -> polite status reply
    (
        ["how are you", "how is it going", "how are things"],
        "I'm doing great, thank you for asking! Ready to chat with you.",
    ),
    # Decision Branch 3: Bot identity FAQ -> state bot name and implementation
    (
        ["whats your name", "what is your name", "who are you"],
        "I am CodeOrbit Bot, a rule-based chatbot built with Python!",
    ),
    # Decision Branch 4: Capabilities / Help FAQ -> summarize supported intents
    (
        ["help", "what can you do"],
        "I can greet you, remember your name (try 'My name is ...'), tell the current time/date, and answer basic questions!",
    ),
    # Decision Branch 5: Live Date/Time FAQ -> callable executes on match for fresh timestamps
    (
        ["time", "date", "what time is it", "today"],
        lambda: f"The current date and time is {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}.",
    ),
    # Decision Branch 6: Gratitude FAQ -> acknowledge thanks politely
    (
        ["thanks", "thank you", "thx"],
        "You're very welcome! Happy to help.",
    ),
    # Decision Branch 7: Creator / Attribution FAQ -> explain author and project context
    (
        ["who made you", "who created you", "creator"],
        "I was built by Daniel as part of the CodeOrbit AI Internship!",
    ),
    # Decision Branch 8: Farewell / Exit intent -> deliver closing message (also terminates chat loop)
    (
        ["bye", "goodbye", "exit", "see you"],
        "Goodbye! Have a productive day ahead!",
    ),
]

EXIT_RESPONSE = RULES[-1][1]

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
    # Stage 1: Normalize the raw text (lowercase + strip punctuation + collapse spaces)
    clean_text = normalize(user_input)

    # Branch A (Empty Input Guard): User hit Enter or sent only whitespace/punctuation
    if not clean_text:
        return "It looks like you didn't type anything! Please enter a message so we can chat."

    # Branch B (Specific Regex Rule First): Capture user's name before general keyword checks
    # so inputs like "Hello, my name is Daniel" personalize the greeting immediately.
    name_match = re.search(r"\bmy name is (\w+)\b", clean_text, re.IGNORECASE)
    if name_match:
        captured_name = name_match.group(1).capitalize()
        return f"Nice to meet you, {captured_name}!"

    # Branch C (Ordered Keyword FAQ Matching): Evaluate RULES sequentially top-to-bottom
    for keywords, response in RULES:
        for kw in keywords:
            # \b enforces whole-word matching so substrings like "this" never trigger "hi"
            if re.search(rf"\b{re.escape(kw)}\b", clean_text):
                # Sub-branch C1: Dynamic rule (e.g., current time) invokes its callable
                if callable(response):
                    return response()
                # Sub-branch C2: Static FAQ/greeting rule returns its predefined string
                return response

    # Branch D (Default Fallback): No pattern or keyword matched; guide user to valid prompts
    return FALLBACK_RESPONSE


def main() -> None:
    """Main interactive chat loop."""
    print("====================================================")
    print(" Welcome to CodeOrbit Rule-Based Chatbot! ")
    print(" Type a message to chat, or 'bye' / 'exit' to quit.")
    print("====================================================")

    while True:
        # Handle EOF (piped input ending) or Ctrl+C gracefully without a traceback
        try:
            user_input = input("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye! Exiting chat.")
            break

        # Dispatch input through the 4-stage decision pipeline and display reply
        reply = get_response(user_input)
        print(f"Bot: {reply}")

        # Exit branch: Terminate the loop whenever the farewell rule was triggered
        if reply == EXIT_RESPONSE:
            break


if __name__ == "__main__":
    main()