from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import openai
from typing import Any, cast


openai.api_key = 'YOUR_OPENAI_API_KEY'



@api_view(['POST'])
def login(request):
   def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

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
