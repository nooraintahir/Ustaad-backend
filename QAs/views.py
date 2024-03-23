from rest_framework import status
import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Exercise, User
from .serializer import ExerciseSerializer
from rest_framework.response import Response
import g4f
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
messages = []
# Create your views here.


class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication succeeds, log in the user
            login(request, user)
            return JsonResponse({"message": "Login successful"})
        else:
            # If authentication fails, return error response
            return JsonResponse({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)


class Signup(APIView):
    def post(self, request):
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
            return Response({"message": "Signup successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Failed to create user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ExView(APIView):
    def get(self, request):
        output = [{"title": output.title, 
                   "difficulty_level": output.difficulty_level,
                   "question": output.question,
                   "answers": output.answers}
                   for output in Exercise.objects.all()]
        return Response(output)
    

    def post(self, request):
        serializer = ExerciseSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        

'''
class ExView(viewsets.ModelViewSet):
    serializer_class = ExerciseSerializer
    queryset = Exercise.objects.all()
    '''

class CompileCPlusPlus(APIView):
    def post(self, request):
        client_secret = '0c4dfc1b49c97871aab1e4576bb9901ebd1171f6'  # Replace with your actual client secret

        # Check if 'code' is provided in the request data
        code = request.data.get('code')
        if code is None:
            return Response(
                {"error": "Code is required in the request data."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Define the API endpoint
        api_endpoint = 'https://api.hackerearth.com/v4/partner/code-evaluation/submissions/'

        # Prepare the request data
        data = {
            'lang': 'CPP17',  # Set the language to C++
            'source': code,
            'time_limit': 5,  # Set the execution time limit (in seconds)
            'memory_limit': 262144,  # Set the memory limit (in KB)
            'callback': 'http://127.0.0.1:8000/compiler'  # Replace with your callback URL
        }

        # Set the required headers
        headers = {
            'client-secret': client_secret,
            'content-type': 'application/json'
        }

        # Send the POST request to HackerEarth API
        response = requests.post(api_endpoint, json=data, headers=headers)

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

