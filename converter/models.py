
from django.db import models

class ConvertedFile(models.Model):
    original_vtt = models.FileField(upload_to='vtt_files/')
    converted_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)
    
