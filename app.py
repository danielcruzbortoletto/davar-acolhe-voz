import streamlit as st
import openai
import tempfile
import pyttsx3
import os

# Configuração da API OpenAI
openai.api_key = st.secrets["openai_api_key"] 

st.info(f"🔐 Chave carregada? {'✅' if openai.api_key.startswith('sk-') else '❌'}")

if "openai_api_key" in st.secrets else "SUA_CHAVE_AQUI"
client = openai.OpenAI(api_key=openai.api_key)

st.title("Davar Acolhe Voz")
st.write("Envie um áudio com sua pergunta ou desabafo. Davar vai te escutar.")

# Upload do áudio
uploaded_file = st.file_uploader("Envie seu áudio (.mp3 ou .wav)", type=["mp3", "wav"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    st.audio(temp_audio_path, format="audio/mp3")
    st.info("Transcrevendo com Whisper...")

    with open(temp_audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="pt"
        )

    texto_usuario = transcript.text
    st.subheader("Transcrição")
    st.write(texto_usuario)

    st.info("Gerando resposta do Davar...")
    prompt_davar = (
        "Você é uma presença acolhedora, que responde com escuta, sensibilidade e cuidado."
        f" A pessoa disse: '{texto_usuario}'"
    )

    resposta = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é o Davar, um ser de escuta."},
            {"role": "user", "content": prompt_davar}
        ]
    )

    resposta_davar = resposta.choices[0].message.content

    st.subheader("Resposta do Davar")
    st.write(resposta_davar)

    # Geração de áudio com voz simulada (pyttsx3)
    st.info("Gerando áudio da resposta...")
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    audio_out_path = temp_output.name
    engine.save_to_file(resposta_davar, audio_out_path)
    engine.runAndWait()

    st.subheader("Ouvir resposta do Davar")
    st.audio(audio_out_path, format="audio/mp3")

    # Limpeza opcional dos arquivos temporários
    # os.remove(temp_audio_path)
    # os.remove(audio_out_path)

else:
    st.info("Aguardando envio de um áudio...")
