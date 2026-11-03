# Engineering Journal — Day 1: Rule-Based Chatbot

## 1. What I Studied
- **Python `re` Module:** Studied `re.search()`, raw strings (`r"..."`), case-insensitive matching (`re.IGNORECASE`), capture groups (`(\w+)`), and word boundaries (`\b`).
- **String Normalization:** Practiced chaining `.lower()`, `.strip()`, and `re.sub()` to sanitize noisy user input.
- **Control Flow:** Reviewed `while True` loops paired with `break` for interactive CLI programs.

## 2. What I Built
- Created `CodeOrbit_RuleBasedChatbot` with a virtual environment (`.venv`) and Git repository.
- Built `chatbot.py` with normalization, 8 ordered keyword rules, regex name capture, fallback handling, and a CLI loop.

## 3. Tests Run & Results
- **Empty Input:** Handled gracefully with a polite prompt.
- **Caps & Punctuation (`HELLO!!!`):** Normalized successfully and triggered greeting.
- **Substring Trap (`this is nice`):** Word boundaries (`\b`) prevented false positive on `"hi"`.
- **Regex Capture (`My name is Daniel`):** Successfully captured `"Daniel"` and replied.
- **Clean Exit (`bye`):** Exited the loop cleanly.

## 4. Tomorrow's Plan
- Review Day 2 internship tasks and expand the chatbot's capabilities.