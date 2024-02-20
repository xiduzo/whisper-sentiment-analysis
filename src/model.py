import os, subprocess

def download_model():
    model = os.environ.get("WHISPER_MODEL", "base.en")
    print(f"Using whisper model: {model}")

    # Download the model
    subprocess.run(f'pywhispercpp/whisper.cpp/models/download-ggml-model.sh {model}', shell=True, executable="/bin/bash")
    
    # Use the model
    return f'pywhispercpp/whisper.cpp/models/ggml-{model}.bin'