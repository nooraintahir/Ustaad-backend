from rest_framework import status
import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Exercise
from .serializer import ExerciseSerializer
from rest_framework.response import Response
import g4f
# Create your views here.


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
                status=status.HTTP_INTERNAL_SERVER_ERROR
            )
        
class ChatView(APIView):
    def get(self, request):
        # You can return initial data or instructions for the chat here
        return Response({"message": "Welcome to the chat!"})

    def post(self, request):
        # Extract user input from the request data
        user_input = request.data.get('user_input', '')

        # Check if the user wants to exit the chat
        if user_input.lower() == 'exit':
            return Response({"message": "Goodbye!"})

        # Add the user's message to the conversation
        messages = [{"role": "user", "content": user_input + " in c++ "+ "(tell in simplest way for a beginner with examples)"}]

        # Get the model's reply using the chat_with_model function
        model_reply = self.chat_with_model(messages)

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