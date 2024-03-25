import pandas as pd
import numpy as np
import csv
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import random

data = pd.read_csv(".\\QAs\\input_dataset.csv")

# Function to generate similar questions using BART


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

# Function to initialize BART model and generate questions


def BART(existing_question, difficulty_level):
    model_name = "facebook/bart-large-cnn"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    question = generate_similar_questions(
        tokenizer, model, existing_question, difficulty_level)
    return question

# Function to generate questions and save them


def generate_questions_and_save():
    # Initialize a dictionary to store selected questions for each category and difficulty level
    selected_questions = {category: {difficulty: [] for difficulty in [
        'Easy', 'Medium', 'Hard']} for category in data['Topic'].unique()}

    # Iterate over the original questions and select 30 questions for each category, 10 for each difficulty level
    for category in selected_questions.keys():
        for difficulty in selected_questions[category].keys():
            filtered_data = data[(data['Topic'] == category) & (
                data['Difficulty'] == difficulty)]

            print(
                f"Category: {category}, Difficulty: {difficulty}, Filtered Data Length: {len(filtered_data)}")

            if len(filtered_data) >= 10:
                selected_questions_list = filtered_data.sample(
                    n=10, replace=False, random_state=42)['Question'].tolist()
            else:
                selected_questions_list = filtered_data['Question'].tolist()

            # Store selected questions for the current category and difficulty level
            selected_questions[category][difficulty] = selected_questions_list

    print(len(selected_questions_list))

    # Initialize a list to store all selected questions
    all_selected_questions = []

    # Iterate over selected questions dictionary and accumulate all selected questions
    for category, difficulties in selected_questions.items():
        for difficulty, questions in difficulties.items():
            all_selected_questions.extend(questions)

    print("Total number of selected questions:", len(all_selected_questions))

    # Initialize a list to store generated questions
    generated_questions = []

    # Generate new questions for each selected question
    for category, difficulties in selected_questions.items():
        for difficulty, original_questions in difficulties.items():
            for original_question in original_questions:
                # Generate a similar question using BART
                similar_question = BART(original_question, difficulty)
                # Append the generated question along with original difficulty and topic
                generated_questions.append(
                    {'Question': similar_question, 'Difficulty': difficulty, 'Topic': category})

                print("Length of generated_questions:",
                      len(generated_questions))

    # Convert the list of dictionaries to DataFrame
    generated_questions_df = pd.DataFrame(generated_questions)

    # Save the DataFrame to a new CSV file
    generated_questions_df.to_csv('questions.csv', index=False)

    return generated_questions_df


# Call the function to generate questions and save them
# import QuestionGeneratorv3 as qg
# qg.generate_questions_and_save()
