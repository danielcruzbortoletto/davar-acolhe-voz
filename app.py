import streamlit as st
import tempfile
from openai import OpenAI
import os

# Configurar cliente com chave da API vinda do secrets
client = OpenAI(api_key=st.secrets["openai_api_key"])

# Título e instruções
st.set_page_config(page_title="Davar Acolhe Voz", layout="centered")
st.title("🎙️ Davar Acolhe Voz")
st.markdown("Envie um áudio com sua pergunta ou desabafo. Davar vai te escutar com carinho.")

# Upload de arquivo de áudio
uploaded_file = st.file_uploader("📎 Envie seu áudio (.mp3 ou .wav)", type=["mp3", "wav"])

if uploaded_file is not None:
    # Salva arquivo temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    st.info("🎧 Transcrevendo com Whisper...")
    with open(temp_audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="pt"
        )

    texto_transcrito = transcript.text
    st.subheader("📝 Transcrição")
    st.write(texto_transcrito)

    # Geração de resposta com empatia
    st.info("💬 Gerando resposta do Davar...")
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Você é um companheiro sensível. Responda com escuta acolhedora, empatia e presença."
            },
            {
                "role": "user",
                "content": texto_transcrito
            }
        ]
    )

    resposta = completion.choices[0].message.content
    st.subheader("🧠 Resposta do Davar")
    st.write(resposta)

    # Placeholder para áudio
    st.warning("⚠️ A resposta por voz será incluída em breve. Por enquanto, leia o texto acima com atenção e carinho.")
