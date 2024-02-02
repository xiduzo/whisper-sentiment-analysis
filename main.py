from transformers import pipeline
# https://github.com/abdeladim-s/pywhispercpp
from pywhispercpp.examples.assistant import Assistant

print("")
print("------------------------------")
print("    made with ❤️ by xiduzo    ")
print("------------------------------")
print("")

classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
# another interesting classifier
# classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

def commands_callback(model_output):
    print("")
    print("")
    print("------------------------------")
    print("")
    print("user said:")
    print(model_output)
    print("")
    classified = classifier(model_output)[0]

    print("feels like:")
    for sentiment in classified:
        print(f"{sentiment['label'].ljust(8)} {sentiment['score']}")

    print("")
    print("------------------------------")
    print("")
    print("")

# if you need a specific model, make sure to download it first
# How to download the model:
# 1. Clone the repository (git clone --recurse-submodules https://github.com/abdeladim-s/pywhispercpp.git)
# 2. Install the model (./pywhispercpp/whisper.cpp/models/download-ggml-model.sh <MODEL>)
# 3. Set the model path below (model = 'pywhispercpp/whisper.cpp/models/ggml-<MODEL>.bin')
model = 'pywhispercpp/whisper.cpp/models/ggml-base.bin'

# Settings, see https://github.com/abdeladim-s/pywhispercpp for more
my_assistant = Assistant(
    commands_callback=commands_callback,
    n_threads=8,
    model=model)

my_assistant.start()
