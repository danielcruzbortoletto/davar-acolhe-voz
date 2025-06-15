import streamlit as st
import openai
import tempfile

# Chave da API da OpenAI (via secrets.toml)
openai.api_key = st.secrets["openai_api_key"]

st.title("Davar Acolhe Voz")
st.markdown("Envie um áudio com sua pergunta ou desabafo. Davar vai te escutar.")

# Upload do áudio
uploaded_file = st.file_uploader("Envie seu áudio (.mp3 ou .wav)", type=["mp3", "wav"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    st.audio(temp_audio_path, format="audio/mp3")
    st.info("Transcrevendo com Whisper...")

    with open(temp_audio_path, "rb") as audio_file:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="pt"
        )

    texto_transcrito = transcript.text
    st.subheader("Transcrição")
    st.write(texto_transcrito)

    st.info("Gerando resposta do Davar...")
    completion = openai.ChatCompletion.create(
        model="gpt-4o",
        mes


