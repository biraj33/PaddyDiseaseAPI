from django.shortcuts import render
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image # type: ignore
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import ImageUploadSerializer, ImageRepredectSerilzer, SeachUserSerilizer
from .models import ImageUpload
import os
from django.db.models import Q

# Create your views here.
main_model_path = os.path.join(settings.BASE_DIR, 'ResNet50_Transfer_Learning.keras')
main_model = tf.keras.models.load_model(main_model_path)

Emotion_Classes = ['bacterial_leaf_blight', 'bacterial_leaf_streak', 'bacterial_panicle_blight', 'blast', 'brown_spot', 'dead_heart', 'downy_mildew', 'hispa', 'normal', 'tungro']


def custom_preprocess_input(img, target_size=(224, 224)):
    img_array = image.img_to_array(img)
    img_array = tf.image.resize(img_array, target_size).numpy()
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_image(image_path, model, emotion_classes=Emotion_Classes):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = custom_preprocess_input(img)
    preds = model.predict(img_array, verbose=0)
    predicted_class = np.argmax(preds, axis=1)[0]
    confidence_level = np.max(preds, axis=1)[0]
    predicted_label = emotion_classes[predicted_class]
    return predicted_label, confidence_level ,predicted_class 


class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image_instance = serializer.save()
            image_path = os.path.join(settings.MEDIA_ROOT, image_instance.image.name)

            predicted_label, confidence_level, predicted_class = predict_image(image_path, main_model)
            image_instance.disease_predict = f'{predicted_class}, {predicted_label}, {confidence_level}' 
            image_instance.save()

            return Response({
                "predection_class":predicted_class,
                "predicted_label": predicted_label,
                "confidence_level": confidence_level,
                "image-id": image_instance.id
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ImageRepredectView(APIView):
    
    def post(self, request):
        serializer = ImageRepredectSerilzer(data=request.data)
        if serializer.is_valid():
            new_id = serializer.validated_data['id']
            image  = ImageUpload.objects.get(id = new_id)
            image_path = os.path.join(settings.MEDIA_ROOT, image.image.name)
        
            predicted_label, confidence_level, predicted_class = predict_image(image_path, main_model)
            image.disease_predict = f'{predicted_class}, {predicted_label}, {confidence_level}' 
            image.save()

            return Response({
                "predection_class":predicted_class,
                "predicted_label": predicted_label,
                "confidence_level": confidence_level,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SearchUserView(APIView):
    def post(self, request):
        serializer = SeachUserSerilizer(data = request.data)
        
        if serializer.is_valid():
            print(serializer.validated_data['user'])
            datas = ImageUpload.objects.filter(user = serializer.validated_data['user'])
            all_data = []
            for i in datas:
                all_data.append({'image_id': i.id,
                                  'predict': i.disease_predict,
                                  'user': i.user
                                  })

            return Response(
               all_data
            , status=status.HTTP_200_OK)
        print("hi")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







            

