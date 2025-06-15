import streamlit as st
import openai
import tempfile

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Chave da API (via secrets no Streamlit)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Davar Acolhe Voz")
st.markdown("Envie um áudio com sua pergunta ou desabafo. Davar vai te escutar.")
uploaded_file = st.file_uploader("Envie seu áudio (.mp3 ou .wav)", type=["mp3", "wav"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    st.info("Transcrevendo com Whisper...")
    audio_file = open(temp_audio_path, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="pt"
    )

    texto_transcrito = transcript.text
    st.subheader("Transcrição")
    st.write(texto_transcrito)

    st.info("Gerando resposta do Davar...")
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é um companheiro sensível, escutando com empatia. Responda com carinho e presença."},
            {"role": "user", "content": texto_transcrito}
        ]
    )
    resposta_davar = completion.choices[0].message.content
    st.subheader("Resposta do Davar")
    st.write(resposta_davar)

    # Áudio por voz removido temporariamente para compatibilidade no Streamlit Cloud
    st.info("⚠️ A resposta por voz será incluída em breve. Por enquanto, leia o texto acima.")
