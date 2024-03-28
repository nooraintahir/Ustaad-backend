import numpy as np
from Performance_classifier import classify_performance
import pandas as pd
from datetime import datetime


def generate_initial_lesson_plan(experience_level, preferred_frequency):
    # Define the starting topic based on experience level
    starting_topic = 'Variables'

    # Initialize variables for lesson plan
    lesson_plan = {
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Topic': starting_topic,
        'Questions present': [],
        'Score': 0
    }

    if experience_level == 0:
        difficulty = 'Easy'
    elif experience_level == 1:
        difficulty = 'Medium'
    elif experience_level == 2:
        difficulty = 'Hard'

    completed_questions = 0  # Initially, no questions are completed
    # Assuming all questions are of the preferred difficulty level
    total_questions = preferred_frequency
    # Display the number of completed questions out of total
    question = f'{difficulty}: {completed_questions}/{total_questions}'
    lesson_plan['Questions present'].append(question)
    q2 = 'Medium: 0/0'
    q3 = 'Hard: 0/0'
    lesson_plan['Questions present'].append(q2)
    lesson_plan['Questions present'].append(q3)

    return lesson_plan


''' 

# Example usage:
experience_level = 0  # 0: Noob, 1: Beginner, 2: Amateur
preferred_frequency = 3  # Preferred number of questions
initial_lesson_plan = generate_initial_lesson_plan(experience_level, preferred_frequency)

# Print initial lesson plan
print("Timestamp:", initial_lesson_plan['Timestamp'])
print("Topic:", initial_lesson_plan['Topic'])
print("Questions present:")
for question in initial_lesson_plan['Questions present']:
    print(question)
print("Score:", initial_lesson_plan['Score'])

# Convert lesson plan to DataFrame
lesson_plan_df = pd.DataFrame([initial_lesson_plan])

# Save initial lesson plan to CSV file
lesson_plan_df.to_csv('initial_lesson_plan.csv', index=False)

'''

# updation functions:

# update timestamp


def update_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def switch_topic(current_topic, current_difficulty, performance_classification):
    topic_order = ['Variables', 'Arithmetic',
                   'If-else', 'Loops', 'Arrays', 'Functions']
    topic_switched = False

    if performance_classification == 'good':
        for item in current_difficulty:
            if 'Hard' in item:
                _, hard_count = item.split(': ')[1].split('/')
                if hard_count != '0':
                    topic_switched = True
                    break

        if topic_switched:
            current_topic_index = topic_order.index(current_topic)
            if current_topic_index < len(topic_order) - 1:
                return topic_order[current_topic_index + 1], topic_switched
            else:
                return None, topic_switched
        else:
            return current_topic, topic_switched
    else:
        return current_topic, topic_switched


def update_questions_field(current_questions_present, performance_classification):
    current_questions_list = [q.strip() for q in current_questions_present.replace(
        "[", "").replace("]", "").split(",")]

    questions_count = {'Easy': 0, 'Medium': 0, 'Hard': 0}
    total_questions = 0

    for question in current_questions_list:
        parts = question.split(':')
        difficulty = parts[0].strip().replace("'", "")
        completion = parts[1].strip()

        completion = completion.replace("'", "").replace('"', '')

        try:
            completed, total = map(int, completion.split('/'))
            total_questions += total
            questions_count[difficulty] = total
        except ValueError:
            print(
                f"Error: Completion status '{completion}' is not in the expected format.")
            continue

    print("Detected counts for each difficulty level:")
    print(questions_count)
    print(total_questions)
    print(performance_classification)

   # Update questions based on performance classification and total number of questions
    if performance_classification == 'good':

        if total_questions == 1:
            if questions_count['Easy'] > 0:
                questions_count['Easy'] -= 1
                questions_count['Medium'] += 1
            elif questions_count['Medium'] > 0:
                questions_count['Medium'] -= 1
                questions_count['Hard'] += 1

        elif total_questions == 2:
            if questions_count['Easy'] == 2:
                questions_count['Easy'] -= 1
                questions_count['Medium'] += 1
            elif questions_count['Medium'] == 1:
                questions_count['Medium'] -= 1
                questions_count['Easy'] = 0
                questions_count['Hard'] = 1
            else:
                questions_count['Medium'] -= 1
                questions_count['Hard'] += 1

        elif total_questions == 3:
            if questions_count['Easy'] == 3:
                questions_count['Easy'] -= 1
                questions_count['Medium'] += 1
            elif questions_count['Easy'] == 2:
                questions_count['Easy'] -= 1
                questions_count['Medium'] += 1
            elif questions_count['Medium'] == 2:
                questions_count['Easy'] -= 1
                questions_count['Medium'] += 1
            elif questions_count['Medium'] == 3:
                questions_count['Medium'] -= 1
                questions_count['Hard'] += 1

        elif performance_classification == 'poor':
            pass

    updated_questions = [
        f'{difficulty}: 0/{questions_count[difficulty]}' for difficulty in ['Easy', 'Medium', 'Hard']]

    return updated_questions


def generate_updated_lesson_plan(current_lesson_plan_df, input_dataframe):

    performance_classification = classify_performance(input_dataframe)

    latest_lesson_plan_row = current_lesson_plan_df.loc[current_lesson_plan_df['Timestamp'].idxmax(
    )]
    print("Latest Lesson Plan:")
    print(latest_lesson_plan_row)

    current_topic = latest_lesson_plan_row['Topic']
    current_questions_present = latest_lesson_plan_row['Questions present']
    current_score = latest_lesson_plan_row['Score']

    updated_topic, switch_flag = switch_topic(
        current_topic, current_questions_present, performance_classification)
    timestamp = update_timestamp()

    if switch_flag == False:
        updated_questions_present = update_questions_field(
            current_questions_present, performance_classification)

    elif switch_flag == True:
        updated_questions_present = ['Easy: 0/3', 'Medium: 0/0', 'Hard: 0/0']

    updated_lesson_plan_df = pd.DataFrame({
        'Timestamp': [timestamp],
        'Topic': [updated_topic],
        'Questions present': [updated_questions_present],
    })

    return updated_lesson_plan_df


''' 
example usage:

# Provided data
input_df = {
    'score': [100, 100, 100, 100, 100, 100, 100],
    'completed': [1, 1, 1, 1, 1, 1, 1],
    'max_correct_questions': [5, 3, 3, 5, 3, 1, 1],
    'questions_correct': [5, 3, 3, 5, 3, 1, 1],
    'topics': [0, 0, 0, 0, 0, 0, 0],
    'timestamp': ['20/09/2013', '20/09/2013', '20/09/2013', '20/09/2013', '20/09/2013', '20/09/2013', '20/09/2013']
}

# Convert to DataFrame
input_data_frame = pd.DataFrame(input_df)

previous_lesson_plan_df = pd.read_csv('initial_lesson_plan.csv')
updated_lesson_plan_df = generate_updated_lesson_plan(previous_lesson_plan_df, input_data_frame)
print("Updated Lesson Plan:")
print(updated_lesson_plan_df)


'''
