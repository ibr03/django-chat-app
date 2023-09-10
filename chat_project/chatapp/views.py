from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import exception_handler
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegistrationSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from .models import UserProfile

class CustomObtainAuthToken(ObtainAuthToken):
    permission_classes = (AllowAny,)

@login_required
def chat_home(request):
    return render(request, 'chatapp/chat_home.html')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('chat_home')  # Redirect to chat homepage after registration
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# chatapp/views.py

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration_api(request):
    try:
        if request.method == 'POST':
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': True, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_online_users(request):
    online_users = UserProfile.objects.filter(online=True).values('user__username')
    return Response({'online_users': online_users}, status=status.HTTP_200_OK)

def custom_exception_handler(exc, context):
    # Handle exceptions and return custom error responses
    response = exception_handler(exc, context)

    if response is not None:
        response_data = {
            'error': True,
            'message': 'An error occurred while processing your request.'
        }
        response.data = response_data

    return response