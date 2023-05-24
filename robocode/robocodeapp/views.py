from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
import openai
from django.contrib.auth.decorators import login_required
from typing import Any, cast
from .forms import SignUpForm, VerifyForm, LoginForm, PasswordResetForm, UserInfoForm, PasswordChangeForm
from .decorators import verification_required
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import ForgotPasswordSerializer, SignupSerializer, UserSerializer, ProfileSerializer, NotificationsSerializer, SubscriptionsSerializer, PasswordSerializer
from . import verify
from .models import User, Notifications, Subscriptions, Profile

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))


openai.api_key = os.getenv('YOUR_OPENAI_API_KEY')



@api_view(['POST'])
def login(request):  
    form = LoginForm(request.POST)    
    if request.method == 'POST':
        username = Profile.objects.get('username')
        password = request.data.get('password')
        phone_number = Profile.objects.get('phone_number')
        
        if not (username and password and phone_number):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=username, password=password)
        
        if Profile is not None:
            verify.send(phone_number)
            # Store user ID in the session or use a token-based authentication system (e.g., JWT)
            request.session['user_id'] = Profile.id
            return Response({'message': 'Verification code sent'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def generate(request):
    prompt = request.data.get('prompt')

    # Generate code using OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=100
    )

    # Extract the generated code from the response
    response = cast(Any, response)
    generated_code = response.choices[0].text.strip()

    # Redact the generated code
    for word in ["password", "secret"]:
        generated_code = generated_code.replace(word, "REDACTED")

    # Correct the generated code
    generated_code = generated_code.replace("your_openai_api_key", "YOUR_OPENAI_API_KEY")

    # Return the redacted and corrected code
    return JsonResponse({"generated_code": generated_code})


@api_view(['POST'])
def signup(request):       
    if request.method == 'POST':
        serializer = SignupSerializer(request.POST)
        if serializer.is_valid():
          if User is not None:
            serializer.save()
            verify.send(serializer.phone_number)
            return redirect('verify_code')
    else :
     return render(request, 'signup.dart')
    
               
@api_view(['POST'])        
@login_required
def verify_code(request):    
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if verify.check(User.phone_number, code):
                User.is_verified = True
                request.user.save()
                return redirect('index')
    else:
        form = VerifyForm()
    return redirect(request, 'verify_code')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def welcome(request):  
  if User is not None:
    return redirect('user_info_update')
  else:
    return redirect('signup')
  


@api_view(['POST'])
@verification_required
def forgot_password(request):       
    if request.method == 'POST':
        serializer = ForgotPasswordSerializer(request.POST)
        if serializer.is_valid():
          if User is not None:
            serializer.save()
            verify.send(serializer.phone_number)
            return redirect('new_password')
    else :
      return render(request, 'forgot_password')
    


@api_view(['POST'])
@verification_required
def new_password(request):       
    if request.method == 'POST':
          if User is not None:
            return redirect('login')
    else :
      return render(request, 'new_password.dart')
  
  
      
        
class UserDetailUpdateView(generics.RetrieveUpdateAPIView):  
  queryset = User.objects.all()
  serializer = ProfileSerializer

  def get_object(self):
    return self.request.user

  def update(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = UserSerializer(request.POST)
    if serializer.is_valid():     
      serializer.is_valid(raise_exception=False) 
      self.get_serializer(instance, data=request.data, partial=True)      
      self.perform_update(serializer)
    return Response(UserSerializer.data)
  
  
    
@api_view(['POST'])
@verification_required
@login_required
def change_password(request):  
    if request.method == 'POST':
        serializer = PasswordSerializer(data=request.POST)
        if serializer.is_valid():            
            user = authenticate(request, username=User.full_name, password=request.data['password1'])
            if user is not None:
                password = request.data['password1']
                user.set_password(password)
                user.save()
                login(request)
                messages.success(request, 'Your password was successfully updated!')
                
            else:
                messages.error(request, 'Invalid current password')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        serializer = UserSerializer()

    return render(request, 'change_password', {'serializer': serializer})
