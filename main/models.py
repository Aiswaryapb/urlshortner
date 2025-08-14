from django.db import models
from django.core.validators import URLValidator

class ShortURL(models.Model):
    code = models.CharField(max_length=10, unique=True, db_index=True)
    original_url = models.URLField(max_length=1000, validators=[URLValidator()])
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} → {self.original_url}"
