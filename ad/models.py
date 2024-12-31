from django.db import models
from category.models import Category

class AdImage(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    image = models.ImageField(upload_to='media/images/ad/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.name}"

class Ad(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ads')
    images = models.ManyToManyField(AdImage, related_name='ads')
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    discount = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)  # Поле для отслеживания просмотров
    likes = models.PositiveIntegerField(default=0)  # Поле для отслеживания лайков
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

class AdLike(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='ad_likes')
    ip_address = models.GenericIPAddressField() # для получения IP ADRESS
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ad', 'ip_address')

    def __str__(self):
        return f"Like by {self.ip_address} for {self.ad.name}"