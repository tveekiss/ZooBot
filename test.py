import os
from config import animals_answers

keys = list(animals_answers.keys())
for root, dirs, files in os.walk('./image'):
    if keys[0] in files:
        print(root)

