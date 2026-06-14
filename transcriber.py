from mistralai.client import Mistral

from config import MISTRAL_API_KEY, MISTRAL_LANGUAGE, MISTRAL_MODEL


class MistralTranscriber:
    def __init__(self):
        if not MISTRAL_API_KEY:
            raise ValueError(
                "MISTRAL_API_KEY non définie. "
                "Créez un fichier .env à partir de .env.example"
            )
        self.client = Mistral(api_key=MISTRAL_API_KEY)

    def transcribe(self, audio_bytes):
        res = self.client.audio.transcriptions.complete(
            model=MISTRAL_MODEL,
            file={"file_name": "audio.wav", "content": audio_bytes},
            language=MISTRAL_LANGUAGE,
        )
        return res.text
