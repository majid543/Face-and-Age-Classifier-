from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .models import Image
from django.conf import settings
from django.shortcuts import render
from .models import Image
from django.http import JsonResponse
import numpy as np
import cv2
from PIL import Image as PilImage
from io import BytesIO
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import os 

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save(commit=False)
            image_instance.user = request.user  # Assuming you have authentication set up
            image_instance.save()
            return redirect('webapp:process_image', image_id=image_instance.id)
    else:
        form = ImageUploadForm()

    return render(request, 'upload_image.html', {'form': form})

def display_images(request):
    images = Image.objects.filter(user=request.user)  # Assuming you have authentication set up
    return render(request, 'display_images.html', {'images': images})

def enhance_image(image):
    # Load the image
    nparr = np.fromstring(image.image.read(), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # Apply image enhancement operations
    # Example: Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Example: Apply histogram equalization for contrast enhancement
    enhanced_img = cv2.equalizeHist(gray_img)

    # Update the Image model with the path to the enhanced image
    img_encoded = cv2.imencode('.jpg', enhanced_img)[1].tostring()
    image.image.save('modified_image.jpg', ContentFile(img_encoded))
    return image

def recognize_faces(image):
    # Convert the Django ImageField data to a NumPy array
    nparr = np.fromstring(image.image.read(), np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Load the pre-trained Haar Cascade face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert the image to grayscale for face detection
    gray_image = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5)

    # Draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img_np, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display the result (for testing purposes)
    img_encoded = cv2.imencode('.jpg', img_np)[1].tostring()
    image.image.save('modified_image.jpg', ContentFile(img_encoded))
    return image
    

def detect_and_crop_face(image_np):
    # Load the pre-trained Haar Cascade face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert the image to grayscale for face detection
    gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5)

    if len(faces) > 0:
        # Choose the first detected face
        (x, y, w, h) = faces[0]

        # Crop the image to include only the detected face
        cropped_face = image_np[y:y+h, x:x+w]

        return cropped_face
    else:
        # No faces detected, return a placeholder image or default image
        # In this case, returning a black image as a placeholder
        return np.zeros((50, 50, 3), dtype=np.uint8)


import numpy as np

from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import cv2
# Function to preprocess input data
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from django.core.files.uploadedfile import InMemoryUploadedFile

# Assuming your model expects input images with shape (50, 50, 3)
def preprocess_input_data(image):
    # Read the image
    nparr = np.frombuffer(image.image.read(), np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # Use cv2.IMREAD_COLOR for color images
    img_np = detect_and_crop_face(img_np)
    # Resize the image to the model's input size
    resized_image = cv2.resize(img_np, (50, 50))

    # Normalize the pixel values to be in the range [0, 1]
    normalized_image = resized_image / 255.0

    # Add an extra dimension to simulate batch size of 1
    input_data = np.expand_dims(normalized_image, axis=0)

    return input_data

def classify_image(image):
    model = load_model('model_age.hdf5')

    # Preprocess the image
    input_data = preprocess_input_data(image)

    # Perform inference
    predictions = model.predict(input_data)

    # Assuming predictions[0] contains age predictions
    pred_age = round(predictions[0][0])

    # Print the predicted age
    print("Predicted Age:", pred_age )
    if pred_age == 83:
        return "NO FACE DETECTED Try Providing with Clearer Image of Face "
    else:
        return "Predicted Age: {}".format(pred_age)

def perform_face_detection(request, image_id):
    image = Image.objects.get(pk=image_id)
    modified_image = recognize_faces(image)
    return render(request, 'process_image.html', {'image': modified_image})

def perform_age_classification(request, image_id):
    image = Image.objects.get(pk=image_id)
    
    # Assuming that the classify_image function returns the predicted age
    pred_age = classify_image(image)  # Uncomment this line once your classify_image function is working
    
    return render(request, 'process_image.html', {'image': image, 'pred_age': pred_age})

def perform_image_enhancement(request, image_id):
    image = Image.objects.get(pk=image_id)
    modifie_image = enhance_image(image)
    return render(request, 'process_image.html', {'image': modifie_image})

def process_image(request, image_id):
    # Retrieve the Image instance
    image = Image.objects.get(pk=image_id)
    return render(request, 'process_image.html', {'image': image})



    