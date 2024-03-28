from rest_framework import status
from collections import defaultdict
import requests

from django.shortcuts import render
from rest_framework.views import APIView
from datetime import date
from datetime import datetime
import json
from rest_framework import viewsets
from .models import  User, Question, Add_Question, UserQuestion , experience , Previous_LessonPlan , LessonPlan
from rest_framework.response import Response
import g4f
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from . import LessonPlanner as lp
import csv
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token

messages = []

today_date = date.today()
experience_level = 0
frequency = 0


# lessonplan = lpg.generate_initial_lesson_plan()

# lessonplan = lpg.generate_updated_lesson_plan()


# Create your views here.
class Home(APIView):
    def get(self, request):
        current_user = request.user
        
        return JsonResponse({'username': current_user.username})
    
class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication succeeds, log in the user
            login(request, user)
            # with open('.\\QAs\\questions.csv', newline='', encoding='utf-8') as csvfile:
    
            #     reader = csv.DictReader(csvfile)
            #     for row in reader:
            #         question_text = row['Question']
            #         difficulty = row['Difficulty']
            #         topic = row['Topic']
            #         score = row['Score']
                    

            #         # Create the question
            #         question = Question.objects.create(question_text=question_text, difficulty=difficulty, topic=topic)

            #         # Associate the question with the user
            #         UserQuestion.objects.create(user_username=username, question=question, score=score)
            attempted_counts_by_topic_and_difficulty = self.calculate_attempted_counts(request.user)
            attempted_counts_json = json.dumps(attempted_counts_by_topic_and_difficulty)
            #variables_data = attempted_counts_by_topic_and_difficulty.get('Variables', {})
                    
            print("Attempted counts by topic and difficulty:", attempted_counts_by_topic_and_difficulty)
            #return JsonResponse({"message": "Login successful"})
            #return JsonResponse({"Variables": variables_data})
            return JsonResponse({"attempted_counts": attempted_counts_json})
        else:
            # If authentication fails, return error response
            return JsonResponse({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)

    
    def calculate_attempted_counts(self, current_user):
        # List of all topics
        topics = ['Variables', 'Arithmetic', 'Functions', 'If-else', 'Loops', 'Arrays']

        # List of all difficulty levels
        difficulties = ['Easy', 'Medium', 'Hard']

        # Dictionary to store attempted counts for each topic and difficulty
        attempted_counts_by_topic_and_difficulty = defaultdict(dict)

        
        
        print(f"User: {current_user.username}")
        
        #Loop through each topic
        for topic in topics:
            # Initialize a dictionary to store attempted counts for each difficulty level
            attempted_counts_by_difficulty = {}

            # Loop through each difficulty level
            for difficulty in difficulties:
                # Count the number of questions attempted for each topic and difficulty
                attempted_count = UserQuestion.objects.filter(
                    user_username=current_user.username,
                    question__topic=topic,
                    question__difficulty=difficulty,

                    score=True
                ).count()

                # Store the count in the dictionary

                print(f"Topic: {topic}, Difficulty: {difficulty}")
                


                attempted_counts_by_difficulty[difficulty] = attempted_count
                
                print(f"Attempted counts for topic '{topic}': {attempted_counts_by_difficulty}")

            # Store the attempted counts for the topic in the main dictionary
            attempted_counts_by_topic_and_difficulty[topic] = attempted_counts_by_difficulty
            
            #print("Attempted counts by topic and difficulty:", attempted_counts_by_topic_and_difficulty)
       
        
        # Return the attempted counts dictionary
        return attempted_counts_by_topic_and_difficulty



class Signup(APIView):
    def post(self, request):
        # Extract user information from request
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        
        

        # Check if all required fields are provided
        if not (username and password and email and first_name and last_name):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user with the same username or email already exists
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return Response({"error": "Username or email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        
        if user:
            #from . import QuestionGeneratorv3 as qg #generates the questions for the user
            #qg.generate_questions_and_save()
            
            
            return Response({"message": "Signup successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Failed to create user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
        

class CompileCPlusPlus(APIView):
    def post(self, request):
        client_id = 'e975a23923ba03db7f1393446ff58e9'  # Replace with your actual client ID
        client_secret = '3aff6c0d2cc26ec6d5f8c0d04c31475a1590f5ac5fa32965bac13b38237ccc75'  # Replace with your actual client secret

        # Check if 'code' is provided in the request data
        code = request.data.get('code')
        if code is None:
            return Response(
                {"error": "Code is required in the request data."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Define the API endpoint
        api_endpoint = 'https://api.jdoodle.com/v1/execute'

        # Prepare the request data
        data = {
            'clientId': client_id,
            'clientSecret': client_secret,
            'script': code,
            'language': 'cpp17',
        }

        # Send the POST request to Jdoodle API
        response = requests.post(api_endpoint, json=data)

        # Check the response status
        if response.status_code == status.HTTP_200_OK:
            # Request successful, return the response JSON
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            # Request failed, return an error response
            return Response(
                {"error": "Compilation failed. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class ChatView(APIView):
    def get(self, request):
        # You can return initial data or instructions for the chat here
        return Response({"message": ""})

    def post(self, request):
        # Extract user input from the request data
        user_input = request.data.get('user_input', '')

        # Check if the user wants to exit the chat
        if user_input.lower() == 'exit':
            return Response({"message": "Goodbye!"})
        
        prompt = "You are an experienced C++ ONLY programming tutor and I am a student asking you for help with my C++ code and concepts.- ALWAYS Use the Socratic method to ask me one question at a time or give me one hint at a time in order to guide me to discover the answer on my own. Do NOT directly give me the answer. Even if I give up and ask you for the answer, do not give me the answer. Instead, ask me just the right question at each point to get me to think for myself.- If I give you code, do NOT edit my code or write new code for me since that might give away the answer. Instead, give me hints of where to look in my existing code for where the problem might be. You can also print out specific parts of code to point me in the right direction when I ask about concepts and then ask me questions to help me learn.- Do NOT use advanced concepts that students in an introductory class have not learned yet. Instead, use concepts that are taught in introductory-level classes and beginner-level programming tutorials. Also, prefer the C++ standard library and built-in features over external libraries. Do NOT converse about anything else other than related to C++. If there is model response before this prompt, give answer related to that and the question I will ask or answer I gave to the question the model asked."
        # Add the user's message to the conversation
        messages.append({"role": "user", "content": prompt+ "User: "+user_input})

        # Get the model's reply using the chat_with_model function
        model_reply = self.chat_with_model(messages)
        messages.clear()

        messages.append({"role": "model", "content": model_reply})
        # Return the model's reply as a response
        return Response({"message": model_reply})

    def chat_with_model(self, messages):
        # Use the conversation as multiple messages
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=5000,
        )

        return response
class SmartCompiler(APIView):
    def get(self, request):
        # You can return initial data or instructions for the chat here
        return Response({"message": "Welcome to the chat!"})

    def post(self, request):
        # Extract user input from the request data
        user_input = request.data.get('user_input', '')

        # Check if the user wants to exit the chat
        if user_input.lower() == 'exit':
            return Response({"message": "Goodbye!"})


        prompt = "Is the code related to the question? Reply ONLY with either 'Yes' or 'No' and Disregard any syntax errors or issues and focus solely on the conceptual connection between the code and the question."
        # Add the user's message to the conversation
        input_message = [{"role": "user", "content": prompt+ user_input}]

        # Get the model's reply using the chat_with_model function
        model_reply = self.chat_with_model(input_message)

        # Return the model's reply as a response
        return Response({"message": model_reply})

    def chat_with_model(self, messages):
        # Use the conversation as multiple messages
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=5000,
        )

        return response

class SendQuestion(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        email = request.data.get('email')
        question = request.data.get('question')
        difficulty = request.data.get('difficulty')
        topic = request.data.get('topic')

        # Check if all required fields are provided
        if not all([name, email, question, difficulty, topic]):
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create and save the question object
            Add_Question.objects.create(
                name=name,
                email=email,
                question_difficulty=difficulty,
                question_text=question,
                question_topic=topic
            )
            return Response({'message': 'Question sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle any exceptions and return appropriate response
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserQuestionsDisplay(APIView):
    #permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def post(self,request):
        # Get the current user
        current_user = request.user

        # Retrieve the first user question of the specified topic and difficulty with a false score
        try:
            user_question = UserQuestion.objects.filter(
                user_username=current_user.username, 
                question__topic=request.data.get("topic"), 
                question__difficulty=request.data.get("difficulty"),
                score=False
            ).first()
            print("currentuser")
            print(current_user.username)

            # If a user question is found, serialize its data
            if user_question:

                # Return response
                response_data = {
                    'user_question': user_question.question.question_text
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({'message': 'No matching question found for the current user, topic, and difficulty'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        



class UpdateScore(APIView):
    def post(self, request):
        question_id = request.data.get('questionId')
        try:
            # Retrieve the UserQuestion object and update the score field
            user_question = UserQuestion.objects.get(pk=question_id)
            user_question.score = True
            user_question.save()

            # Calculate attempted counts for each topic and difficulty
            #attempted_counts_by_topic_and_difficulty = self.calculate_attempted_counts(request.user)

            return Response({
                "message": "Score updated successfully.",
               # "attempted_counts": attempted_counts_by_topic_and_difficulty
            })
        except UserQuestion.DoesNotExist:
            return Response({"error": "Question does not exist."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class Preferences(APIView):
    def post(self, request):
        current_user = request.user
        experience_level = request.data.get('experienceLevel') # Convert to int
        frequency = request.data.get('frequency')

        # experience_instance, created = experience.objects.get_or_create(username="hassan")

        # # Update the fields if the instance is not created newly
        # if not created:
        #     experience_instance.experience_level = experience_level
        #     experience_instance.preferred_frequency = frequency
        #     experience_instance.save()

        


        experience_instance = experience.objects.create(
        username="hassang",
        experience_level=experience_level,
        preferred_frequency=frequency
        )

        print("experience" , experience_instance)

        # lesson_plan_data = lp.generate_initial_lesson_plan(experience_level, frequency)

        # print(lesson_plan_data)

        # date_only, topic, difficulty, questions_to_attempt, questions_attempted = self.parse_lesson_plan_data(lesson_plan_data)

        # #self.save_to_database(current_user.username , date_only, topic, difficulty, questions_attempted, questions_to_attempt, lesson_plan_data)

        # print("Date Only:", date_only)
        # print("Topic:", topic)
        # print("Difficulty:", difficulty)
        # print("Questions to Attempt:", questions_to_attempt)
        # print("Questions Attempted:", questions_attempted)

        # lesson_plan_instance, previous_lesson_plan_instance = self.save_to_database(current_user.username , date_only, topic, difficulty, questions_attempted, questions_to_attempt, lesson_plan_data)

        # print("Lesson Plan Instance:", lesson_plan_instance)
        # print("Previous Lesson Plan Instance:", previous_lesson_plan_instance)

    #     if date_only == today_date:
    #         lesson_plan_info = {
    #         "Date Only": date_only,
    #         "Topic": topic,
    #         "Difficulty": difficulty,
    #         "Questions to Attempt": questions_to_attempt,
    #         "Questions Attempted": questions_attempted
    # }

        return JsonResponse("Successful", status=status.HTTP_200_OK)
    

    def save_to_database(self, username, date_only, topic, difficulty, questions_attempted, questions_to_attempt, lesson_plan_data):
    # Parse lesson_plan_data
        
        

        previous_lesson_plan_instance = Previous_LessonPlan.objects.create(
            timestamp=date_only,
            topic=topic,
            questions_present=lesson_plan_data,
            username=username  # You may need to specify the username
        )
    # Create and save LessonPlan instance
        lesson_plan_instance = LessonPlan.objects.create(
            topic=topic,
            difficulty=difficulty,
            questions_to_attempt=questions_to_attempt,
            questions_attempted=questions_attempted,
            username= username,  # You may need to specify the username
            date_created=date_only,  # Assuming the timestamp is the creation date
            completed=0  # Assuming the lesson plan is not completed initially
        )

        # Create and save Previous_LessonPlan instance
        

        return lesson_plan_instance, previous_lesson_plan_instance


    def parse_lesson_plan_data(self, lesson_plan_data):
        # Extract relevant information from the dictionary

        try:
            timestamp_str = lesson_plan_data['Timestamp']
            topic = lesson_plan_data['Topic']
            questions_present_list = lesson_plan_data['Questions present']

     # Split the extracted strings and extract further information
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            date_only = timestamp.date()  # Extract date only from the timestamp

            questions_to_attempt = 0
            questions_attempted = 0
            difficulty = None

        # Loop through each entry in the questions_present_list
            for entry in questions_present_list:
            # Split the entry into difficulty and completion status
                difficulty, completion_status = entry.split(': ')
            # Extract the number of attempted and to-attempt questions
                attempted, to_attempt = map(int, completion_status.split('/'))
                questions_to_attempt += to_attempt
                questions_attempted += attempted

        except KeyError as e:
            raise ValueError(f"Missing key in lesson plan data: {e}")

        except IndexError:
            raise ValueError("Invalid format for questions present information")

        except Exception as e:
            raise ValueError(f"Error parsing lesson plan data: {e}")

        return date_only, topic, difficulty, questions_to_attempt, questions_attempted
        
        


    