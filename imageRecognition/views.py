from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import tensorflow as tf
import os
from keras.preprocessing import image
import numpy as np
from datetime import datetime

# Create your views here.

from IPython.display import Image
import random

from imageRecognition.models import UploadedImage


def index(request):
    return HttpResponse("<h1>Всё успешно</h1>")

def get_file_name():
    return datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

@csrf_exempt
def upload_image_api(request):
    if request.method == 'POST' and request.FILES["image"]:
        img = UploadedImage(image=request.FILES['image'])
        img.save()

        loaded_model = tf.keras.models.load_model("kanobu.h5")
        loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        img = image.load_img(img.image.path, target_size=(60, 40), grayscale=False)
        # # Преобразуем изображением в массив numpy и нормализуем
        x = image.img_to_array(img)
        x /= 255
        x = np.expand_dims(x, axis=0)
        predictions = loaded_model.predict(x)

        predicted_class = np.argmax(predictions)
        print(predictions)
        print(predicted_class)
        #print("файлы", request.FILES)
        # paper rock scissors
        class_labels = ["Paper", "Rock", "Scissors"]
       # return JsonResponse({f'message': f'{random.choice(["Rock", "Paper", "Scissors"])}'})
        return JsonResponse({f'message': f'{class_labels[predicted_class]}'})
    return JsonResponse({'error': 'some error occurred.'}, status=400)