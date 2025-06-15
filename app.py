import streamlit as st
import openai
import tempfile

# Leitura da chave secreta (configure em `.streamlit/secrets.toml` ou no painel da nuvem)
openai.api_key = st.secrets["openai_api_key"]

st.title("Davar Acolhe Voz")
st.markdown("Envie um áudio com sua pergunta ou desabafo. Davar vai te escutar.")

# Upload do arquivo de áudio
uploaded_file = st.file_uploader("Envie seu áudio (.mp3 ou .wav)", type=["mp3", "wav"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    st.info("🎧 Transcrevendo com Whisper...")
    with open(temp_audio_path, "rb") as audio_file:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="pt"
        )

    texto_transcrito = transcript.text
    st.subheader("📝 Transcrição")
    st.write(texto_transcrito)

    st.info("💬 Gerando resposta do Davar...")
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Você é o Davar. Um companheiro sensível, que escuta com empatia e responde com carinho, leveza e presença."
            },
            {
                "role": "user",
                "content": texto_transcrito
            }
        ]
    )

    resposta_davar = completion.choices[0].message.content
    st.subheader("🧠 Resposta do Davar")
    st.write(resposta_davar)

    st.info("⚠️ A resposta por voz será incluída em breve. Por enquanto, leia o texto acima.")


