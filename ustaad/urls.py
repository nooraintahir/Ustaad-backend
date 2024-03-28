
#from rest_framework import routers

#router = routers.DefaultRouter()
#router.register(r'questions', views.ExView, 'questions')




from django.urls import path
from QAs.views import SendQuestion, CompileCPlusPlus, ChatView, SmartCompiler, Login, Signup, UserQuestionsDisplay, Home , UpdateScore, Preferences, ProgressTracking, LessonPlan

urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('compiler', CompileCPlusPlus.as_view(), name='compiler_app'),
    path('chatbot', ChatView.as_view(), name='chatbot'),
    path('smartcompiler', SmartCompiler.as_view(), name='smartcompiler'),
    path('login/', Login.as_view(), name='login'),
    path('signup/', Signup.as_view(), name='signup'),
    path('sendquestion', SendQuestion.as_view(), name='sendquestion'),
    path('userquestions', UserQuestionsDisplay.as_view(), name='userquestions'),
    path('update-score', UpdateScore.as_view(), name='update-score'),
    path('preferences', Preferences.as_view(), name='preferences'),
    path('progress', ProgressTracking.as_view(), name='progress'),
    path('lessonplan', LessonPlan.as_view(), name='lessonplan'),


]
