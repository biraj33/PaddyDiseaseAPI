from django.db import models

# Create your models here.
class ImageUpload(models.Model):
    disease_predict = models.CharField(max_length=100)
    image = models.ImageField(upload_to= 'uploads/')
    user = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)



    