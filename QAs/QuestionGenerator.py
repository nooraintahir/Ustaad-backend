# imports
import pandas as pd
import numpy as np
import csv
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import random

data = pd.read_csv(".\\fixed_questions.csv")


def generate_similar_questions(tokenizer, model, existing_question, difficulty_level, reword=True, modify_values=True):

    prompt = f"Generate an {difficulty_level.lower()} question: {existing_question}"
    if reword:
        prompt += " (reworded)"
    if modify_values:
        prompt += " (with modified values)"

    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(**inputs, max_length=2000,
                             num_return_sequences=1, temperature=1.5, do_sample=True)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def BART(existing_question, difficulty_level):
    model_name = "facebook/bart-large-cnn"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    question = generate_similar_questions(
        tokenizer, model, existing_question, difficulty_level)

    return question


def generate_questions_and_save():
    generated_questions = []

    for index, row in data.iterrows():
        original_question = row['Question']
        difficulty = row['Difficulty']
        topic = row['Topic']

        # Truncate the input sequence length if it exceeds a certain threshold
        max_sequence_length = 512
        original_question = original_question[:max_sequence_length]

        # Generate a similar question using BART
        similar_question = BART(original_question, difficulty)

        # Append the generated question along with original difficulty and topic
        generated_questions.append({
            # 'og': original_question,
            'Question': similar_question,
            'Difficulty': difficulty,
            'Topic': topic
        })

    # Convert the list of dictionaries to DataFrame
    generated_questions_df = pd.DataFrame(generated_questions)

    # Save the DataFrame to a new CSV file
    generated_questions_df.to_csv('generated_questions_new.csv', index=False)

    return generated_questions_df


# to run this code in another file:

# import QuestionGenerator_v2 as qg
# qg.generate_questions_and_save()

# make sure you have the data.csv file in the same directory as the rest of your code
