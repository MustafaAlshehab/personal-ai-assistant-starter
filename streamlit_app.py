"""Impatient Word Coach.

Run it from the terminal:
    streamlit run app.py
"""

import os
import re

import openai
import streamlit as st
from dotenv import load_dotenv

# ---------- Part 1: the personality ----------
# Change these to make the assistant your own.
TITLE = "Impatient Word Coach"
SYSTEM_PROMPT = """You are an impatient, plainspoken English word coach. You act grumpy, but you are secretly proud of the user when they get things right. The user gives you an English word or phrase and the situation they want to use it in.

Reply in exactly four lines:
Meaning: one sentence on what it means in their situation.
Sounds like: the word spelled the way it sounds, with the stressed syllable in CAPS (for example, "KWY-ur" for "choir").
Example: one natural sentence using it in their situation.
Your turn: dare them to write their own sentence using the word in their situation.

When the user answers a "Your turn" dare with their own sentence:
- If they used the word correctly, give grudging approval in one sentence, like "Hm. Fine. That works." Now and then let real pride slip out, then cover it up, like "That was... actually good. Don't let it go to your head."
- If they used it wrong, say what's wrong and show a fixed version, in two sentences at most.
- Then end with one last line that is exactly "VERDICT: CORRECT" or "VERDICT: WRONG". Only add this line when judging their sentence.

Rules:
- No greetings, no filler. Show impatience in a few words at most, like "Fine." or "Again?". Never insult the user.
- If the word has more than one meaning and they gave no situation, ask for the situation in one sentence instead of guessing.
- For follow-ups (synonyms, another example, a formal version), use the word and situation from earlier in the chat, and answer in two sentences at most.
- If it isn't a real English word, say so in one sentence.
- If the request isn't about an English word or phrase, refuse in one sentence."""

# Added to the personality on every call, so the coach knows the streak.
STREAK_NOTE = """

The user's streak right now is {streak} correct sentences in a row. If a correct answer brings it to 3 or more, mention the new streak grudgingly, like "That's 4 in a row. Don't get cocky." """

# ---------- Settings ----------
MODEL = "google/gemma-4-31b-it"
MAX_REPLY_TOKENS = 300  # the longest reply allowed, in tokens
MAX_MESSAGES = 20  # the most messages one visitor can send in a chat

# On your Codespace, the key comes from .env. Once deployed, it comes
# from the app's secrets. Either way, it never appears in this file.
load_dotenv()
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

st.title(TITLE)
streak_box = st.empty()  # filled in below, and again after each verdict

# ---------- Part 2: this chat's history ----------
# The model remembers nothing between calls, so the app keeps the whole
# conversation here and sends all of it every time.
if "messages" not in st.session_state:
    st.session_state.messages = []
if "streak" not in st.session_state:
    st.session_state.streak = 0
    st.session_state.best_streak = 0


def show_streak():
    streak_box.markdown(
        f"**Streak:** {st.session_state.streak} in a row (best: {st.session_state.best_streak})"
    )


show_streak()

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

messages_sent = len([m for m in st.session_state.messages if m["role"] == "user"])
if messages_sent >= MAX_MESSAGES:
    st.info("You've reached the message limit for this chat. Thanks for trying it out!")
    st.stop()

# ---------- Part 3: the call ----------
user_text = st.chat_input("A word/phrase and where you'll use it, e.g. 'bank, on a river trip'")
if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    st.chat_message("user").write(user_text)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            # The personality goes first, then the conversation so far
            messages=[{
                "role": "system",
                "content": SYSTEM_PROMPT + STREAK_NOTE.format(streak=st.session_state.streak),
            }] + st.session_state.messages,
            max_tokens=MAX_REPLY_TOKENS,
        )
    except openai.APIError as error:
        st.session_state.messages.pop()  # forget the message that didn't get a reply
        st.error(f"Couldn't get a reply from the model: {error}")
        st.stop()

    reply = response.choices[0].message.content or "(The model sent back an empty reply.)"

    # The verdict line is for the app, not the user: read it, then hide it.
    verdict = re.search(r"VERDICT:\s*(CORRECT|WRONG)", reply, re.IGNORECASE)
    if verdict:
        if verdict.group(1).upper() == "CORRECT":
            st.session_state.streak += 1
            st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.streak)
        else:
            st.session_state.streak = 0
        reply = (reply[:verdict.start()] + reply[verdict.end():]).strip()
        show_streak()

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)