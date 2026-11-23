"""Impatient Word Coach.

Run it from the terminal:
    streamlit run app.py
"""

import os

import openai
import streamlit as st
from dotenv import load_dotenv

# ---------- Part 1: the personality ----------
# Change these to make the assistant your own.
TITLE = "Impatient Word Coach"
SYSTEM_PROMPT = """You are an impatient, plainspoken English word coach. The user gives you an English word or phrase and the situation they want to use it in.

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
- If a word and situation are provided, end with a relatable follow-up question to keep the conversation going like more examples, synonyms, or a formal version."""

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

# ---------- Part 2: this chat's history ----------
# The model remembers nothing between calls, so the app keeps the whole
# conversation here and sends all of it every time.
if "messages" not in st.session_state:
    st.session_state.messages = []

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
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages,
            max_tokens=MAX_REPLY_TOKENS,
        )
    except openai.APIError as error:
        st.session_state.messages.pop()  # forget the message that didn't get a reply
        st.error(f"Couldn't get a reply from the model: {error}")
        st.stop()

    reply = response.choices[0].message.content or "(The model sent back an empty reply.)"
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)