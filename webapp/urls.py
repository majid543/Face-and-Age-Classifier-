from django.urls import path

app_name ='webapp'


from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='image_upload'),
    path('display/',views.display_images, name='image_display'),
    path('process/<int:image_id>/', views.process_image, name='process_image'),
    path('perform_face_detection/<int:image_id>/',views.perform_face_detection, name='perform_face_detection'),
    path('perform_image_enhancement/<int:image_id>/',views.perform_image_enhancement, name='perform_image_enhancement'),
    path('perform_age_classification/<int:image_id>/',views.perform_age_classification, name='perform_age_classification')
]