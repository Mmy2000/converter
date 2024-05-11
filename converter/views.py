from webvtt import WebVTT
import io

# Create your views here.

# views.py
from django.shortcuts import render
from .forms import VTTUploadForm
from .models import ConvertedFile

def upload_vtt(request):
    if request.method == 'POST':
        form = VTTUploadForm(request.POST, request.FILES)
        if form.is_valid():
            vtt_file = request.FILES['vtt_file']  # Get the uploaded file
            vtt_content = vtt_file.read().decode('utf-8')  # Read its content
            converted_text = convert_vtt_to_text(vtt_content)  # Call the conversion function
            converted_file = ConvertedFile.objects.create(original_vtt=vtt_file, converted_text=converted_text)
            return render(request, 'converter/success.html', {'converted_file': converted_file})
    else:
        form = VTTUploadForm()
    return render(request, 'converter/upload.html', {'form': form})

import tempfile


def convert_vtt_to_text(vtt_content):
    # Create a temporary file to store the VTT content
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
    temp_file.write(vtt_content)
    temp_file.close()

    try:
        # Parse the VTT content using webvtt-py
        subtitles = WebVTT().read(temp_file.name)
        
        # Extract text content from subtitles
        text_content = ""
        for subtitle in subtitles:
            # Encode the subtitle text as 'utf-8' and then decode it as 'latin-1', 
            # replacing characters that cannot be encoded
            encoded_text = subtitle.text.encode('utf-8', errors='ignore').decode('latin-1')
            text_content += encoded_text + " "
        
        return text_content
    finally:
        # Clean up: delete the temporary file
        import os
        os.unlink(temp_file.name)

