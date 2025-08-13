from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)       # Task name
    is_done = models.BooleanField(default=False)   # Done or Pending
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return self.title