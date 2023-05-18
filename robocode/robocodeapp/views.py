from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from rest_framework.decorators import api_view
import openai

openai.api_key = 'YOUR_OPENAI_API_KEY'

@api_view(['POST'])
def generate(request):
    prompt = request.data.get('prompt')

    # Generate code using OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )

    # Extract the generated code from the response
    generated_code = response.choices[0].text.strip()

    # Redact the generated code
    for word in ["password", "secret"]:
        generated_code = generated_code.replace(word, "REDACTED")

    # Correct the generated code
    generated_code = generated_code.replace("your_openai_api_key", "YOUR_OPENAI_API_KEY")

    # Return the redacted and corrected code
    return JsonResponse({"generated_code": generated_code})
