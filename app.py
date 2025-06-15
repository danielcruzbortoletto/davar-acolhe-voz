import streamlit as st
import openai
import tempfile
import os
import csv
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis do ambiente
load_dotenv()

# Configurar chave da API
openai.api_key = st.secrets["openai_api_key"]

# Função para salvar logs localmente
def salvar_log(audio_transcricao, resposta_gerada):
    with open("logs_davar.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), audio_transcricao, resposta_gerada])

# Interface acolhedora
st.title("🌷 Davar Acolhe Voz")
st.markdown("**Envie um áudio com sua pergunta, desabafo ou apenas para ser escutado.**\n\nDavar vai te ouvir com carinho, presença e sem pressa.")

uploaded_file = st.file_uploader("🎙️ Envie seu áudio (MP3 ou WAV)", type=["mp3", "wav"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    st.info("🎧 Transcrevendo com carinho...")
    audio_file = open(temp_audio_path, "rb")

    # Transcrição com Whisper
    transcript = openai.Audio.transcribe(
        model="whisper-1",
        file=audio_file,
        language="pt"
    )
    texto_transcrito = transcript["text"]
    st.subheader("📝 O que você disse")
    st.write(texto_transcrito)

    # Geração da resposta
    st.info("💬 Gerando uma resposta com escuta...")
    completion = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Você é um companheiro sensível, escutando com empatia. Responda com carinho, presença e respeito."
            },
            {
                "role": "user",
                "content": texto_transcrito
            }
        ]
    )
    resposta_davar = completion["choices"][0]["message"]["content"]
    st.subheader("🧠 Resposta do Davar")
    st.write(resposta_davar)

    # Salvar log local
    salvar_log(texto_transcrito, resposta_davar)

    # Aviso de voz
    st.info("⚠️ Em breve, Davar também poderá responder com voz. Por enquanto, leia a resposta acima com atenção e carinho.")

    # Botão para nova pergunta
    if st.button("🔄 Fazer outra pergunta"):
        st.experimental_rerun()
