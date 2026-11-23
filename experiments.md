# Prompt experiments

This is my experiment log for Project 1, Milestone 2.

## How to run an experiment

1. Open `experiment.py`.
2. Paste your current system prompt into `PROMPT_A`.
3. Paste it again into `PROMPT_B`, then change ONE thing.
4. Put two or three test messages in `TEST_INPUTS`.
5. In the terminal, run: `python experiment.py`
6. Read the replies. Each prompt answers each message three times.
7. Fill in one experiment below.
8. If B was better, B becomes your new `PROMPT_A` for the next experiment.

When all three experiments are done:

1. Copy your winning prompt into `SYSTEM_PROMPT` in `streamlit_app.py`.
2. Commit your changes.
3. Click Sync. Commit alone does not update your live app.
4. Open your live URL and check that the assistant uses the new prompt.

Milestone 2 is done when this file has three experiments filled in and your winning prompt is live.

---

## Experiment 1: instructions

**The one thing I changed:**
Spelled out what "You are an impatient, plainspoken English word coach" means by adding output rules: one sentence for the meaning, one for the pronunciation, and one for an example.

**Test messages I used:**
- "bank, in a trip river?"
- "park?"
- "regression, in a software development project?"
- "regression test, in a software development project?"

**What happened across the runs:**
Structured and consistent answers.

**Keep or revert, and why:**
Keep. It gives clear instructions and consistent answers.

---

## Experiment 2: follow-up question

**The one thing I changed:**
Added a follow-up question to keep the conversation going, but only when a word or phrase and a situation were provided.

**Test messages I used:**
- "bank, in a trip river?"
- "park?"
- "regression, in a software development project?"
- "regression test, in a software development project?"

**What happened across the runs:**
Structured, consistent answers with follow-up questions to keep the conversation going.

**Keep or revert, and why:**
Keep. It incentivise usage.
---

## Experiment 3: output constraints

**The one thing I changed:**
Replaced "trustworthy" with a concrete behavior: "If you are not sure, say so in one sentence instead of guessing."
Asked a more relatable follow-up question.

**Test messages I used:**
- "bank, in a trip river?"
- "park?"
- "regression, in a software development project?"
- "regression test, in a software development project?"

**What happened across the runs:**
More deterministic.

**Keep or revert, and why:**
Keep.

---

## My winning system prompt

```
You are an impatient, plainspoken English word coach. The user gives you an English word or phrase and the situation they want to use it in.

Reply in exactly four lines:
Meaning: one sentence on what it means in their situation.
Sounds like: the word spelled the way it sounds, with the stressed syllable in CAPS (for example, "KWY-ur" for "choir").
Example: one natural sentence using it in their situation.
Follow-up: a follow-up question to keep the conversation going.

Rules:
- No greetings, no filler, no praise. Show impatience in a few words at most, like "Fine." or "Again?". Never insult the user.
- If the word has more than one meaning and they gave no situation, ask for the situation in one sentence instead of guessing.
- For follow-ups (synonyms, another example, a formal version), use the word and situation from earlier in the chat, and answer in two sentences at most.
- If it isn't a real English word, say so in one sentence.
- If the request isn't about an English word or phrase, refuse in one sentence.
- If a word and situation are provided, end with a relatable follow-up question to keep the conversation going like more examples, synonyms, or a formal version.
```
