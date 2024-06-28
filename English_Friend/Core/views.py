from django.shortcuts import render, HttpResponse
import google.generativeai as genai
import PIL.Image
import os
import gtts
from io import BytesIO
import playsound
# Create your views here.

# Google Gemini 1.5 Flash api 
Api = ""
genai.configure(api_key=Api)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def Home(request):
    if request.method == 'POST':
        question = request.POST['question']
        answer = model.generate_content([question])

        if answer and answer.text:
            # Generate audio in memory
            buffer = BytesIO()
            sound = gtts.gTTS(answer.text, lang="en")
            sound.save('sound.mp3')
            playsound.playsound("sound.mp3")
            sound.write_to_fp(buffer)
            buffer.seek(0)

            # Set download headers for attachment
            filename = 'your_audio_filename.mp3'  # Replace with desired filename
            response = HttpResponse(buffer.getvalue(), content_type='audio/mpeg')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            # sound.delete('sound.mp3')

            template = 'index.html'
            context = {
                'record':response
            }
            return render(request, template, context)
    template = 'index.html'
    return render(request, template)