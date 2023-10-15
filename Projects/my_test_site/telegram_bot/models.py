from django.db import models

class Command(models.Model):
    command_text = models.TextField()
    executed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
