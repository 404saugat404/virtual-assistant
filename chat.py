import torch
import os
import json 
import random

# import Speech Engine
from core.engine import *
from core.intents import *

# import Intent 
from neuralnet.model import IntentModelClassifier
from neuralnet.nltk_utils import bag_of_words, tokenize

# import task automation functions
from directory import *

# Setting device agnostic code
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(device)

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

""" Load Intent_Classifier Trained Model """
MODEL_SAVE_PATH = "model/intent.pth"
model_info = torch.load(MODEL_SAVE_PATH)

input_size = model_info["input_size"]
hidden_size = model_info["hidden_size"]
output_size = model_info["output_size"]
all_words = model_info["all_words"]
tags = model_info["tags"]
model_state = model_info["model_state"]

# Instantiate IntentModelClassifier
model = IntentModelClassifier(
    input_size, 
    hidden_size, 
    output_size).to(device)

model.load_state_dict(model_state)
model.eval()


# ANSI escape codes for colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


bot_name = "ByteBot"
print("Let's chat! (type 'quit' to exit)")
while True:
    sentence = input(f"{GREEN}You{RESET}: ")
    if sentence == "quit" or sentence == "bye":
        break

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    # print(X.shape[0])
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    # print(f"Bot: {bot_name}, {tag}")

    probs = torch.softmax(output, dim=1)  # Assigns all proabability in range [0, 1]
    prob = probs[0, predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent['tag']:
                response = random.choice(intent['responses'])

                # Create Folder
                if tag == "Create":
                    # recognizer, mic, stream = initialize_model()
                    # print(user_input)
                    # folder_name = speech_recognize(recognizer, stream)
                    print(f"{RED}{bot_name}{RESET}: {response}")
                    folder_name = input(f"{GREEN}Name your folder{RESET}: ")
                    create_folder(folder_name)
                    
                elif tag == "Delete":
                    print(f"{RED}{bot_name}{RESET}: {response}")
                    folder_name = input(f"{GREEN}Name of folder{RESET}: ")
                    delete_folder(folder_name)



                else:
                    print(f"{RED}{bot_name}{RESET}: {response}")
                break
    else:
        print(f'{RED}{bot_name}{RESET}: I donot understand...')