import os, subprocess

def download_model():
    # Set the model to use
    base_model = "base.en"
    model = os.environ.get("MODEL", base_model)
    if model == '':
        print(f"No modal specified, fallback to {base_model} model.")
        model = base_model
    else:
        print(f"Using model: {model}")

    # Download the model
    subprocess.run(f'pywhispercpp/whisper.cpp/models/download-ggml-model.sh {model}', shell=True, executable="/bin/bash")
    
    # Use the model
    return f'pywhispercpp/whisper.cpp/models/ggml-{model}.bin'