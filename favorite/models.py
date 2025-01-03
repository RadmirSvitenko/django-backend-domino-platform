from django.db import models
from django.db.models import OneToOneField
from ad.models import Ad

class Favorite(models.Model):
    ads = models.ManyToManyField(Ad, related_name='favorite_ads', default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Favorite {self.id} by {self.user.email}"
