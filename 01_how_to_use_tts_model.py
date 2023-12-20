# Source of the below information: https://platform.openai.com/docs/guides/text-to-speech
# Audio API provides a speech endpoint that comes with 6 in-built voice
# usage policy requires you to disclose that this a AI voice
# Supported output format
# Opus: For internet streaming and communication, low latency.
# AAC: For digital audio compression, preferred by YouTube, Android, iOS.
# FLAC: For lossless audio compression, favored by audio enthusiasts for archiving.
# Supports the same languages as whisper
# The Speech API provides support for real time audio streaming using chunk transfer encoding.
# This means that the audio is able to be played before the full file has been generated and made accessible.
import base64
import os
import time

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or st.secrets['OPENAI_API_KEY']
client = OpenAI(api_key=OPENAI_API_KEY)

with st.sidebar:
    st.header("Settings")
    voice = st.selectbox("Select Voice", ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'], index=0)
    model = st.selectbox("Select Model", ['tts-1','tts-1-hd'], index=0)


with st.container():
    with st.form(key="chat_form", clear_on_submit=True):
        text = st.text_area("Enter your text")
        submit_button = st.form_submit_button("speak up")
        if submit_button:
            speech_file_path = "./{voice}.mp3".format(voice=voice)
            response = client.audio.speech.create(
                model=model,
                voice=voice,
                input=text
            )

            response.stream_to_file(speech_file_path)

            with open(speech_file_path, "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                md = f"""
                    <audio controls autoplay="true">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                    """
                sound = st.empty()
                sound.markdown(
                    md,
                    unsafe_allow_html=True,
                )
                time.sleep(3)
                sound.empty()

                os.remove(speech_file_path)
