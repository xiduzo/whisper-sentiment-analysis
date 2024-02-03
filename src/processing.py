from transformers import pipeline

classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
# another interesting classifier
# classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

def commands_callback(model_output):
    print("")
    print("")
    print("----------------------------------------------------")
    print("")
    print("user said:")
    print(model_output)
    print("")
    classified = classifier(model_output)[0]

    print("feels like:")
    for sentiment in classified:
        print(f"{sentiment['label'].ljust(8)} {sentiment['score']}")

    print("")
    print("----------------------------------------------------")
    print("")
    print("")