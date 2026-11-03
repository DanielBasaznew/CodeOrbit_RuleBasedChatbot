# CodeOrbit Rule-Based Chatbot (Day 1)

A deterministic, rule-based command-line chatbot built in Python using regular expressions (`re`) and ordered keyword matching.

## What It Does
- **Input Normalization:** Cleans user messages by lowercasing text, removing punctuation, and collapsing extra spaces.
- **Regex Name Capture:** Extracts and remembers the user's name from sentences like `"My name is Daniel"` using regex capture groups (`(\w+)`).
- **Ordered Keyword Rules:** Responds to 8 distinct categories (greetings, status check, bot identity, help menu, live date/time via `datetime`, thanks, creator info, and goodbyes) using whole-word boundary matching (`\b`).
- **Smart Fallback:** Gracefully handles empty inputs and unknown messages with helpful suggestions instead of crashing.

## How It Works (Decision Flow)
1. **Normalize:** Lowercases text, strips punctuation, and removes extra whitespace.
2. **Regex Rule First:** Checks `r"\bmy name is (\w+)\b"` before general keywords.
3. **Keyword Rules in Order:** Iterates through `RULES` top-to-bottom using `\b` word boundaries; the first match wins immediately.
4. **Fallback Last:** Returns a helpful default prompt if no rule matches.

## How to Run It

1. Clone this repository and navigate into the project directory:
   ```bash
   cd CodeOrbit_RuleBasedChatbot