# CodeOrbit Rule-Based Chatbot

## Project Overview & Purpose
A deterministic, zero-dependency command-line chatbot built in Python using regular expressions (`re`) and ordered keyword pattern matching. Designed to demonstrate foundational NLP preprocessing, deterministic intent routing, entity extraction (name capture), and graceful fallback handling without external libraries.

---

## How It Works (Rule Decision Tree)
Every incoming message is routed through a strict 4-stage decision pipeline in [`chatbot.py`](chatbot.py):

```text
User Input
  │
  ▼
[1. Normalize] ──► Lowercase + strip punctuation + collapse whitespace
  │
  ├──► Empty string? ──► Return polite empty-input prompt
  │
  ├──► Matches r"\bmy name is (\w+)\b"? ──► Extract name & greet personally
  │
  ├──► Loops RULES in priority order (whole-word \b regex match)
  │      ├── Greeting ("hi", "hello", "hey")
  │      ├── Status Check ("how are you", ...)
  │      ├── Identity FAQ ("whats your name", "who are you")
  │      ├── Capabilities ("help", "what can you do")
  │      ├── Live Date/Time (invokes datetime callable)
  │      ├── Gratitude ("thanks", "thank you", "thx")
  │      ├── Creator Info ("who made you", "creator")
  │      └── Farewell ("bye", "goodbye", "exit", "see you") ──► Exit loop
  │
  └──► No match ──► Return helpful FALLBACK_RESPONSE
```

- **Whole-Word Matching (`\b`):** Prevents substring false positives (e.g., `"this"` will never match `"hi"`).
- **Specific-Before-General Ordering:** Regex name capture executes before keyword matching so `"Hello, my name is Alice"` triggers personalized name recognition rather than a generic greeting.

---

## Setup & How to Run

1. Navigate into the project directory:
   ```bash
   cd CodeOrbit_RuleBasedChatbot
   ```
2. *(Optional)* Activate the virtual environment (standard library only, Python 3.10+):
   - **Windows PowerShell:**
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - **Git Bash / Linux / macOS:**
     ```bash
     source .venv/Scripts/activate
     ```
3. Run the chatbot:
   ```bash
   python chatbot.py
   ```

---

## Example Output

```text
====================================================
 Welcome to CodeOrbit Rule-Based Chatbot! 
 Type a message to chat, or 'bye' / 'exit' to quit.
====================================================

You: hello
Bot: Hello! How can I help you today?

You: My name is Alice
Bot: Nice to meet you, Alice!

You: what can you do
Bot: I can greet you, remember your name (try 'My name is ...'), tell the current time/date, and answer basic questions!

You: time
Bot: The current date and time is Thursday, November 12, 2026 at 07:19 AM.

You: xyzzy unknown
Bot: Sorry, I didn't understand. Try asking about 'what can you do', the current 'time', or introducing yourself with 'My name is [Your Name]'.

You: bye
Bot: Goodbye! Have a productive day ahead!
```
