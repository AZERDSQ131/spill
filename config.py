import os

HOTKEY_KEY = "fn"
SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = "int16"
MISTRAL_MODEL = "voxtral-mini-latest"
MISTRAL_LANGUAGE = "fr"
RECORDING_TIMEOUT = 60
OVERLAY_OPACITY = 0.88


def load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, _, value = line.partition("=")
                    if key and value:
                        os.environ[key.strip()] = value.strip().strip("\"'")


load_env()

MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", "")
